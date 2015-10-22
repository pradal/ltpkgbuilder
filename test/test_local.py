from nose.tools import assert_raises

from ltpkgbuilder.local import load_handlers


def test_load_handlers_fail_if_unknown_option():
    pkg_cfg = {'toto': {}}
    assert_raises(KeyError, lambda: load_handlers(pkg_cfg))


def test_load_handlers_load_functions_in_config_handlers():
    pkg_cfg = {'base': {}}
    h = load_handlers(pkg_cfg)
    assert 'upper' in h
