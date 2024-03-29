import mock

from ltpkgbuilder.option_tools import ask_arg, get_key, get_user_permission


print(__file__)


def test_user_permission():
    with mock.patch('ltpkgbuilder.option_tools.loc_input', return_value=''):
        assert get_user_permission('action')

    with mock.patch('ltpkgbuilder.option_tools.loc_input', return_value='y'):
        assert get_user_permission('action')

    with mock.patch('ltpkgbuilder.option_tools.loc_input', return_value='n'):
        assert not get_user_permission('action')

    with mock.patch('ltpkgbuilder.option_tools.loc_input', return_value='N'):
        assert not get_user_permission('action')


def test_get_key():
    assert get_key('toto', {'toto': 'titi'}) == 'titi'


def test_get_key_nested():
    assert get_key('toto.titi', {'toto': {'titi': 'tata'}}) == 'tata'


def test_get_key_returns_none_for_unknown_key():
    assert get_key('tata', {'toto': {'titi': 'tata'}}) is None
    assert get_key('toto.tata', {'toto': {'titi': 'tata'}}) is None
    assert get_key('titi', {'toto': {'titi': 'tata'}}) is None


def test_ask_arg_do_not_prompt_user_if_value_in_extra():
    with mock.patch('ltpkgbuilder.option_tools.loc_input',
                    return_value='useless'):
        assert ask_arg('toto', None, None, {'toto': 1}) == 1


def test_ask_arg_find_default_in_pkg_cfg():
    with mock.patch('ltpkgbuilder.option_tools.loc_input', return_value=''):
        assert ask_arg('toto', {'toto': 1}) == '1'
        assert ask_arg('toto', {'titi': 1}) == ''
        assert ask_arg('toto') == ''


def test_ask_use_default_if_everything_fail_only():
    with mock.patch('ltpkgbuilder.option_tools.loc_input', return_value=''):
        assert ask_arg('toto', {'toto': 1}, 2) == '1'
        assert ask_arg('toto', {'titi': 1}, 2) == '2'


def test_ask_arg_user_bypass_default():
    with mock.patch('ltpkgbuilder.option_tools.loc_input',
                    return_value='myvalue'):
        assert ask_arg('toto', {'toto': 1}, 0, {}) == 'myvalue'
        assert ask_arg('toto', {}, 0, {}) == 'myvalue'
        assert ask_arg('toto') == 'myvalue'
