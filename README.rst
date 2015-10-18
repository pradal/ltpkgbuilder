Package Builder
===============

At it simplest, a Python_ package is a mere directory with a '__init__.py' file
in it. However, this basic structure needs to be augmented as soon as more
functionality is required: i.e. create a distribution, write a comprehensive
documentation, run some tests. With time the structure of a package grow and
include more and more description files (e.g. setup.py, .gitignore, ...).

The rationale behind the creation of this 'package builder' is to keep the life
of a python programmer as easy as possible by providing two core functions:
 - a way to add more functionality to an existing package
 - a way to keep the package structure up to date with currently known best
   practices.

Quick start
-----------

Download the 'create_package.py' file, launch it and follow the step by step
instructions.

.. warning::

    Improve with virtualenv and step by step tutorial

Default minimalistic package comes with:
 * Free software: CeCILL-C license
 * Easy testing setup with Nose_ ('nosetests')
 * Sphinx_ docs: Documentation ready for generation with, for example, ReadTheDocs_

Upgrade Package Structure
-------------------------

Packages generated with Package Builder contains three different types of files:
 - resources files that contains information entered by developers at some stage
 - generated files, susceptible to be regenerated at any time or with version
   change and not meant to be modified by user. These files are generated
   automatically by the package builder using up to date templates stored on
   internet (or a local repository)
 - developer data and modules edited by hand which contains the actual python
   code of the package independently of the structure of the package.

A call to the 'upgrade' command will check for new versions of each structure
file, fetch the new template and instantiate it with the local meta info stored
in the package. If new meta info are required, the developer will be prompted
during the upgrade. None of the files edited by the developer will be modified::

    $ python manage.py upgrade

Alternatively, specifying a '-repository=pth' argument will provide an
alternative place to look for updates in case of bad internet connection.

Add Package Structure Functionality
-----------------------------------

Package Builder provide a set of addons to introduce new functionality to an
already existing package:
 - license: will help the developer to choose a license and add the relevant
            files
 - data: will guide through all the steps to add non python files to a package
 - github: will guide through all the step to safely store the package on Github_
 - tox: defines config files to use multi environment testing, Tox_
 - travis: will guide through all the steps to compile the code on Travis-CI_
 - coverage: add code coverage_ to the basic test configuration
 - namespace: add the package into a virtual namespace (e.g. openalea_, zope_)
 - lint: install and config tools to check for code compliance to python Flake8_
         guidelines.
 - pypi: step by step guide and configuration to upload package on PyPi_.

Add functionality in the package
--------------------------------

Package Builder also provides a few useful services to check that the python
modules follow code best practices:
 - 'add_object': will create a new python module with the proper headers and
                 a skeleton of a python class.
 - 'add_plugin': will wrap a given python class into a usable plugin_.
 - 'add_script': will wrap a given python functionality into a command line
                 script.
 - 'reset_file_header': will loop through all python modules and try to rewrite
                        file header to match current best practices.


Contributing
------------

You can contribute to this package by:
 - improving the documentation
 - correcting some bugs
 - closing a few issues
 - implementing a new addon to add a new functionality to package structures


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

