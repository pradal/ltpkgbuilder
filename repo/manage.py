# rev = 1
""" Contains functions to manage the structure of the package.

Use 'setup.py' for common tasks.
"""

import json
from os import mkdir
from os.path import exists
from urlparse import urlsplit

from manage_tools import (get, get_revision, ls,
                          get_info, write_info,
                          same, replace,
                          user_modified, write_file,
                          src_dir, create_namespace_dir)


default_repo = "."


def add_option(name, repo=default_repo, extra=None, env=None):
    """ Add a new option to this package.
    See the list of available option online

    args:
     - name (str): name of option to add
     - repo (url): repository to look for existing options
     - extra (dict): extra arguments for option config
     - env (dict): environment for github repository
    """
    if extra is None:
        extra = {}

    info = get_info()

    if name in info:
        raise UserWarning("option already included in this package")

    # find option definition in repository
    try:
        pycode = get("option/%s/config.py" % name, repo, env)
    except IOError:
        raise KeyError("option '%s' does not exists" % name)

    d = {}
    eval(compile(pycode, "optiondef", 'exec'), d)

    if 'main' not in d:
        raise SyntaxError("badly defined config for option '%s'" % name)

    # execute main function to retrieve config options
    option_cfg = d['main'](info, extra)

    # write new pkg_info file
    info[name] = option_cfg
    write_info(info)


def load_handlers(repo, env):
    """ Load handlers for installed options

    args:
     - repo (url): url of repository to find handlers definitions
     - env (dict): environment for github
    """
    info = get_info()

    handlers = {}
    installed_options = info.keys()
    installed_options.remove("hash")

    for opt_name in installed_options:
        handlers[opt_name] = same
        # find definition file
        try:
            pycode = get("option/%s/handlers.py" % opt_name, repo, env)
        except IOError:
            raise UserWarning("option '%s' does not exists" % opt_name)

        d = {}
        eval(compile(pycode, "handlers", 'exec'), d)
        handlers.update(d['handlers'])

    return handlers


def check_tempering(cur_src_pth, cur_dst_pth, repo_url, handlers, info, env, tf):
    """ Parse cur_src_pth assumed to be a directory
    in repository and check all files in it to detect
    tempering by user

    Function called recursively on sub directories

    Does not make any test on the existence of cur_dst_pth

    args:
     - cur_src_pth (str): current pth to look into
     - cur_dst_pth (str): mirror of cur_src_pth on destination
     - repo_url (str): base url of source repository
     - handlers (dict of func): associate keys to handler functions
     - info (dict): more information to pass to handlers
     - env (dict): environment for github
     - tf (list of str): list of tempered files to update, side effect
    """
    print "check", cur_src_pth, cur_dst_pth
    items = ls(cur_src_pth, repo_url)
    for name, is_dir_type in items:
        if is_dir_type:
            new_name = replace(name, handlers, info)
            if new_name != "":
                dst_dir = cur_dst_pth + "/" + new_name
                if not exists(dst_dir):
                    print "Directory '%s' has been removed" % dst_dir
                else:
                    check_tempering(cur_src_pth + "/" + name,
                                    dst_dir,
                                    repo_url,
                                    handlers,
                                    info,
                                    env,
                                    tf)
        else:
            print "check file", name
            new_name = replace(name, handlers, info)
            if new_name != "":
                pth = cur_dst_pth + "/" + new_name
                if user_modified(pth, info['hash']):
                    print "user modified file: %s" % pth
                    tf.append(pth)


