#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This Setup script has been generated automatically
# do not modify

from setuptools import setup, find_packages


short_descr = "$project_short_description"
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = open("requirements.txt").read().split("\n")

test_requirements = [
    # TODO: put package test requirements here
]


# find version number in /src/$pkg_pth/version.py
version = {}
with open("src/$pkg_pth/version.py") as fp:
    exec(fp.read(), version)

url = 'https://github.com/$github_username/$pkg_pth'


setup(
    name='$pkg_name',
    version=version["__version__"],
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="$author_name",
    author_email='$author_email',
    url=url,
    license="Cecill-C",
    zip_safe=False,

    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={'': ['data']},

    install_requires=requirements,
    entry_points={
        # 'console_scripts': [
        #       'fake_script = openalea.fakepackage.amodule:console_script', ],
        # 'gui_scripts': [
        #      'fake_gui = openalea.fakepackage.amodule:gui_script',],
        #      'wralea': wralea_entry_points
    },

    keywords='$keywords',
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
