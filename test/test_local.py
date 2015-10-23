from nose.tools import assert_raises

from ltpkgbuilder.local import load_handlers, installed_options


def test_installed_options_handle_hash_key():
    cfg = {'toto': {}, 'titi': None}
    assert set(installed_options(cfg)) == {'toto', 'titi'}

    cfg['hash'] = {}
    assert set(installed_options(cfg)) == {'toto', 'titi'}


def test_load_handlers_fail_if_unknown_option():
    pkg_cfg = {'toto': {}}
    assert_raises(KeyError, lambda: load_handlers(pkg_cfg))


def test_load_handlers_load_functions_in_config_handlers():
    pkg_cfg = {'base': {}}
    h = load_handlers(pkg_cfg)
    assert 'upper' in h
