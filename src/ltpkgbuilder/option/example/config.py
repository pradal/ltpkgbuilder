from os.path import basename, exists

from ltpkgbuilder.file_management import write_file
from ltpkgbuilder.local import load_handlers
from ltpkgbuilder.option_tools import ask_arg
from ltpkgbuilder.rmtfile import get, ls
from ltpkgbuilder.templating import replace


def copy_dir(cur_src_pth, cur_dst_pth, handlers, pkg_cfg):
    """ Parse cur_src_pth assumed to be a directory
    in repository and regenerate all files in it
    copy regenerated files in cur_dst_pth.

    Function called recursively on sub directories

    Does not make any test on the existence of cur_dst_pth
    Does not create any directory

    TODO: copy of regenerate_dir, not DRY

    args:
     - cur_src_pth (str): current pth to look into
     - cur_dst_pth (str): mirror of cur_src_pth on destination
     - handlers (dict of func): associate keys to handler functions
     - pkg_cfg (dict of (str: dict)): more information to pass to handlers
    """
    if basename(cur_src_pth) == "src":
        if 'base' in pkg_cfg:
            # check for namespace directory
            namespace = pkg_cfg['base']['namespace']
            if namespace is not None:
                cur_dst_pth = cur_dst_pth + "/" + namespace

            # create pkgname directory in src
            pkgname = pkg_cfg['base']['pkgname']
            cur_dst_pth = cur_dst_pth + "/" + pkgname

    items = ls(cur_src_pth)
    for name, is_dir_type in items:
        if is_dir_type:
            new_name = replace(name, handlers, pkg_cfg)
            if new_name not in ("", "_"):
                dst_dir = cur_dst_pth + "/" + new_name
                if exists(dst_dir):
                    copy_dir(cur_src_pth + "/" + name,
                             dst_dir,
                             handlers,
                             pkg_cfg)
        else:
            new_name = replace(name, handlers, pkg_cfg)
            if (new_name.split(".")[0] != "_"
                  and new_name[-3:] not in ("pyc", "pyo")):
                src_content = get(cur_src_pth + "/" + name)
                new_src_content = replace(src_content, handlers, pkg_cfg)
                # overwrite file without any warning
                write_file(cur_dst_pth + "/" + new_name, new_src_content)


def main(pkg_cfg, extra):
    option = ask_arg("option_name", {}, "plugin", extra)

    # get handlers for this option only
    h = load_handlers(option)

    # get option examples
    # check tempering
    copy_dir("ltpkgbuilder_data/example", ".", h, pkg_cfg)

    return None
