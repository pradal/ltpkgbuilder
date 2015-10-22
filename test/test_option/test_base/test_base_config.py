from nose.tools import assert_raises

from ltpkgbuilder.option.base.config import main


def test_base_config_handle_namespace():
    pkg_cfg = main({}, {'pkg_fullname': 'mypkg'})
    assert pkg_cfg['namespace'] is None
    assert pkg_cfg['pkgname'] == 'mypkg'

    pkg_cfg = main({}, {'pkg_fullname': 'myns.mypkg'})
    assert pkg_cfg['namespace'] == 'myns'
    assert pkg_cfg['pkgname'] == 'mypkg'


def test_base_config_check_pkg_names():
    assert_raises(UserWarning, lambda: main({}, {'pkg_fullname': '1mypkg'}))
    assert_raises(UserWarning, lambda: main({}, {'pkg_fullname': ' mypkg'}))
    assert_raises(UserWarning, lambda: main({}, {'pkg_fullname': '1'}))

    assert_raises(UserWarning, lambda: main({}, {'pkg_fullname': '1.mypkg'}))
    assert_raises(UserWarning, lambda: main({}, {'pkg_fullname': ' .mypkg'}))
    assert_raises(UserWarning, lambda: main({}, {'pkg_fullname': '.mypkg'}))
    assert_raises(UserWarning, lambda: main({}, {'pkg_fullname': 'None.mypkg'}))

    assert_raises(UserWarning, lambda: main({}, {'pkg_fullname': 'oa.o.mypkg'}))
