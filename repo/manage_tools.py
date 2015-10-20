from github3 import GitHub
from hashlib import sha512
import json
import os
from os import mkdir
from os.path import basename, dirname, exists, isdir, normpath, splitext
from os.path import join as pj
from StringIO import StringIO
from urlparse import urlsplit
from zipfile import BadZipfile, ZipFile


def src_dir(info):
    """ Compute name of src dir according to pkgname
    in info
    """
    rep = "src"
    namespace = info['base']['namespace']
    if namespace is not None:
        rep = rep + "/" + namespace

    pkgname = info['base']['pkgname']
    rep = rep + "/" + pkgname

    return rep


def create_namespace_dir(dst, namespace):
    """ Create and empty dir with specific __init__.py
    for namespace packages.

    args:
     - dst (str): path in which to create the directory
     - namespace (str): namespace to use
    """
    pth = dst + "/" + namespace
    if not exists(pth):
        mkdir(pth)

    init_pth = pth + "/__init_.py"
    if not exists(init_pth):
        with open(init_pth, 'w') as f:
            f.write("__import__('pkg_resources').declare_namespace(__name__)\n")

    return pth


def parse_github_url(url):
    """ Parse a github url to extract the relevant components.

    args:
     - url (str): e.g. "https://github.com/author/repo_name/pth"

    return:
     - (str, str, str): (author, repo_name, branch, pth)
    """
    url = urlsplit(url)
    assert url.netloc.lower() == "github.com"
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
    """ Retrieve the content of a given filename
    located on the given repo_url (either local or
    located on github).

    args:
     - filename (str): name of the file to read
     - repo_url (str): root url of the resource:
         - local path e.g. "toto/pkg/"
         - local zip file e.g. "toto/pkg.zip"
         - remote path e.g. "https://github.com/author/repo/pth"
         - remote zip e.g. "https://github.com/author/repo/pth/repo.zip"
     - env (dict): extra variables for login

    return:
     - (str): content of the file red in 'r' mode
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


def ls_zip(dir_name, zf):
    """ Parse a zipfile to extract all file names
    in dir_name.

    args:
     - dir_name (str): directory name
     - zf (ZipFile): zipfile open in read mode

    return:
     - (list of (str, bool)): list of files in dir_name (name, isdir)
    """
    dir_name = normpath(dir_name)
    for pth in zf.namelist():
        if normpath(dirname(normpath(pth))) == dir_name:
            yield normpath(pth)


def ls(dir_name, repo_url=".", env=None):
    """ List all files and directories in dir_name
    located in repo_url.

    args:
     - dir_name (str): name of the directory to walk
     - repo_url (str): root url of the resource:
         - local path e.g. "toto/pkg/"
         - local zip file e.g. "toto/pkg.zip"
         - remote path e.g. "https://github.com/author/repo/pth"
         - remote zip e.g. "https://github.com/author/repo/pth/repo.zip"

    return:
     - (yield of str): iterate on the content of dir_name
                       without any specific order
    """
    if env is None:
        env = {}

    url = urlsplit(repo_url)
    if url.netloc == "":  # local file
        pth = url.path
        assert exists(pth)
        if isdir(pth):
            return [(n, isdir(pj(pth, dir_name, n)))
                    for n in os.listdir(pj(pth, dir_name))]
        else:  # presumably a zip file
            try:
                with ZipFile(pth, 'r') as zf:
                    return [(basename(pth), splitext(pth)[1] == "")
                            for pth in ls_zip(dir_name, zf)]
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
            if len(dir_name) > 0 and dir_name != ".":
                dir_pth = "/".join((pth, dir_name))
            else:
                dir_pth = pth
            data = repo.contents(dir_pth)
            return [(name, item.type == 'dir') for name, item in data.items()]
        else:  # zipfile
            try:
                data = repo.contents(pth)
                sf = StringIO(data.content.decode(data.encoding))
                with ZipFile(sf, 'r') as zf:
                    return [(basename(pth), splitext(pth)[1] == "")
                            for pth in ls_zip(dir_name, zf)]
            except BadZipfile:
                msg = "Repo must either be a directory or a valid zip file"
                raise UserWarning(msg)


class Node(object):
    """ Local class created to parse files
    """
    def __init__(self, typ, parent):
        self.typ = typ
        self.key = None
        self.parent = parent
        self.children = []
        self.data = []

        if parent is not None:
            parent.children.append(self)


def parse(txt):
    """ Parse a text for '{{class, bla }}' sections
    and construct a tree of nested sections
    """
    root = Node("root", None)
    root.key = ""
    cur_node = Node("txt", root)

    i = 0
    while i < len(txt):
        if txt[i] == "{" and txt[i + 1] == "{":
            div_node = Node("div", cur_node.parent)
            cur_node = Node("txt", div_node)
            i += 2

            # find key
            ind = txt[i:].find(",")
            div_node.key = txt[i:][:ind]
            i += ind + 1
            if txt[i] == " ":
                i += 1  # strip space after comma
        elif txt[i] == "}" and txt[i + 1] == "}":
            cur_node = Node("txt", cur_node.parent.parent)
            i += 2
        else:
            cur_node.data.append(txt[i])
            i += 1

    return root


def same(txt, env):
    """ local function created to handle no class hooks
    """
    return txt


def get_handler(key, handlers):
    """ Return an instance of a handler
    handler(txt) -> modified txt
    """
    for k in key.split(" "):
        if k in handlers:
            return handlers[k]

    return same


def div_replace(parent, handlers, env):
    """ Reconstruct the whole text inside the text
    attribute of the node and return a version
    of it transformed according to the class attribute.
    """
    txt = ""
    for node in parent.children:
        if node.typ == 'txt':
            frags = "".join(node.data).splitlines()
            if len(frags) > 0:
                # remove unnecessary '#'
                lfrag = frags[-1].strip()
                if lfrag == '#':  # new line comment
                    del frags[-1]
                elif len(lfrag) > 0 and lfrag[-1] == '#':  # inline comment
                    frags[-1] = lfrag[:-1]

            txt += "\n".join(frags)
        elif node.typ == 'div':
            txt += div_replace(node, handlers, env)
        else:
            raise UserWarning("unrecognized type of node")

    handler = get_handler(parent.key, handlers)
    return handler(txt, env)


def replace(txt, handlers, env):
    """ Parse a txt for div elements and reconstruct it
    handling the txt inside the div elements if necessary.
    """
    root = parse(txt)
    txt = div_replace(root, handlers, env)
    return txt


def get_info():
    """ Read info file associated to this package

    return:
     - (dict of (str, dict)): option_name: options
    """
    with open("pkg_info.json", 'rb') as f:
        info = json.load(f)

    return info


def write_info(info):
    """ Store info associated to this package on disk

    args:
     - info (dict of (str, dict)): option_name, options
    """
    with open("pkg_info.json", 'wb') as f:
        json.dump(info, f, sort_keys=True, indent=4)


def get_revision(txt):
    """ Get file revision as defined locally by a single statement
    # rev =
    on a single line
    """
    for line in txt.splitlines():
        if line.startswith("# rev = "):
            return int(line[8:].strip())

    return None


def write_file(pth, content, hashmap):
    """ Write the content of a file on a local path
    register associated hash for further modification
    tests.

    args:
     - pth (str): path to the new created file
     - content (str): content to write on disk
     - hashmap (dict of (str: sha512)): mapping between
                 file path and hash keys
    """
    with open(pth, 'w') as f:
        f.write(content)

    algo = sha512()
    algo.update(content)
    hashmap[pth] = algo.digest().decode("latin1")


def user_modified(pth, hashmap):
    """ Check whether the file ahs been tempered by user
    according to a stored hash.

    args:
     - pth (str): full path to the file
     - hashmap (dict of pth: sha512): table of hash keys

    return:
     - False: if file do not have a hash or if stored hash
              is different equal stored one
     - True: if file hash is different from stored one
    """
    if pth not in hashmap:
        return False

    ref_hash = hashmap[pth]

    algo = sha512()
    with open(pth, 'r') as f:
        algo.update(f.read())

    new_hash = algo.digest().decode("latin1")
    return new_hash != ref_hash


# def compare_revision(file_pth, repo_url):
#     """ Fetch the content of file_name in the repository
#     and compare its revision to the revision of the same
#     local file.
#     """
#     with open(file_pth, 'r') as f:
#         local_rev = get_revision(f.read())
#
#     txt = get(file_pth, repo_url)
#     rev = get_revision(txt)
#
#     return rev > local_rev, txt

# def copyall(cur_src_pth, cur_dst_pth, repo_url):
#     """ Parse cur_src_pth assumed to be a directory
#     and copy everything in cur_dst_pth.
#
#     Function called recursively on sub directories
#
#     Does not make any test on the existence of cur_dst_pth
#
#     args:
#      - cur_src_pth (str): current pth to look into
#      - cur_dst_pth (str): mirror of cur_src_pth on destination
#      - repo_url (str): base url of source repository
#     """
#     items = ls(cur_src_pth, repo_url)
#     for name, is_dir_type in items:
#         if is_dir_type:
#             dst_dir = cur_dst_pth + "/" + name
#             mkdir(dst_dir)
#             copyall(cur_src_pth + "/" + name, dst_dir, repo_url)
#         else:
#             src_content = get(cur_src_pth + "/" + name, repo_url)
#             with open(cur_dst_pth + "/" + name, 'w') as f:
#                 f.write(src_content)
