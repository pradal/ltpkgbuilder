Long Term Package Builder
=========================

At it simplest, a Python_ package is a mere directory with a '__init__.py' file
in it. However, this basic structure needs to be augmented as soon as more
functionality is required: i.e. create a distribution, write a comprehensive
documentation, run some tests. With time the structure of a package grows and
include more and more description files (e.g. setup.py, .gitignore, ...).

The rationale behind the creation of this 'package builder' is to keep the life
of a python programmer as easy as possible by providing two core functions:

 - a way to add more functionality to an existing package
 - a way to keep the package structure up to date with currently known best
   practices.

Quick start
-----------

Create a virtual environment for development::

    $ virtualenv dvlpt

Activate it::

    $ dvlpt/Scripts/activate

Install ltpkgbuilder_::

    (dvlpt)$ pip install ltpkgbuilder

Create a directory for your package::

    (dvlpt)$ mkdir toto

Run 'manage' inside this directory::

    (dvlpt)$ cd toto
    (dvlpt)$ manage init
    (dvlpt)$ manage add -opt base
    (dvlpt)$ manage regenerate

This will create the bare basic minimum for a python package. Add more options
(see `Add Package Structure Functionality`_ for more options) afterward.

Default minimalistic package comes with just a 'src' directory to put your code
in it :)

Upgrade Package Structure
-------------------------

Packages generated with Package Builder contains three different types of files:

 - 'pkg_cfg.json', a resource file that contains information entered by developers
   at some stage during the configuration phase of adding an option.
 - generated files, susceptible to be regenerated at any time or with version
   change and not meant to be modified by user. These files are generated
   automatically by the package builder using templates provided with the package.
 - developer data and modules edited by hand which contains the actual python
   code of the package independently of the structure of the package. ltpkgbuilder_
   will never touch them. If they conflict with some files used by a newly
   added option, the user will be prompted and will have to solve the conflict
   to install the option.

A call to the 'update' command will check for new versions of each structure
file, fetch the new template and instantiate it with the local meta info stored
in the package. If new meta info are required, the developer will be prompted
during the update. None of the files edited by the developer will be modified::

    (dvlpt)$ manage update

This command requires an internet connection since local installation will be
compared to current code on github.

If update is successful, a call to regenerate is mandatory to rebuilt the package
structural files::

    (dvlpt)$ manage regenerate

This phase will never overwrite files modified or created by user. In case of
conflicts it is the responsibility of the user to solve them and relaunch the
command.

Add Package Structure Functionality
-----------------------------------

Package Builder provide a set of addons to introduce new functionality to an
already existing package:

 - license: will help the developer to choose a license and add the relevant
   files
 - doc: Add some documentation to your package
 - test: basic unitests using nose
 - pydist: make your package distributable with setuptools (i.e. setup.py)
 - data: will guide through all the steps to add non python files to a package
 - github: will guide through all the step to safely store the package on Github_
 - tox: defines config files to use multi environment testing, Tox_
 - travis: will guide through all the steps to compile the code on Travis-CI_
 - coverage: add code coverage_ to the basic test configuration
 - lint: install and config tools to check for code compliance to python Flake8_
   guidelines.
 - pypi: step by step guide and configuration to upload package on PyPi_.
 - readthedocs: step by step guide to have your documentation on ReadTheDocs_

Extra services
--------------

.. warning::
    TODO

Package Builder also provides a few useful services to check that the python
modules follow code best practices:

 - 'add_object': will create a new python module with the proper headers and
   a skeleton of a python class.
 - 'add_plugin': will wrap a given python class into a usable plugin_.
 - 'add_script': will wrap a given python functionality into a command line
   script.
 - 'reset_file_header': will loop through all python modules and try to rewrite
   file header to match current best practices.
 - fmt_doc: check code documentation and format it according to given standard
   if possible. Requires some already good documentation, just a quick fix to
   pass from one style to another (e.g. google to numpy).


Contributing
------------

You can contribute to this package by:

 - improving the documentation
 - correcting some bugs
 - closing a few issues
 - implementing a new addon to add a new functionality to package structures


.. _ltpkgbuilder: https://github.com/revesansparole/ltpkgbuilder
.. _Python: http://python.org
.. _Travis-CI: http://travis-ci.org/
.. _Tox: http://testrun.org/tox/
.. _Sphinx: http://sphinx-doc.org/
.. _ReadTheDocs: https://readthedocs.org/
.. _Github: https://github.com/
.. _Nose:
.. _coverage:
.. _openalea:
.. _zope:
.. _Flake8:
.. _plugin: openalea.plugin
.. _PyPi:

