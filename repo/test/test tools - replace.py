from manage_tools import replace


def remove(txt, env):
    return ""


def upper(txt, env):
    return txt.upper()


def use_env(txt, env):
    return env['toto']


def test_replace_handle_no_div():
    txt = "print 'toto'"
    new_txt = replace(txt, {}, None)
    assert txt == new_txt


def test_replace_handle_unknown_div_class():
    txt = """
print 'toto'
# {{,
print 'titi'
# }}
"""
    new_txt = replace(txt, {}, None)
    assert new_txt == "\nprint 'toto'\nprint 'titi'"


def test_replace_handle_non_commented_lines():
    txt = """
print 'toto'
{{,
print 'titi'
}}
"""
    new_txt = replace(txt, {}, None)
    assert new_txt == "\nprint 'toto'\nprint 'titi'"


def test_replace_handle_inline_div():
    txt = "print #{{, 'titi'}}"
    new_txt = replace(txt, {}, None)
    assert new_txt == "print 'titi'"


def test_replace_handle_nested_div():
    txt = "print '{{upper, titi {{, toto}} retiti}}'"
    handlers = {'upper': upper}
    new_txt = replace(txt, handlers, None)
    assert new_txt == "print 'TITI TOTO RETITI'"


def test_replace_handle_multi_class():
    txt = "print '{{toto upper, toto}}'"
    handlers = {'upper': upper}
    new_txt = replace(txt, handlers, None)
    assert new_txt == "print 'TOTO'"


def test_replace_handle_remove_class():
    txt = "print 'toto{{toto remove, titi}}'"
    handlers = {'upper': upper, 'remove': remove}
    new_txt = replace(txt, handlers, None)
    assert new_txt == "print 'toto'"


def test_replace_handle_existing_inferior_sign_in_file():
    txt = "print '<toto>'{{remove, titi}}"
    handlers = {'upper': upper, 'remove': remove}
    new_txt = replace(txt, handlers, None)
    assert new_txt == "print '<toto>'"


def test_replace_pass_env_to_handlers():
    txt = "print '{{use_env, }}'"
    handlers = {'use_env': use_env}
    new_txt = replace(txt, handlers, {'toto': 'new toto'})
    assert new_txt == "print 'new toto'"


def test_replace_preserve_indentation():
    txt = "print 'toto'\n\t# {{upper, toto}}"
    handlers = {'upper': upper}
    new_txt = replace(txt, handlers, None)
    print repr(new_txt)
    assert new_txt == "print 'toto'\n\tTOTO"
