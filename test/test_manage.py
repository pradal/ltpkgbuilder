import mock
from nose.tools import assert_raises, with_setup
from os import mkdir
from os.path import exists
from hashlib import sha512
from shutil import rmtree

from ltpkgbuilder.manage import (get_pkg_config,
                                 init_pkg,
                                 regenerate,
                                 add_option, update_option, edit_option,
                                 update_pkg,
                                 write_pkg_config)


tmp_dir = 'toto_local'


def setup():
    if not exists(tmp_dir):
        mkdir(tmp_dir)


def teardown():
    if exists(tmp_dir):
        rmtree(tmp_dir)


@with_setup(setup, teardown)
def test_manage_init_create_pkg_config():
    init_pkg(tmp_dir)
    cfg = get_pkg_config(tmp_dir)
    assert 'hash' in cfg


@with_setup(setup, teardown)
def test_manage_pkg_config():
    cfg = {'toto': 1}
    write_pkg_config(cfg, tmp_dir)
    new_cfg = get_pkg_config(tmp_dir)
    assert new_cfg == cfg


@with_setup(setup, teardown)
def test_manage_cfg_store_any_item():
    algo = sha512()
    algo.update("lorem ipsum\n" * 10)

    cfg = dict(simple=1,
               txt="lorem ipsum\n" * 4,
               hash=algo.digest().decode("latin1"))

    write_pkg_config(cfg, tmp_dir)

    new_cfg = get_pkg_config(tmp_dir)
    assert new_cfg == cfg

    algo = sha512()
    algo.update("lorem ipsum\n" * 10)
    assert algo.digest() == new_cfg['hash'].encode("latin1")


def test_add_already_existing_option_raises_warning():
    pkg_cfg = add_option('base', {}, extra={'pkg_fullname': 'toto'})
    assert_raises(UserWarning, lambda: add_option('base', pkg_cfg))


def test_manage_update_pkg():
    assert not update_pkg({})  # TODO


def test_manage_update_opt_raise_error_if_not_already_installed():
    pkg_cfg = {}
    assert_raises(UserWarning, lambda: update_option('base', pkg_cfg))


def test_manage_update_same_opt_do_not_change_anything():
    pkg_cfg = {'hash': {}}
    pkg_cfg = add_option('base', pkg_cfg, {"pkg_fullname": 'toto'})

    mem = dict(pkg_cfg['base'])
    pkg_cfg = update_option('base', pkg_cfg)
    assert mem == pkg_cfg['base']


def test_manage_edit_opt_raise_error_if_not_already_installed():
    pkg_cfg = {}
    assert_raises(UserWarning, lambda: edit_option('base', pkg_cfg))


def test_manage_edit_opt_with_defaults_do_not_change_anything():
    pkg_cfg = {'hash': {}}
    pkg_cfg = add_option('base', pkg_cfg, {"pkg_fullname": 'toto'})

    mem = dict(pkg_cfg['base'])
    with mock.patch('__builtin__.raw_input', return_value=''):
        pkg_cfg = edit_option('base', pkg_cfg)
        assert mem == pkg_cfg['base']


@with_setup(setup, teardown)
def test_regenerate():
    pkg_cfg = {'doc': {}, 'hash': {}}
    regenerate(pkg_cfg, tmp_dir)
    assert True  # TODO


@with_setup(setup, teardown)
def test_regenerate_raise_error_if_tempered_files():
    pkg_cfg = {'doc': {}, 'hash': {}}
    regenerate(pkg_cfg, tmp_dir)

    with open(tmp_dir + "/doc/info.rst", 'w') as f:
        f.write("tempered")

    assert_raises(UserWarning, lambda: regenerate(pkg_cfg, tmp_dir))
