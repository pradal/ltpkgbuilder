from glob import glob
import json
from os import chdir, getcwd, mkdir
from os.path import exists
from shutil import rmtree
from subprocess import call
import sys
from sys import argv

if len(argv) > 1:
    install_mode = argv[1]
else:
    install_mode = "develop"

pkg_dir = "pkg_tata"
venv_dir = "venv_toto"


def find_wheel(name):
    for fname in glob("wheels/*.whl"):
        if name in fname:
            return fname


def create_venv():
    try:
        if exists(venv_dir):
            rmtree(venv_dir)

    except OSError:
        print("unable to create dir")
        sys.exit(0)

    call("virtualenv %s" % venv_dir, shell=True)

    # install requirements from local depot
    reqs = ["six", "pbr", "funcsigs", "nose", "coverage", "mock", "lice"]

    for req in reqs:
        whl = find_wheel(req)
        if whl is not None:
            call("pip install %s" % whl)


try:
    if exists(pkg_dir):
        rmtree(pkg_dir)

    mkdir(pkg_dir)
except OSError:
    print("unable to create dir")
    sys.exit(0)

# generate virtual env for this session
if len(argv) > 2:
    create_venv()

execfile("%s/Scripts/activate_this.py" % venv_dir,
         dict(__file__="%s/Scripts/activate_this.py" % venv_dir))

cwd = getcwd()

# install ltpkgbuiler
chdir("..")

call("python setup.py %s" % install_mode, shell=True)

# generate new package
chdir(cwd + "/" + pkg_dir)

call("manage init")

# call("manage add -opt dist")
# call("manage add -opt github")

with open("pkg_cfg.json", 'r') as f:
    pkg_cfg = json.load(f)

pkg_cfg['base'] = dict(pkg_fullname='toto',
                       pkgname='toto',
                       namespace=None,
                       author_name='moi')

pkg_cfg['doc'] = dict(option=None)
pkg_cfg['test'] = dict(option=None)
pkg_cfg['license'] = dict(name="mit",
                          year="2015",
                          organization="oa",
                          project="toto")
pkg_cfg['version'] = dict(major="0", minor="5", post="0")
pkg_cfg['pydist'] = dict(description="belle description",
                         keywords="keys, words")
pkg_cfg['coverage'] = dict(option=None)

# pkg_cfg['github'] = dict(user="revesansparole",
#                          project="toto")
# pkg_cfg['plugin'] = dict(option=None)

with open("pkg_cfg.json", 'w') as f:
    json.dump(pkg_cfg, f)

call("manage regenerate")

call("manage add -opt example -e option_name base")
call("manage add -opt example -e option_name test")

call("manage regenerate")

# call("manage add -opt test")
# call("manage add -opt doc")
#
# call("manage regenerate")
#
# call("manage update -opt base")
#
# call("manage regenerate")
#
# call("manage edit -opt base")

call("nosetests")