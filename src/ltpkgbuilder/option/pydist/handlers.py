from importlib import import_module

from ltpkgbuilder.local import installed_options


def requirements(txt, env):
    """ Check all requirements for installed options
    and add them to setup.py
    """
    reqs = set()
    for name in installed_options(env):
        try:
            opt_require = import_module("ltpkgbuilder.option.%s.require" % name)
            reqs.update(opt_require.install)
        except ImportError:
            raise KeyError("option '%s' does not exists" % name)

    reqs_str = ", ".join(["'%s'" %n for n in reqs])
    return "install_requires=[%s]," % reqs_str


mapping = {"requirements": requirements}
