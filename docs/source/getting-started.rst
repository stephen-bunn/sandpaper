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

   my_sandpaper = SandPaper('my-sandpaper')\
      .strip()\
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

   for (output_filepath, output_statistics) in my_sandpaper.apply(
      '~/data_*{01..99}.csv'
   ):
      print(output_filepath)


.. important:: If applying to ``.csv`` files, unnecessary quotations are implicitly removed as part of the reading and saving processes.
   Currently there is no way of disabling this... sorry 😞.

.. _getting_started-rule-filters:

Rule Filters
''''''''''''

An important thing to note about rules is that every value has to first pass several optional filters if the rule is to be applied to that value.

   ``sheet_filter`` : regex
      A regular expression filter applied to the sheet name (*must have a match to pass*)

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
This exports the configuration of the intance to a `json <http://www.json.org>`__ format.

.. code-block:: python

    serialized = my_sandpaper.export()


This exported format can be used to bootstrap a new :class:`~sandpaper.sandpaper.SandPaper` instance by providing the serialization to the :func:`~sandpaper.sandpaper.SandPaper.load` method.

.. code-block:: python

    new_sandpaper = SandPaper.load(serialized)



.. _getting_started-be-explicit:

Be Explicit
-----------

Some rules have named arguments that are also required.
This may look strange to users familiar with the standard ``*args``, ``**kwargs`` function setup, but because of the way that rules are registered and executed, some rules required explicit usage of named paramters.
An example of this is the :func:`~sandpaper.sandpaper.SandPaper.substitute` rule.
This rule expects a named parameter ``substitutes``.

.. code-block:: python

   SandPaper().substitute(substitutes={
      r'KEY': 'VALUE'
   })


When applied this rule works as intended (mainly substituting the text ``KEY`` with ``VALUE``).
However, if the users specifies the ``substitute`` rule like the following:

.. code-block:: python

   SandPaper().substitute({
      r'KEY': 'VALUE'
   })

no error will be thrown right away.
However, when the user tries to apply the :class:`~sandpaper.sandpaper.SandPaper` instance a ``TypeError`` will be thrown saying the following:
::

   TypeError: substitute() missing 1 required positional argument: 'substitutes'
   substitute() missing 1 required positional argument: 'substitutes'


This is due to how the ``substitutes`` are stored as ``kwargs`` rather than ``args`` to the ``substitute`` function.

**TLDR:** *Be explicit with the parameters of all rules!*


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
We utilize the clever `dateparser <https://dateparser.readthedocs.io/en/latest/>`_ library to handle date parsing which can be greedy at times.
In order to counteract this greediness we specify the ``STRICT_PARSING`` setting in order to limit the format matching to only those provided to the :func:`~sandpaper.sandpaper.SandPaper.translate_date` rule.

However, because this parsing takes a considerable amount of time (when executed for many many items) it is recommended to also specify at least a ``column_filter`` for all instances of the rule.
