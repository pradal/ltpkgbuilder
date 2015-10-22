from hashlib import sha512


def get_revision(txt):
    """ Get file revision as defined locally by a single statement
    # rev =
    on a single line

    args:
     - txt (str): text content to parse
    """
    for line in txt.splitlines():
        if line.startswith("# rev = "):
            return int(line[8:].strip())

    return None


def write_file(pth, content, hashmap):
    """ Write the content of a file on a local path and
    register associated hash for further modification
    tests.

    args:
     - pth (str): path to the new created file
     - content (str): content to write on disk
     - hashmap (dict of (str: sha512)): mapping between
                 file path and hash keys
    """
    with open(pth, 'w') as f:
        f.write(content)

    algo = sha512()
    algo.update(content)
    hashmap[pth] = algo.digest().decode("latin1")


def user_modified(pth, hashmap):
    """ Check whether the file has been tempered by user
    according to a stored hash.

    args:
     - pth (str): full path to the file
     - hashmap (dict of pth: sha512): table of hash keys

    return:
     - False: if file do not have a hash or if stored hash
              is different equal stored one
     - True: if file hash is different from stored one
    """
    if pth not in hashmap:
        return False

    ref_hash = hashmap[pth]

    algo = sha512()
    with open(pth, 'r') as f:
        algo.update(f.read())

    new_hash = algo.digest().decode("latin1")
    return new_hash != ref_hash
