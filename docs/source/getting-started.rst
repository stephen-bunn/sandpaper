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
First things first, in order to normalize any data you have to create an instance of the :class:`~sandpaper.sandpaper.SandPaper` object to group together your normalization rules.

.. code-block:: python

   from sandpaper import SandPaper

   # for an explicitly named sandpaper instance
   my_sandpaper = SandPaper('my-sandpaper')

   # for an implicitly named sandpaper instance
   my_sandpaper = SandPaper()


.. _getting_started-chaining-rules:

Chaining Rules
''''''''''''''

Now that you have a :class:`~sandpaper.sandpaper.SandPaper` instance, you can start chaining in rules that should be applied in order to normalize the data.

.. tip:: For a full list of available rules, check out the list of rules `here <available-rules.html>`__.

Rule can be applied by simply chaining the ordered normalization processes directly off of a :class:`~sandpaper.sandpaper.SandPaper` isntance.

.. code-block:: python

   my_sandpaper.strip()

This will apply the :func:`~sandpaper.sandpaper.SandPaper.strip` rule to the ``my_sandpaper`` instance.
The way it is now, the ``my_sandpaper`` instance will strip all whitespace from all values (since no filters were given).

We can add another rule to ``my_sandpaper`` by simply calling it.

.. code-block:: python

   my_sandpaper.substitute(
      substitutes={
         r'FL': 'Florida',
         r'NC': 'North Carolina'
      },
      column_filter=r'state'
   )

This will apply the :func:`~sandpaper.sandpaper.SandPaper.substitute` rule to the ``my_sandpaper`` instance.

Since the :func:`~sandpaper.sandpaper.SandPaper.strip` rule has already been applied, stripping of all whitespace will occur before this rule is applied.
The :func:`~sandpaper.sandpaper.SandPaper.substitute` rule will substitute the regular expression matches ``FL`` and ``NC`` with the values ``Florida`` and ``North Carolina`` respectively only in the column matching the filter ``state``.


The current state of the ``my_sandpaper`` instance could have also been initialized in one go using the chaining feature that rules provide.

.. code-block:: python

   my_sandpaper = SandPaper('my-sandpaper')
      .strip()
      .substitute(
         substitutes={
            r'FL': 'Florida',
            r'NC': 'North Carolina'
         },
         column_filter=r'state'
      )

---

In order to run this :class:`~sandpaper.sandpaper.SandPaper` instance you need to call the :func:`~sandpaper.sandpaper.SandPaper.apply` method to a glob of files.

.. code-block:: python

   my_sandpaper.apply('~/data_*{01..99}.csv')


.. note:: We use fancy brace expansion in our glob evaluation!
   You can take very interesting glob shortcuts with brace expansion; which you can learn about `here <https://pypi.python.org/pypi/braceexpand>`__.

In this instance the whitespace stripping will be applied to all ``.csv`` files starting with ``data_`` and ending with a number between ``01`` and ``99``.
*However*, because :func:`~sandpaper.sandpaper.SandPaper.apply` is actually a generator, in order to run the normalization you need to iterate over the method call.

.. code-block:: python

   for output_filepath in my_sandpaper.apply('~/data_*{01..99}.csv'):
      print(output_filepath)


.. _getting_started-rule-filters:

Rule Filters
''''''''''''

An important thing to note about rules is that every value has to first pass several optional filters if the rule is to be applied to that value.

   ``column_filter`` : regex
      A regular expression filter applied to the column name of the value (*must have a match to pass*)

   ``value_filter`` : regex
      A regular expression filter applied to the value (*must have a match to pass*)

   ``callable_filter`` : callable
      A callable reference that is executed for each value (*must evaluate to true to pass*)

      .. note:: This callable should expect to receive the parameters ``record``, ``column`` in that order, as well as any specified rule kwargs.
         The callable should return a boolean value which is True if the rule should be applied, otherwise False.

These filters are processed in the order presented and are completely optional.
**If no filters are specified, then the rule is applied.**


.. _getting_started-saving-sandpapers:

Saving SandPapers
'''''''''''''''''

It is possible to export a :class:`~sandpaper.sandpaper.SandPaper` instance using the :func:`~sandpaper.sandpaper.SandPaper.export` function.
This exports the configuration of the intance to a `json <http://www.json.org>`__ format either to a provided filepath or to stdout.

.. code-block:: python

    # for exporting to a file
    my_sandpaper.export('/home/USER/my-sandpaper.json')
    # for writing the export to stdout
    my_sandpaper.export()


This exported format can be used to bootstrap a new :class:`~sandpaper.sandpaper.SandPaper` instance by providing the filepath where the exported data is stored to the :func:`~sandpaper.sandpaper.SandPaper.load` method.

.. code-block:: python

    new_sandpaper = SandPaper.load('/home/USER/my-sandpaper.json')
