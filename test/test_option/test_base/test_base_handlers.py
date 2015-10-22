from ltpkgbuilder.option.base.handlers import upper, lower


def test_base_upper():
    assert upper("toto", {}) == "TOTO"


def test_base_lower():
    assert lower("ToTo", {}) == "toto"
