from ltpkgbuilder.rmtfile import get, ls


def test_rmtfile_ls():
    assert set(ls('data')) == {('base', True),
                               ('example', True),
                               ('test', True),
                               ('__init__.py', False),
                               ('__init__.pyc', False)}  # Bof, system dependent


def test_rmtfile_get():
    assert get('data/test/toto.txt').rstrip() == "lorem ipsum"
