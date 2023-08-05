About
-----

**debrepo** is a library for inspecting composes of Debian repositories and
their elements, including package archives. It includes classes capable of
reading compose, repository, and package data from the filesystem, and methods
to compare the data between different versions. To this end, the
:doc:`debrepodiff` tool provides a command line interface for comparing
composes.

Installation
------------

In the ``debrepo`` directory containing ``setup.py``, run:

.. code:: sh

   python setup.py install
