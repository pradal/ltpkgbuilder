from nose.tools import assert_raises

from ltpkgbuilder.manage_tools import update_opt


def test_non_existing_option_raises_warning():
    assert_raises(KeyError, lambda: update_opt('toto', {}))


def test_option_pass_environment_to_config():
    pkg_cfg = update_opt('base', {}, extra={'pkg_fullname': 'toto'})
    assert 'base' in pkg_cfg


def test_option_register():
    pkg_cfg = update_opt('base', {}, extra={'pkg_fullname': 'toto'})
    pkg_cfg = update_opt('test', pkg_cfg)
    assert 'base' in pkg_cfg
    assert 'test' in pkg_cfg


def test_option_look_for_dependencies():
    extra = {"install_option_dependencies": True, "pkg_fullname": 'toto'}
    pkg_cfg = update_opt('test', {}, extra=extra)
    assert 'base' in pkg_cfg
    assert 'test' in pkg_cfg
