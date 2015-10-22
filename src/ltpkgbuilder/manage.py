# rev = 1
""" Contains functions to manage the structure of the package.

Use 'setup.py' for common tasks.
"""

import json
from os.path import join as pj

from local import load_handlers
from manage_tools import check_tempering, regenerate_dir, update_opt


def init_pkg(rep="."):
    """ Initialise a package in given directory
    """
    pkg_cfg = {'hash': {}}
    write_pkg_config(pkg_cfg, rep)


def get_pkg_config(rep="."):
    """ Read pkg_cfg file associated to this package

    args:
     - rep (str): directory to search for info

    return:
     - (dict of (str, dict)): option_name: options
    """
    with open(pj(rep, "pkg_cfg.json"), 'rb') as f:
        info = json.load(f)

    return info


def write_pkg_config(pkg_cfg, rep="."):
    """ Store config associated to this package on disk

    args:
     - pkg_cfg (dict of (str, dict)): option_name, options
     - rep (str): directory to search for info
    """
    with open(pj(rep, "pkg_cfg.json"), 'wb') as f:
        json.dump(pkg_cfg, f, sort_keys=True, indent=4)


def update_pkg(pkg_cfg):
    """ Check if a new version of ltpkgbuilder exists
    """
    return pkg_cfg
    # check new version of ltpkgbuilder
    # check new version of each option to know if update_opt is required


def update_option(name, pkg_cfg):
    """ Update an already installed option

    args:
     - name (str): name of option to update
     - pkg_cfg (dict of (str, dict)): option_name, options
    """
    if name not in pkg_cfg:
        raise UserWarning("Option '%s' seems not to be installed" % name)

    extra = pkg_cfg[name]  # one way to re-force already set args

    return update_opt(name, pkg_cfg, extra)


def edit_option(name, pkg_cfg):
    """ Edit an already installed option

    args:
     - name (str): name of option to update
     - pkg_cfg (dict of (str, dict)): option_name, options
    """
    if name not in pkg_cfg:
        raise UserWarning("Option '%s' seems not to be installed" % name)

    return update_opt(name, pkg_cfg)


def add_option(name, pkg_cfg, extra=None):
    """ Add a new option to this package.
    See the list of available option online

    args:
     - name (str): name of option to add
     - pkg_cfg (dict of (str, dict)): package configuration parameters
     - extra (dict): extra arguments for option configuration
    """
    if name in pkg_cfg:
        raise UserWarning("option already included in this package")

    return update_opt(name, pkg_cfg, extra)


def regenerate(pkg_cfg, target="."):
    """ Rebuild all automatically generated files

    args:
     - target (str): target directory to write into
    """
    # parse options and load handlers
    handlers = load_handlers(pkg_cfg)

    # walk all files in repo to check for possible tempering
    # of files by user
    tf = []
    check_tempering("data/base", target, handlers, pkg_cfg, tf)
    if len(tf) > 0:
        msg = "These files have been modified by user:\n"
        msg += "\n".join(tf)
        raise UserWarning(msg)

    # walk all files in repo and regenerate them
    regenerate_dir("data/base", target, handlers, pkg_cfg)
