""" Some helpers for options
"""


def get_user_permission(action_name):
    return raw_input("%s [y], n?" % action_name) in ("", "y")


def get_key(key, env):
    """ Fetch a specific key in env
    """
    try:
        elms = key.split(".")
        d = env
        for k in elms:
            d = d[k]

        return d
    except KeyError:
        return None


def ask_arg(name, pkg_cfg=None, default=None, extra=None):
    """ Prompt the user for the value of some argument

    If user returns nothing then default will be returned

    If pkg_cfg is provided, the function will attempt to
    find a proper default in it.

    If extra is provided, the function will attempt to
    find a value in it and return it without prompting
    the user.

    args:
     - name (str): name of argument. Can be in the form of
                   'option.arg'.
     - pkg_cfg (dict of (str, any)): place to look for defaults
     - default (any): default to use as a last resort
     - extra (dict of (str, any)): place to look for values

    return:
     - (str): value of argument either from prompt or from default
    """
    if extra is None:
        extra = {}

    # try to find value in extra
    if name in extra:
        return extra[name]

    key = name.split(".")[-1]
    if key in extra:
        return extra[key]

    # prompt user for value
    if pkg_cfg is None:
        pkg_cfg = {}

    val = get_key(name, pkg_cfg)
    if val is None:
        val = default

    msg = name
    if val is None:
        msg += ":"
        val = ""
    else:
        val = str(val)
        msg += " [%s]:" % val

    ans = raw_input(msg)
    if ans == "":
        return val
    else:
        return ans
