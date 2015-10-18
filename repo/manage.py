# rev = 1
""" Contains functions to manage the structure of the package.

Use 'setup.py' for common tasks.
"""

import json
from os import mkdir
from os.path import exists
from manage_tools import get, get_revision, ls, replace


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

    with open("pkg_info.json", 'r') as f:
        info = json.load(f)

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
    with open("pkg_info.json", 'w') as f:
        json.dump(info, f)


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
    """
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
                with open(cur_dst_pth + "/" + new_name, 'w') as f:
                    f.write(new_src_content)


def regenerate(repo=default_repo, target=".", env=None):
    """ Rebuild all automatically generated files

    args:
     - repo (str): url of repository to use
     - target (str): target directory to write into
     - env (dict): environment for github access
    """
    # check for new version of this file and tools file
    for filename in ("manage.py", "manage_tools.py")[:1]:
        with open(filename, 'r') as f:
            local_rev = get_revision(f.read())

        txt = get('%s' % filename, repo, env)
        rev = get_revision(txt)

        if rev > local_rev:
            print "newer file: %s" % filename
            with open(filename, 'w') as f:
                f.write(txt)

    # parse options and load handlers
    with open("pkg_info.json", 'r') as f:
        info = json.load(f)

    print "info", info

    handlers = {}
    for opt_name in info.keys():
        # find definition file
        try:
            pycode = get("option/%s/handlers.py" % opt_name, repo, env)
        except IOError:
            raise UserWarning("option '%s' does not exists" % opt_name)

        d = {}
        eval(compile(pycode, "handlers", 'exec'), d)
        handlers.update(d['handlers'])

    print "handlers", handlers
    # walk all files in repo and regenerate them
    regenerate_dir("base", target, repo, handlers, info, env)

