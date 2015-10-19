from hashlib import sha512
from nose import with_setup
from os import remove
from os.path import exists

from manage_tools import get_info, write_info


def teardown():
    if exists("pkg_info.json"):
        remove("pkg_info.json")


@with_setup(teardown=teardown)
def test_tools_info_store_any_info():
    algo = sha512()
    algo.update("loren ipsum\n" * 10)

    info = dict(simple=1,
                txt="loren ipsum\n" * 4,
                hash=algo.digest().decode("latin1"))

    write_info(info)

    new_info = get_info()
    assert new_info == info

    algo = sha512()
    algo.update("loren ipsum\n" * 10)
    assert algo.digest() == new_info['hash'].encode("latin1")
