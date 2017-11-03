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
Currently SandPaper is on `PyPi <https://pypi.python.org/pypi/sandpaper/>`_ and can easily be installed through `pip <https://pypi.python.org/pypi/pip>`_!

.. code-block:: bash

   pip install sandpaper



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

   my_sandpaper.translate_text({
      r'FL': 'Florida',
      r'NC': 'North Carolina'
   }, column_filter=r'state')

This will apply the :func:`~sandpaper.sandpaper.SandPaper.translate_text` rule to the ``my_sandpaper`` instance.

Since the :func:`~sandpaper.sandpaper.SandPaper.strip` rule has already been applied, stripping of all whitespace will occur before this rule is applied.
The :func:`~sandpaper.sandpaper.SandPaper.translate_text` rule will substitute the regular expression matches ``FL`` and ``NC`` with the values ``Florida`` and ``North Carolina`` respectively only in the column matching the filter ``state``.


The current state of the ``my_sandpaper`` instance could have also been initialized in one go using the chaining feature that rules provide.

.. code-block:: python

   my_sandpaper = SandPaper('my-sandpaper')\
      .strip()\
      .translate_text({
         r'FL': 'Florida',
         r'NC': 'North Carolina'
      }, column_filter=r'state')

---

In order to run this :class:`~sandpaper.sandpaper.SandPaper` instance you need to call the :func:`~sandpaper.sandpaper.SandPaper.apply` method to a file.

.. code-block:: python

   my_sandpaper.apply('/path/to/input_file.csv', '/path/to/output_file.csv')


.. important:: If applying to ``.csv`` files, unnecessary quotations are implicitly removed as part of the reading and saving processes.
   Currently there is no way of disabling this... sorry 😞.

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

It is possible to export a :class:`~sandpaper.sandpaper.SandPaper` instance using the :func:`~sandpaper.sandpaper.SandPaper.__json__` function.
This exports the configuration of the intance to a dictionary which is suitable for `json <http://www.json.org>`__ serialization.

.. code-block:: python

    serialized = my_sandpaper.__json__()


This exported format can be used to bootstrap a new :class:`~sandpaper.sandpaper.SandPaper` instance by providing the serialization to the :func:`~sandpaper.sandpaper.SandPaper.from_json` method.

.. code-block:: python

    new_sandpaper = SandPaper.from_json(serialized)


.. important:: The json serialization does not store any information about callables.
   A ``UserWarning`` is raised during serialization if a callable is found.


.. _getting_started-limitations:

Limitations
-----------

Several limitations to the effectiveness of the reading and writing of normalized data still exist within this module.
These are described in the subsections below...


.. _getting_started-reading-as-records:

Reading as Records
''''''''''''''''''

In order to provide all of the lovely filtering (:ref:`getting_started-rule-filters`) that make specifying advanced normalization rules much easier, SandPaper reads rows of table type data in as records (:class:`collections.OrderedDict`).
This allows us to tie row entries to column names easily but unfortunately causes limitations on the format of data that can be properly read in.
The main limitation is that **table sheets with duplicate column names cannot be read properly**.

Because `pyexcel <https://pyexcel.readthedocs.io/en/latest/>`_ reads records as :class:`~collections.OrderedDict`, the last column with a duplicate name is the only column considered.

For example the following table data...

========= =========
my_column my_column
========= =========
1         2
3         4
========= =========

will only output the last ``my_column`` column (with values 2 and 4) in the resulting ``sanded`` data.
This is because the reading of the record first reads the first column and then overwrites it with the second column.

A fix for this issue is possible, however would cause a lot of refactoring and additional testing which (obviously) has not been done.


.. _getting_started-translating-dates:

Translating Dates
'''''''''''''''''

The :func:`~sandpaper.sandpaper.SandPaper.translate_date` rule is quite nifty, but also has a couple limitations that need to be considered.
We utilize the clever `arrow <https://arrow.readthedocs.io/en/latest/>`_ library to handle date parsing which can be greedy at times.

However, because this parsing can take a considerable amount of time (when executed for many many items) it is recommended to also specify at least a ``column_filter`` for all instances of the rule.
