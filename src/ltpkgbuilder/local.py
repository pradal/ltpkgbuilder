""" Regroup set of functions that make use of local environment
inside a package. Just a way to normalize pre defined paths.
"""

from importlib import import_module
from os import mkdir
from os.path import exists

from .file_management import write_file
from .templating import same


# def src_dir(info):
#     """ Compute name of src dir according to pkgname
#     and namespace in info
#     """
#     rep = "src"
#     namespace = info['base']['namespace']
#     if namespace is not None:
#         rep = rep + "/" + namespace
#
#     pkgname = info['base']['pkgname']
#     rep = rep + "/" + pkgname
#
#     return rep


def installed_options(pkg_cfg):
    """ Returns a list of installed options according
    to the package config file.
    """
    opts = list(pkg_cfg.keys())

    # handle 'hash' key
    try:
        opts.remove("hash")
    except ValueError:
        pass

    return opts


namespace_txt = """
__import__('pkg_resources').declare_namespace(__name__)
"""


def create_namespace_dir(dst, namespace, pkg_cfg):
    """ Create and empty dir with specific __init__.py
    for namespace packages.

    args:
     - dst (str): path in which to create the directory
     - namespace (str): namespace to use
     - pkg_cfg (dict of (str: dict)): package config info
    """
    pth = dst + "/" + namespace
    if not exists(pth):
        mkdir(pth)

    init_pth = pth + "/__init__.py"
    if not exists(init_pth):
        write_file(init_pth, namespace_txt, pkg_cfg['hash'])

    return pth


def load_handlers(pkg_cfg):
    """ Load handlers for installed options

    args:
     - pkg_cfg (dict of (str: dict)): package config
    """
    handlers = {}
    for name in installed_options(pkg_cfg):
        handlers[name] = same
        # find definition file
        try:
            opt_handlers = import_module("ltpkgbuilder.option.%s.handlers" % name)
        except ImportError:
            raise KeyError("option '%s' does not exists" % name)

        handlers.update(opt_handlers.mapping)

    return handlers
