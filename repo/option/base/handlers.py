def remove(txt, env):
    return ""


def delete(txt, env):
    return "_"


def upper(txt, env):
    return txt.upper()


def lower(txt, env):
    return txt.lower()


def key(txt, env):
    try:
        elms = txt.split(".")
        d = env
        for k in elms:
            d = d[k]

        return d
    except KeyError:
        return txt


handlers = {'remove': remove,
            'rm': remove,
            'del': delete,
            'upper': upper,
            'lower': lower,
            'key': key}