def regenerate_dir(cur_src_pth, cur_dst_pth, repo_url, handlers, info, env):
    """ Parse cur_src_pth assumed to be a directory
    in repository and regenerate all files in it
    copy regenerated files in cur_dst_pth.

    Function called recursively on sub directories

    Does not make any test on the existence of cur_dst_pth

    args:
     - cur_src_pth (str): current pth to look into
     - cur_dst_pth (str): mirror of cur_src_pth on destination
     - repo_url (str): base url of source repository
     - handlers (dict of func): associate keys to handler functions
     - info (dict): more information to pass to handlers
     - env (dict): environment for github

    return:
     - cur_dst_pth (str): in case it has been modified
    """
    if cur_src_pth == "base/src":
        print "specific treatment for src"
        # check for namespace directory
        namespace = info['base']['namespace']
        if namespace is not None:
            cur_dst_pth = create_namespace_dir(cur_dst_pth, namespace)

        # create pkgname directory in src
        pkgname = info['base']['pkgname']
        cur_dst_pth = cur_dst_pth + "/" + pkgname
        if not exists(cur_dst_pth):
            mkdir(cur_dst_pth)

    print "act", cur_src_pth, cur_dst_pth
    items = ls(cur_src_pth, repo_url)
    for name, is_dir_type in items:
        if is_dir_type:
            new_name = replace(name, handlers, info)
            if new_name != "":  # TODO: Bof when removing one option
                dst_dir = cur_dst_pth + "/" + new_name
                if not exists(dst_dir):
                    mkdir(dst_dir)

                regenerate_dir(cur_src_pth + "/" + name,
                               dst_dir,
                               repo_url,
                               handlers,
                               info,
                               env)
        else:
            print "act file", name
            new_name = replace(name, handlers, info)
            if new_name != "":  # TODO: Bof when removing one option
                src_content = get(cur_src_pth + "/" + name, repo_url, env)
                new_src_content = replace(src_content, handlers, info)
                # overwrite file without any warning
                write_file(cur_dst_pth + "/" + new_name,
                           new_src_content,
                           info['hash'])


def regenerate(repo=default_repo, target=".", env=None):
    """ Rebuild all automatically generated files

    args:
     - repo (str): url of repository to use
     - target (str): target directory to write into
     - env (dict): environment for github access
    """
    # load info file
    info = get_info()

    # check for new version of this file and tools file
    need_reload = False
    for filename in ("manage.py", "manage_tools.py")[:1]:
        with open(filename, 'r') as f:
            local_rev = get_revision(f.read())

        txt = get('%s' % filename, repo, env)
        rev = get_revision(txt)

        if rev > local_rev:
            print "newer file: %s" % filename
            if user_modified(filename, info['hash']):
                raise UserWarning("File has been modified by user")

            write_file(filename, txt, info['hash'])
            # with open(filename, 'w') as f:
            #     f.write(txt)
            need_reload = True

    if need_reload:
        print "manage.py have been updated with new version, relaunch"
        return

    # parse options and load handlers
    handlers = load_handlers(repo, env)

    # walk all files in repo to check for possible tempering
    # of files by user
    tf = []
    check_tempering("base", target, repo, handlers, info, env, tf)
    if len(tf) > 0:
        msg = "These files have been modified by user:\n"
        msg += "\n".join(tf)
        raise UserWarning(msg)

    # walk all files in repo and regenerate them
    regenerate_dir("base", target, repo, handlers, info, env)

    # rewrite info
    write_info(info)


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Package structure manager')
    parser.add_argument('action', metavar='action',
                        help="action to perform on package")

    parser.add_argument('-url', '--url', metavar='repo_url',
                        help="url of repository for fetching definitions")

    parser.add_argument('-u', '--user', metavar='user',
                        help="github username")

    parser.add_argument('-p', '--password', metavar='password',
                        help="github password")

    args = parser.parse_args()

    if args.url is None:
        repo_url = "https://github.com/revesansparole/ltpkgbuilder/tree/master/repo"
    else:
        repo_url = args.url

    if urlsplit(repo_url).netloc == '':
        env = None
    else:
        user = args.user
        if user is None:
            user = raw_input("user:")

        if len(user) == 0:  # anonymous login
            env = {}
        else:
            pwd = args.password
            if pwd is None:
                pwd = raw_input("password:")

            env = dict(user=user, password=pwd)

    if args.action == 'upgrade':
        print "upgrade"
        regenerate(repo_url, env=env)
    else:
        print "unknown"
