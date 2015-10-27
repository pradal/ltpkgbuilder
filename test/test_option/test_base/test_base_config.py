from nose.tools import assert_raises

from ltpkgbuilder.option.base.config import main


def test_base_config_handle_namespace():
    pkg_cfg = main({}, {'pkg_fullname': 'mypkg',
                        'author_name': 'moi',
                        'author_email': 'moi@mybox.com'})
    assert pkg_cfg['namespace'] is None
    assert pkg_cfg['pkgname'] == 'mypkg'

    pkg_cfg = main({}, {'pkg_fullname': 'myns.mypkg',
                        'author_name': 'moi',
                        'author_email': 'moi@mybox.com'})
    assert pkg_cfg['namespace'] == 'myns'
    assert pkg_cfg['pkgname'] == 'mypkg'


def test_base_config_check_pkg_names():
    for pkg in ('1mypkg', ' mypkg', '1', '1.mypkg',
                ' .mypkg', '.mypkg', 'None.mypkg', 'oa.o.mypkg'):
        assert_raises(UserWarning, lambda: main({}, {'pkg_fullname': pkg}))
