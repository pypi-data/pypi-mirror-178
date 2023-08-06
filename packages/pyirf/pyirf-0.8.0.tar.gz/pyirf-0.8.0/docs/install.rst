.. _install:

Installation
============

``pyirf`` requires Python ≥3.7 and pip, plus the packages defined in
the ``setup.py``.

Core dependencies are

* ``numpy``
* ``astropy``
* ``scipy``

We provide an environment file for Anaconda or Miniconda users.

Installing a released version
-----------------------------

To install a released version, just install the ``pyirf`` package using

.. code-block:: bash

    pip install pyirf

or add it to the dependencies of your project.

Installing for development
--------------------------

If you want to work on pyirf itself, clone the repository and install the local
copy of pyirf in development mode.

The dependencies required to perform unit-testing and to build the documentation
are defined in ``extras`` under ``tests`` and ``docs`` respectively.

These requirements can also be enabled by installing the ``all`` extra:

.. code-block:: bash

    pip install -e '.[all]'  # or [docs,tests] to install them separately


You should isolate your pyirf development environment from the rest of your system.
Either by using a virtual environment or by using ``conda`` environments.
``pyirf`` provides a conda ``environment.yml``, that includes all dependencies:

.. code-block:: bash

   conda env create -f environment.yml
   conda activate pyirf
   pip install -e '.[all]'
