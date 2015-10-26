""" Set of examples to explore most python package behaviour.

Documentation of the module
"""

import os


def example_func(txt="{{key, base.pkgname}}"):
    """Print txt message and return it.
    """
    print(txt)

    return txt


class ExampleClass(object):
    """Example class to show typical behaviour.
    """

    def __init__(self):
        self.repo_name = "{{key, base.pkgname}}"

    def txt(self):
        return self.repo_name


def main():
    ex = ExampleClass()
    print(ex.txt())
    print(os.getcwd())
