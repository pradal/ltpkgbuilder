from os import mkdir, remove
from os.path import abspath
from shutil import rmtree
from zipfile import ZipFile

from manage_tools import get


gh_url = "https://github.com/revesansparole/starter_tpl/tree/master/testpb/"


def test_tools_get_local_dir():
    repo = "titi1"
    mkdir(repo)
    with open(repo + "/test.txt", 'w') as f:
        f.write("loren ipsum")

    txt = get("test.txt", repo)
    assert txt == "loren ipsum"

    rmtree(repo)


def test_tools_get_local_dir_abs_path():
    repo = abspath("titi2")
    mkdir(repo)
    with open(repo + "/test.txt", 'w') as f:
        f.write("loren ipsum")

    txt = get("test.txt", repo)
    assert txt == "loren ipsum"

    rmtree(repo)


def test_tools_get_local_dir_subdir():
    repo = "titi3"
    mkdir(repo)
    mkdir(repo + "/subdir")
    with open(repo + "/subdir/test.txt", 'w') as f:
        f.write("loren ipsum")

    txt = get("subdir/test.txt", repo)
    assert txt == "loren ipsum"

    rmtree(repo)


def test_tools_get_local_zip():
    repo = "titi.zip"
    zf = ZipFile(repo, 'w')
    zf.writestr("test.txt", "loren ipsum")
    zf.close()

    txt = get("test.txt", repo)
    assert txt == "loren ipsum"

    remove(repo)


def test_tools_get_local_zip_subdir():
    repo = "titi2.zip"
    zf = ZipFile(repo, 'w')
    zf.writestr("subdir/test.txt", "loren ipsum")
    zf.close()

    txt = get("subdir/test.txt", repo)
    assert txt == "loren ipsum"

    remove(repo)


# def test_tools_get_github_dir():
#     repo = gh_url + "repo"
#
#     txt = get("test.txt", repo)
#     assert txt.rstrip() == "toto was here"
#
#
# def test_tools_get_github_subdir():
#     repo = gh_url + "repo"
#
#     txt = get("sub/test.txt", repo)
#     assert txt.rstrip() == "and also here"
#
#
# def test_tools_get_github_zip():
#     repo = gh_url + "repo.zip"
#
#     txt = get("test.txt", repo)
#     assert txt.rstrip() == "toto was here"
#
#
# def test_tools_get_github_zip_subdir():
#     repo = gh_url + "repo.zip"
#
#     txt = get("sub/test.txt", repo)
#     assert txt.rstrip() == "and also here"
