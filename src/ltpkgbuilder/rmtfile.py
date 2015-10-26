""" Set of function to work with resources that are located inside
this package data
"""

from pkg_resources import (Requirement, resource_isdir,
                           resource_listdir, resource_string)


req = Requirement.parse('ltpkgbuilder')


def get(file_name):
    """ Retrieve the content of a given filename
    located in the data part of this package.

    args:
     - filename (str): name of the file to read

    return:
     - (str): content of the file red in 'r' mode
    """
    return resource_string(req, file_name).decode("utf-8")


def ls(dir_name):
    """ List all files and directories in dir_name
    located in the data part of this package.

    args:
     - dir_name (str): name of the directory to walk

    return:
     - (list of (str, bool)): list the content of dir_name
                       without any specific order, items are
                       (entity_name, is_directory)
    """
    return [(n, resource_isdir(req, dir_name + "/" + n))
            for n in resource_listdir(req, dir_name)]
