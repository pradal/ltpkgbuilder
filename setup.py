#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
from os.path import dirname
from setuptools import setup, find_packages


short_descr = "Manage python package structure"
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = open("requirements.txt").read().split("\n")

test_requirements = [
    # TODO: put package test requirements here
]


# find version number in /src/ltpkgbuilder/version.py
version = {}
with open("src/ltpkgbuilder/version.py") as fp:
    exec(fp.read(), version)

url = 'https://github.com/revesansparole/ltpkgbuilder'

# extra magic for data management since package_data does not seem to work
data_files = []


# def rel_pth(pth):
#     return pth[4:]
#
#
# def fetch_data_files(cur_dir):
#     data_files.append((rel_pth(cur_dir), glob("%s/*.*" % cur_dir)))
#
#     for dname in glob("%s/*/" % cur_dir):
#         fetch_data_files(dirname(dname))

base_pth = "src/ltpkgbuilder_data/"


def rel_pth(pth):
    return pth[len(base_pth):]


def fetch_data_files(cur_dir):
    data_files.extend(rel_pth(n) for n in glob("%s/*.*" % cur_dir))

    for dname in glob("%s/*/" % cur_dir):
        fetch_data_files(dirname(dname))

for dname in ("base", "example", "test"):
    fetch_data_files(base_pth + dname)


setup(
    name='ltpkgbuilder',
    version=version["__version__"],
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="revesansparole",
    author_email='revesansparole@gmail.com',
    url=url,
    license="Cecill-C",
    zip_safe=False,

    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={'ltpkgbuilder_data': data_files},
    # data_files=data_files,

    install_requires=requirements,
    entry_points={
        'console_scripts': [
              'manage = ltpkgbuilder.manage_script:main',
        ],
        # 'gui_scripts': [
        #      'fake_gui = openalea.fakepackage.amodule:gui_script',],
        #      'wralea': wralea_entry_points
    },

    keywords='package builder',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='test',
    tests_require=test_requirements
)
