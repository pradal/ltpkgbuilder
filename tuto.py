import json
from os import chdir
from os.path import exists
from shutil import rmtree
from subprocess import call

if exists("toto"):
    rmtree("toto")

call("python crpkg.py toto -url repo", shell=True)

chdir("toto")

# with open("pkg_info.json", 'r') as f:
#     info = json.load(f)
#
# info['license'] = {"name": "mit",
#                    "organization": "openalea",
#                    "project": "toto",
#                    "year": "2015"}
#
# with open("pkg_info.json", 'w') as f:
#     json.dump(info, f)

# call("python manage.py add -opt github -url ..\\repo")
# call("python manage.py add -opt license -url ..\\repo")
#
# call("python manage.py add -opt dist -url ..\\repo")

call("python manage.py add -opt base -url ..\\repo")
call("python manage.py add -opt test -url ..\\repo")
call("python manage.py add -opt doc -url ..\\repo")

call("python manage.py upgrade -url ..\\repo")
