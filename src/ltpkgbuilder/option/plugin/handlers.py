from ltpkgbuilder.local import src_dir

from .tools import find_plugins


def setup(txt, env):
    """ Find all objects defined as plugins and install them
    as entry points
    """
    # walk all files:
    pkg_dir = src_dir(env)

    entry_points = find_plugins(pkg_dir)

    entry_points_msg = ["entry_points={"]
    for gr, pgs in entry_points.items():
        entry_points_msg.append(" " * 8 + "'%s': [" % gr)
        for plugin in pgs:
            name = plugin.split(":")[-1]
            entry_points_msg.append(" " * 12 + "'%s = %s'," % (name, plugin))
        entry_points_msg.append(" " * 8 + "],")
    entry_points_msg.append(" " * 4 + "},")

    return "\n".join(entry_points_msg)


mapping = {"plugin.setup": setup}
