from nose import with_setup
from os import remove
from os.path import exists

from manage_tools import user_modified, write_file


pth = "krakoukas.txt"


def teardown():
    if exists(pth):
        remove(pth)


@with_setup(teardown=teardown)
def test_tools_hash_newly_created_file_not_user_modified():
    content = "loren ipsum\n" * 10
    hashmap = {}

    write_file(pth, content, hashmap)

    assert not user_modified(pth, hashmap)

