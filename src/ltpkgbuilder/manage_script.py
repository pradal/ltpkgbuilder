from argparse import ArgumentParser

from local import installed_options
from manage import (clean, get_pkg_config,
                    init_pkg,
                    regenerate,
                    add_option, update_option, update_pkg,
                    write_pkg_config)


def main():
    parser = ArgumentParser(description='Package structure manager')
    parser.add_argument('action', metavar='action',
                        help="action to perform on package")

    parser.add_argument('-opt', '--option', metavar='option_name',
                        help="argument for action=add")

    args = parser.parse_args()

    if args.action == 'init':
        print "init package"
        init_pkg()
    elif args.action == 'clean':
        clean()
    elif args.action == 'update':
        pkg_cfg = get_pkg_config()
        if args.option is None:
            print "update package"
            pkg_cfg = update_pkg(pkg_cfg)
        elif args.option == 'all':
            print "update all options"
            for name in installed_options(pkg_cfg):
                pkg_cfg = update_option(name, pkg_cfg)
        else:
            print "update option"
            pkg_cfg = update_option(args.option, pkg_cfg)
        write_pkg_config(pkg_cfg)
    elif args.action == 'regenerate':
        print "regenerate"
        pkg_cfg = get_pkg_config()
        regenerate(pkg_cfg)
        write_pkg_config(pkg_cfg)
    elif args.action == 'add':
        pkg_cfg = get_pkg_config()
        pkg_cfg = add_option(args.option, pkg_cfg)
        write_pkg_config(pkg_cfg)
    else:
        print "unknown"


if __name__ == '__main__':
    main()
