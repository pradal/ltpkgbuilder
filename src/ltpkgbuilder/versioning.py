from distutils.version import StrictVersion
from urllib2 import urlopen

github_url = "https://raw.githubusercontent.com/revesansparole/ltpkgbuilder/master/src/ltpkgbuilder/version.py"


def get_github_version():
    """ Fetch the current version of this package on master branch
     on github.
    """
    response = urlopen(github_url)
    pycode = response.read()

    ast = compile(pycode, "<file>", 'exec')
    d = {}
    eval(ast, d)

    return StrictVersion(d['__version__'])


def get_local_version():
    """ Fetch the current installed version of this package
    """
    import ltpkgbuilder
    return StrictVersion(ltpkgbuilder.__version__)
