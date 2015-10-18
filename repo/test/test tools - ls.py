from os import mkdir, remove
from os.path import abspath
from shutil import rmtree
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

from manage_tools import ls


gh_url = "https://github.com/revesansparole/starter_tpl/tree/master/testpb/"


def test_tools_ls_local_dir():
    repo = "tata1"
    mkdir(repo)
    with open(repo + "/test.txt", 'w') as f:
        f.write("loren ipsum")
    mkdir(repo + "/toto")
    with open(repo + "/toto/test.txt", 'w') as f:
        f.write("loren ipsum")

    l = ls("", repo)
    assert set(l) == {("test.txt", False),
                      ("toto", True)}

    rmtree(repo)


def test_tools_ls_local_absdir():
    repo = abspath("tata1")
    mkdir(repo)
    with open(repo + "/test.txt", 'w') as f:
        f.write("loren ipsum")
    mkdir(repo + "/toto")
    with open(repo + "/toto/test.txt", 'w') as f:
        f.write("loren ipsum")

    l = ls("", repo)
    assert set(l) == {("test.txt", False),
                      ("toto", True)}

    rmtree(repo)


def test_tools_ls_local_dir_subdir():
    repo = "tata2"
    mkdir(repo)
    with open(repo + "/test.txt", 'w') as f:
        f.write("loren ipsum")
    mkdir(repo + "/toto")
    with open(repo + "/toto/test.txt", 'w') as f:
        f.write("loren ipsum")

    l = ls("toto", repo)
    assert set(l) == {("test.txt", False)}

    rmtree(repo)


def test_tools_ls_local_zip():
    repo = "tata.zip"
    zf = ZipFile(repo, 'w')
    zf.writestr("test.txt", "loren ipsum")
    zipi = ZipInfo()
    zipi.filename = "toto/" # this is what you want
    zipi.compress_type = ZIP_DEFLATED
    zf.writestr(zipi, "")
    zf.writestr("toto/test.txt", "loren ipsum")
    zf.close()

    l = ls("", repo)
    assert set(l) == {("test.txt", False),
                      ("toto", True)}

    remove(repo)


def test_tools_ls_local_zip_subdir():
    repo = "tata2.zip"
    zf = ZipFile(repo, 'w')
    zf.writestr("test.txt", "loren ipsum")
    zipi = ZipInfo()
    zipi.filename = "toto/" # this is what you want
    zipi.compress_type = ZIP_DEFLATED
    zf.writestr(zipi, "")
    zf.writestr("toto/test.txt", "loren ipsum")
    zf.close()

    l = ls("toto", repo)
    assert set(l) == {("test.txt", False)}

    remove(repo)


# def test_tools_get_github_dir():
#     repo = gh_url + "repo"
#
#     l = ls("", repo)
#     assert set(l) == {("test.txt", False),
#                       ("sub", True)}
#
#
# def test_tools_get_github_subdir():
#     repo = gh_url + "repo"
#
#     l = ls("sub", repo)
#     assert set(l) == {("test.txt", False)}
#
#
# def test_tools_get_github_zip():
#     repo = gh_url + "repo.zip"
#
#     l = ls("", repo)
#     assert set(l) == {("test.txt", False),
#                       ("sub", True)}
#
#
# def test_tools_get_github_zip_subdir():
#     repo = gh_url + "repo.zip"
#
#     l = ls("sub", repo)
#     assert set(l) == {("test.txt", False)}
