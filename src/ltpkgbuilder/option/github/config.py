from ltpkgbuilder.option_tools import ask_arg


def main(pkg_cfg, extra):
    user = ask_arg("github.user", pkg_cfg, "revesansparole", extra)
    project = ask_arg("github.project",
                      pkg_cfg,
                      pkg_cfg['base']['pkgname'],
                      extra)

    return dict(user=user,
                project=project)
