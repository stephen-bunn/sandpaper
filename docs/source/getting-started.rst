===============
Getting Started
===============

This module provides basic table-type data normalization that I have personally needed in many different projects over the past couple years.
It allows the normalization of table data readable by the popular `pyexcel <https://pyexcel.readthedocs.io/en/latest/>`_ library (mainly ``.xlsx``, ``.xls``, and ``.csv`` files).

It uses the concept of rules which can be chained to form a cleaning processes for these files.
**This module has a lot of room for improvement**, but it gets the job done that I needed it to.
Hopefully I'll continue to contribute rules, features, and more clean functionality as I need it.


.. _getting_started-installation:

Installation
------------
Currently SandPaper is not present on `PyPi <https://pypi.org>`_, but it's super easy to install from the git repo!
Assuming you have `pip <https://pypi.python.org/pypi/pip>`_ (or **even better** `pipenv <https://docs.pipenv.org>`_) installed, you can install SandPaper using the following snippets.

.. code-block:: bash

   # if using pip
   pip install -e git+https://github.com/stephen-bunn/sandpaper.git
   # if using pipenv
   pipenv install -e git+https://github.com/stephen-bunn/sandpaper.git


Now that you have the package installed, you will have to run the ``setup.py`` script.

.. code-block:: bash

   python setup.py

.. _getting_started-usage:

Usage
-----
Using SandPaper is *fairly* simple and straightforward.
First things first, in order to normalize any data you have to create an instance of the SandPaper object to group together your normalization rules.

.. code-block:: python

   from sandpaper import SandPaper

   # for an explicitly named sandpaper instance
   my_sandpaper = SandPaper('my-sandpaper')

   # for an implicitly named sandpaper instance
   my_sandpaper = SandPaper()


Now that you have a SandPaper instance, you can start chaining in rules that should be applied in order to normalize the data.

.. tip:: For a full list of available rules, check out the list of rules `here <available-rules.html>`_.
