import json
from nose.tools import assert_raises, with_setup
from os import remove
from os.path import exists

from manage import add_option


def setup():
    with open("pkg_info.json", 'w') as f:
        json.dump({}, f)


def teardown():
    if exists('pkg_info.json'):
        remove('pkg_info.json')


@with_setup(setup, teardown)
def test_add_already_existing_option_raises_warning():
    add_option('base')
    assert_raises(UserWarning, lambda: add_option('base'))


@with_setup(setup, teardown)
def test_add_non_existing_option_raises_warning():
    assert_raises(KeyError, lambda: add_option('toto'))


@with_setup(setup, teardown)
def test_add_option_bad_config_raises_warning():
    assert_raises(SyntaxError, lambda: add_option('badtest'))


@with_setup(setup, teardown)
def test_add_option_pass_environment_to_config():
    assert_raises(UserWarning, lambda: add_option('test1'))


@with_setup(setup, teardown)
def test_add_option_register():
    add_option('base')
    add_option('test1')

