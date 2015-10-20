from os import chdir
from os.path import exists
from shutil import rmtree
from subprocess import call

if exists("toto"):
    rmtree("toto")

call("python crpkg.py toto -url repo", shell=True)

chdir("toto")

call("python manage.py add -opt github -url ..\\repo")
call("python manage.py add -opt license -url ..\\repo")

call("python manage.py upgrade -url ..\\repo")
