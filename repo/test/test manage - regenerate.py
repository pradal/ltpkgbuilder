import json
from nose.tools import assert_raises, with_setup
from os import listdir, mkdir, remove, walk
from os.path import exists
from shutil import copytree, rmtree

from manage import regenerate, add_option

repo = "takapouet"
rb = repo + "/base"


def setup():
    if not exists(repo):
        mkdir(repo)

    if not exists(rb):
        mkdir(rb)

    with open(repo + "/manage.py", 'w') as f:
        f.write("# rev = 0\nloren ipsum")

    if not exists(repo + "/option"):
        copytree("option", repo + "/option")

    with open("pkg_info.json", 'w') as f:
        json.dump({'hash': {}}, f)

    add_option('base', extra={'pkg_fullname': repo})
    # add_option('test1')


def teardown():
    if exists(repo):
        rmtree(repo)

    if exists('pkg_info.json'):
        remove('pkg_info.json')


@with_setup(setup, teardown)
def test_regenerate_walk_all_files_in_repo_base():
    # create false repo
    mkdir(rb + "/dir1")
    mkdir(rb + "/dir2")
    mkdir(rb + "/dir1/subdir")
    for fname in ("/dir1/toto.txt", "/dir2/titi.py", "/dir1/subdir/tutu.txt"):
        with open(rb + fname, 'w') as f:
            f.write("I was here\nloren ispum\n")

    # do regenerate
    nr = "toto1"
    mkdir(nr)
    regenerate(repo, nr)

    ref_fnames = set()
    for r, d, fs in walk(rb):
        ref_fnames.update(fs)

    crt_fnames = set()
    for r, d, fs in walk(nr):
        crt_fnames.update(fs)

    print ref_fnames
    print crt_fnames
    assert ref_fnames == crt_fnames

    rmtree(nr)


@with_setup(setup, teardown)
def test_regenerate_replace_directory_names():
    mkdir(rb + "/{{rm, to}}toko")

    # do regenerate
    nr = "toto1"
    mkdir(nr)
    regenerate(repo, nr)

    assert not exists(nr + "/{{rm, to}}toko")
    assert exists(nr + "/toko")

    rmtree(nr)


@with_setup(setup, teardown)
def test_regenerate_do_not_create_directory_with_empty_name():
    mkdir(rb + "/{{rm, toto}}")

    # do regenerate
    nr = "toto2"
    mkdir(nr)
    regenerate(repo, nr)

    assert not exists(nr + "/{{rm, toto}}")
    assert not exists(nr + "/toto")

    rmtree(nr)


@with_setup(setup, teardown)
def test_regenerate_replace_file_names():
    with open(rb + "/{{rm, to}}to.txt", 'w') as f:
        f.write("loren ipsum")

    # do regenerate
    nr = "toto3"
    mkdir(nr)
    regenerate(repo, nr)

    assert not exists(nr + "/{{rm, to}}to.txt")
    assert not exists(nr + "/toto.txt")
    assert exists(nr + "/to.txt")

    rmtree(nr)


@with_setup(setup, teardown)
def test_regenerate_do_not_create_file_with_empty_name():
    with open(rb + "/{{del, toto.txt}}", 'w') as f:
        f.write("loren ipsum")

    with open(rb + "/{{del, titi}}.txt", 'w') as f:
        f.write("loren ipsum")

    # do regenerate
    nr = "toto4"
    mkdir(nr)
    regenerate(repo, nr)

    assert not exists(nr + "/{{del, toto.txt}}")
    assert not exists(nr + "/toto.txt")
    assert not exists(nr + "/{{del, titi}}.txt")
    assert not exists(nr + "/titi.txt")
    assert len(listdir(nr)) == 0

    rmtree(nr)


@with_setup(setup, teardown)
def test_regenerate_replace_file_content():
    with open(rb + "/toto.txt", 'w') as f:
        f.write("loren ipsum {{upper, nothing}} loren ipsum")

    # do regenerate
    nr = "toto5"
    mkdir(nr)
    regenerate(repo, nr)

    assert exists(nr + "/toto.txt")
    with open(nr + "/toto.txt", 'r') as f:
        txt = f.read()
        assert txt == "loren ipsum NOTHING loren ipsum"

    rmtree(nr)


