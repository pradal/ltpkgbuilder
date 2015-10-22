from glob import glob
import json
from os import chdir, getcwd, mkdir
from os.path import exists
from shutil import rmtree
from subprocess import call

pkg_dir = "pkg_tata"
venv_dir = "venv_toto"

if exists(venv_dir):
    rmtree(venv_dir)

if exists(pkg_dir):
    rmtree(pkg_dir)

mkdir(pkg_dir)

# generate virtual env for this session
call("virtualenv %s" % venv_dir, shell=True)
execfile("%s/Scripts/activate_this.py" % venv_dir,
         dict(__file__="%s/Scripts/activate_this.py" % venv_dir))

cwd = getcwd()

# install requirements from local depot
reqs = ["six", "pbr", "funcsigs", "nose", "coverage", "mock", "lice"]

chdir("wheels")


def find_wheel(name):
    for fname in glob("*.whl"):
        if name in fname:
            return fname

for req in reqs:
    whl = find_wheel(req)
    if whl is not None:
        call("pip install %s" % whl)


# install ltpkgbuiler
chdir("../..")

call("python setup.py develop", shell=True)

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
pkg_cfg['github'] = dict(user="revesansparole",
                         project="toto")
pkg_cfg['pydist'] = dict(description="belle description",
                         keywords="keys, words")

with open("pkg_cfg.json", 'w') as f:
    json.dump(pkg_cfg, f)

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
