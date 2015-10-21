def main(info, extra):
    try:
        user_name = extra['user_name']
    except KeyError:
        user_name = raw_input("github user name [revesansparole]:")
        if user_name == "":
            user_name = "revesansparole"

    try:
        pkg_pth = extra['pkg_pth']
    except KeyError:
        pkg_pth = raw_input("github project name [%s]:" % info['base']['pkgname'])
        if pkg_pth == "":
            pkg_pth = info['base']['pkgname']

    return dict(user=user_name,
                pkg_pth=pkg_pth)
