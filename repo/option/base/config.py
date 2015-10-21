def is_valid_identifier(name):
    """ Check that name is a valid python identifier
    sort of back port of "".isidentifier()
    """
    try:
        compile("%s=1" % name, "test", 'single')
        return True
    except SyntaxError:
        return False


def main(info, extra):
    try:
        pkg_fullname = extra["pkg_fullname"]
    except KeyError:
        pkg_fullname = raw_input("package full name:")

    if "." in pkg_fullname:
        try:
            namespace, pkgname = pkg_fullname.split(".")
        except ValueError:
            raise UserWarning("package name not valid: %s" % pkg_fullname)

        if not is_valid_identifier(namespace) \
                or not is_valid_identifier(pkgname):
            raise UserWarning("package name not valid: %s" % pkg_fullname)
    else:
        namespace = None
        pkgname = pkg_fullname
        if not is_valid_identifier(pkg_fullname):
            raise UserWarning("package name not valid: %s" % pkg_fullname)

    return dict(pkg_fullname=pkg_fullname,
                pkgname=pkgname,
                namespace=namespace,
                author_name='moi')
