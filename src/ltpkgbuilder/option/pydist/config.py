from ltpkgbuilder.option_tools import ask_arg


def main(pkg_cfg, extra):
    description = ask_arg('dist.description',
                          pkg_cfg,
                          "belle petite description",
                          extra)

    keywords = ask_arg('keywords', pkg_cfg, None, extra)

    return dict(description=description,
                keywords=keywords)
