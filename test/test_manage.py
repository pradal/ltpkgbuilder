import mock
from nose.tools import assert_raises, with_setup
from os import mkdir
from os.path import exists
from hashlib import sha512
from shutil import rmtree

from ltpkgbuilder.versioning import get_local_version
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
    algo.update(("lorem ipsum\n" * 10).encode("latin1"))

    cfg = dict(simple=1,
               txt="lorem ipsum\n" * 4,
               hash=algo.digest().decode("latin1"))

    write_pkg_config(cfg, tmp_dir)

    new_cfg = get_pkg_config(tmp_dir)
    assert new_cfg == cfg

    algo = sha512()
    algo.update(("lorem ipsum\n" * 10).encode("latin1"))
    assert algo.digest() == new_cfg['hash'].encode("latin1")


def test_add_already_existing_option_raises_warning():
    pkg_cfg = add_option('base', {}, extra={'pkg_fullname': 'toto'})
    assert_raises(UserWarning, lambda: add_option('base', pkg_cfg))


def test_manage_update_pkg_do_nothing_if_up_to_date():
    pkg_cfg = update_pkg({})
    assert len(pkg_cfg) == 0


def test_manage_update_pkg_do_not_change_installed_options():
    ver = get_local_version()
    ver.version = (ver.version[0], ver.version[1] + 1, ver.version[2])

    pkg_cfg = {'base': dict(pkg_fullname='toto',
                            pkgname='toto',
                            namespace=None,
                            author_name='moi')}

    mem = dict(pkg_cfg['base'])

    with mock.patch("ltpkgbuilder.manage.get_github_version", return_value=ver):
        with mock.patch('ltpkgbuilder.option_tools.input', return_value=''):
            pkg_cfg = update_pkg(pkg_cfg)
            assert len(pkg_cfg) == 1
            assert pkg_cfg['base'] == mem


def test_manage_update_pkg_requires_user_input():
    ver = get_local_version()
    ver.version = (ver.version[0], ver.version[1] + 1, ver.version[2])

    pkg_cfg = {'base': dict(pkg_fullname='toto',
                            pkgname='toto',
                            namespace=None,
                            author_name='moi')}

    mem = dict(pkg_cfg['base'])

    with mock.patch("ltpkgbuilder.manage.get_github_version", return_value=ver):
        with mock.patch('ltpkgbuilder.option_tools.input', return_value='n'):
            pkg_cfg['toto'] = dict(option=None)
            pkg_cfg = update_pkg(pkg_cfg)
            assert len(pkg_cfg) == 2
            assert pkg_cfg['base'] == mem


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
    with mock.patch('ltpkgbuilder.option_tools.input', return_value=''):
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
