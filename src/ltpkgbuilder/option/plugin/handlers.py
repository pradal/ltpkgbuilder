import __builtin__
from collections import OrderedDict
from inspect import getmembers, getmodule, isclass
from os import chdir, getcwd, walk
from os.path import abspath, dirname, normpath, sep, splitext
import sys

from ltpkgbuilder.local import src_dir


def discover_plugin(root, filename):
    """ Find all defined plugins in the given file
    located in root directory.
    """
    mem_dir = getcwd()
    chdir(root)
    sys.path.insert(0, root)

    # evaluate file
    with open(filename, 'r') as f:
        pycode = f.read()

    ast = compile(pycode, filename, 'exec')

    d = OrderedDict()
    eval(ast, d)
    # del d['__builtins__']

    plugins = []
    for name, obj in d.items():
        mod = getmodule(obj)
        if mod is None or (isclass(obj) and mod == __builtin__):
            # i.e. object defined in this file
            mbs = dict(getmembers(obj))
            if '__plugin__' in mbs:
                plugins.append((name, mbs['__plugin__']))

    chdir(mem_dir)
    del sys.path[0]

    return plugins


def get_definition_id(root, pth, obj_name):
    """ Construct a python identifier for reconstructing
    the given object.

    args:
     - root (str): base path for package
     - pth (str): absolute path to the definition file of the object
     - obj_name (str): object name as defined in the file

    return:
     - (str): 'pkg.module:obj_name' such as 'from pkgmodule import obj_name'
              is a valid statement.
    """
    root = dirname(normpath(abspath(root)))
    pth = normpath(abspath(pth))
    assert pth.startswith(root)

    mod_pth = pth[(len(root) + 1):].split(sep)
    mod_pth[-1] = splitext(mod_pth[-1])[0]
    return ".".join(mod_pth) + ":" + obj_name


def setup(txt, env):
    """ Find all objects defined as plugins and install them
    as entry points
    """
    # walk all files:
    pkg_dir = src_dir(env)
    print getcwd(), pkg_dir

    for root, dnames, fnames in walk(pkg_dir):
        for name in fnames:
            if splitext(name)[1] == ".py":
                print "Xplo", name
                plugins = discover_plugin(abspath(root), name)
                for p_name, p_gr in plugins:
                    p_def = get_definition_id(pkg_dir, root + "/" + name, p_name)
                    print p_def

    return txt


mapping = {"plugin.setup": setup}
