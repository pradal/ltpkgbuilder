def main(info, extra):
    return dict(pkgname=extra.get("pkgname", 'mypkg').split(".")[-1],
                pkg_fullname=extra.get("pkgname", 'mypkg'),
                author_name='moi')
