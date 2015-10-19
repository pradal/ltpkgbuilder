""" Script use main function
"""

from github3 import GitHub
import json
from os import mkdir, chdir
from os.path import abspath, exists, isdir, splitext
from os.path import join as pj
from StringIO import StringIO
from urlparse import urlsplit
from zipfile import BadZipfile, ZipFile


def parse_github_url(url):
    """ Local copy of manage_tools.py:parse_github_url
    """
    url = urlsplit(url)
    assert url.netloc == "github.com"
    elms = url.path.split("/")
    author = elms[1]
    repo_name = elms[2]
    if len(elms) == 3:
        branch = 'master'
        pth = ""
    else:
        branch = elms[4]
        pth = elms[5:]
        if len(pth) > 0 and len(pth[-1]) == 0:
            del pth[-1]

    return author, repo_name, branch, "/".join(pth)


def get(file_name, repo_url=".", env=None):
    """ Local copy of manage_tools.py:get
    """
    if env is None:
        env = {}

    url = urlsplit(repo_url)
    if url.netloc == '':  # local file
        pth = url.path
        assert exists(pth)
        if isdir(pth):
            with open(pj(pth, file_name), 'r') as f:
                return f.read()
        else:  # presumably a zip file
            try:
                with ZipFile(pth, 'r') as zf:
                    f = zf.open(file_name, 'r')
                    return f.read()
            except BadZipfile:
                msg = "Repo must either be a directory or a valid zip file"
                raise UserWarning(msg)
    else:  # remote file on github
        author, repo_name, branch, pth = parse_github_url(repo_url)
        try:
            gh = GitHub(login=env['user'], password=env['password'])
        except KeyError:  # attempt anonymous login
            gh = GitHub()
        repo = gh.repository(author, repo_name)
        if splitext(pth)[1] == "":  # assume remote directory
            file_pth = "/".join((pth, file_name))
            data = repo.contents(file_pth)
            return data.content.decode(data.encoding)
        else:  # zipfile
            try:
                data = repo.contents(pth)
                sf = StringIO(data.content.decode(data.encoding))
                with ZipFile(sf, 'r') as zf:
                    f = zf.open(file_name, 'r')
                    return f.read()
            except BadZipfile:
                msg = "Repo must either be a directory or a valid zip file"
                raise UserWarning(msg)


def main(name, repo_url, env):
    """ Create a new package from scratch. Just
    copy manage.py and manage_tools.py in a new
    driectory and add 'base' option.

    .. warning: need to run the newly created manage.py
                to obtain a valid package.

    args:
     - name (str): full package name including namespaces
                   e.g. 'mypkg' or 'openalea.mypkg'
     - repo_url (str): url of repository to use for fetching files
     - env (dict): github environment
    """
    root = name.split(".")[-1]

    # create root directory
    if exists(root):
        if isdir(root):  # TODO: offer overwrite
            raise UserWarning("root dir already exists")
        else:
            raise UserWarning("root dir already exists as a file")
    else:
        mkdir(root)

    # copy manage.py and tools files
    for fname in ("manage.py", "manage_tools.py"):
        try:
            pycode = get(fname, repo_url, env)
            with open(root + "/" + fname, 'w') as f:
                f.write(pycode)
                f.close()
        except OSError:
            msg = "Bad repository format, must contain '%s'" % fname
            raise UserWarning(msg)

    # create a basic package info with info harvested
    # during the creation process
    with open(root + "/pkg_info.json", 'w') as f:
        json.dump({"hash": {}}, f)

    # add base option
    extra = dict(pkgname=name)

    if urlsplit(repo_url).netloc == '':
        repo_url = abspath(repo_url)

    sys.path.append(abspath(root))
    chdir(root)
    d = {}
    execfile("manage.py", d)
    d['add_option']("base", repo_url, extra, env)

    # launch regenerate
    d['regenerate'](repo_url, env=env)


if __name__ == '__main__':
    import sys
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Package creator')
    parser.add_argument('pkgname', metavar='pkg_name',
                        help="name of the package to create")  # TODO add gestion of namespace.pkg

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

    main(args.pkgname, repo_url, env)
