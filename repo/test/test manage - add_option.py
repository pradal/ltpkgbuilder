import json
from nose.tools import assert_raises, with_setup
from os import mkdir, remove
from os.path import exists
from shutil import copytree, rmtree

from manage import add_option


def setup():
    with open("pkg_info.json", 'w') as f:
        json.dump({}, f)


def teardown():
    if exists('pkg_info.json'):
        remove('pkg_info.json')


@with_setup(setup, teardown)
def test_add_already_existing_option_raises_warning():
    add_option('base', extra={'pkg_fullname': 'toto'})
    assert_raises(UserWarning, lambda: add_option('base'))


@with_setup(setup, teardown)
def test_add_non_existing_option_raises_warning():
    assert_raises(KeyError, lambda: add_option('toto'))


@with_setup(setup, teardown)
def test_add_option_bad_config_raises_warning():
    copytree("base", 'opt_toto/base')
    mkdir("opt_toto/option")
    mkdir("opt_toto/option/badtest")
    with open("opt_toto/option/badtest/config.py", 'w') as f:
        f.write("print 'bla'")
        f.close()

    assert_raises(SyntaxError, lambda: add_option('badtest', repo="opt_toto"))

    rmtree("opt_toto")


@with_setup(setup, teardown)
def test_add_option_pass_environment_to_config():
    assert_raises(UserWarning, lambda: add_option('test1'))


@with_setup(setup, teardown)
def test_add_option_register():
    add_option('base', extra={'pkg_fullname': 'toto'})
    add_option('test1')

