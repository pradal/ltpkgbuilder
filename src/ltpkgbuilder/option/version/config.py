from ltpkgbuilder.option_tools import ask_arg


def main(pkg_cfg, extra):
    major = ask_arg("major", pkg_cfg, "0", extra)
    minor = ask_arg("minor", pkg_cfg, "1", extra)
    post = ask_arg("post", pkg_cfg, "0", extra)

    return dict(major=major, minor=minor, post=post)
