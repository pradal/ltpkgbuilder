from ltpkgbuilder.rmtfile import get, ls


def test_rmtfile_ls():
    assert set(ls('ltpkgbuilder_data/test/test1')) == {('subtest', True),
                                          ('titi.txt', False)}


def test_rmtfile_get():
    assert get('ltpkgbuilder_data/test/toto.txt').rstrip() == "lorem ipsum"
