===============
Available Rules
===============

Below are a list of available rules that can be attached to a :class:`~sandpaper.sandpaper.SandPaper` instance.
All of these rules first must pass several optional filters discussed in :ref:`getting_started-rule-filters`.

**In the following examples of these rules the symbol □ represents whitespace.**

Value Rules
-----------

These rules are applied to every value that passes the specified rule filters documented in :ref:`getting_started-rule-filters`.

lower
'''''
A basic rule that lowercases the text in a value.

.. code-block:: python

   SandPaper().lower()


====== ======
Input  Output
====== ======
DATa   data
====== ======


upper
'''''
A basic rule that uppercases the text in a value.

.. code-block:: python

   SandPaper().upper()


====== ======
Input  Output
====== ======
daTa   DATA
====== ======


capitalize
''''''''''
A basic rule that capitalizes the text in a value.

.. code-block:: python

   SandPaper().capitalize()


====== ======
Input  Output
====== ======
daTa   Data
====== ======


title
'''''
A basic rule that titlecases the text in a value.

.. code-block:: python

   SandPaper().title()


======= =======
Input   Output
======= =======
mY dAta My Data
======= =======


lstrip
''''''
A basic rule that strips all *left* whitespace from a value.

.. code-block:: python

   SandPaper().lstrip()


====== ======
Input  Output
====== ======
□□data data
====== ======


rstrip
''''''
A basic rule that strips all *right* whitespace from a value.

.. code-block:: python

   SandPaper().rstrip()


====== ======
Input  Output
====== ======
data□□ data
====== ======


strip
'''''
A basic rule that strips *all* whitespace from a value.

.. code-block:: python

   SandPaper().strip()


====== ======
Input  Output
====== ======
□data□ data
====== ======


substitute
''''''''''
A substitution rule that replaces regex matches with specified values.

.. code-block:: python

   SandPaper().substitute(
      substitutes={
         r'FL': 'Florida',
         r'NC': 'North Carolina'
      }
   )


====== ==============
Input  Output
====== ==============
FL     Florida
NC     North Carolina
====== ==============


translate_text
''''''''''''''
A translation rule that translate regex matches to a specified format.

.. code-block:: python

   SandPaper().translate_text(
      from_regex=r'group_(?P<group_id>\d+)$',
      to_format='{group_id}'
   )


========= ==============
Input     Output
========= ==============
group_47  47
group_123 123
group_0   0
========= ==============


translate_date
''''''''''''''
A translation rule that translate greedily evaluated dates to a specified datetime format.

.. note:: This rule is very greedy and can potentailly evaluate dates incorrectly.
   It is **highly recommended** that at the very least a ``column_filter`` is supplied with this rule.

.. code-block:: python

   SandPaper().translate_date(
      from_formats=['%Y-%m-%d', '%Y-%m', '%Y'],
      to_format='%Y'
   )


========== ==============
Input      Output
========== ==============
2017-01-32 2017
2017-01    2017
2017       2017
========== ==============


Record Rules
------------

These rules are applied to every record regardless of rule filters documented in :ref:`getting_started-rule-filters`.

add_column
''''''''''
Adds a column to every record.

The given ``column_value`` can either be a base type variable or a callable.
If the ``column_value`` is a callable it should expect to receive the record as the only parameter and should return the value desired for the newly added column.

.. note:: If the ``column_value`` is a string, the (key, value) pairs of the record are passed into the ``str.format`` method of the ``column_value``.

.. code-block:: python

   import uuid

   def gen_uuid(record):
      return uuid.uuid4()

   SandPaper().add_column(
      column_name='uuid',
      column_value=gen_uuid
   )


== ===== =====
Before
--------------
id name  value
== ===== =====
1  hello world
2  test  table
== ===== =====

|

== ===== ===== ====================================
After
---------------------------------------------------
id name  value uuid
== ===== ===== ====================================
1  hello world a6a76896-c33d-4654-afdf-12aa80dd6238
2  test  table b1e171c2-fee9-4270-96e9-4853c3a6e130
== ===== ===== ====================================


remove_column
'''''''''''''
Removes a column from every record.

.. code-block:: python

   SandPaper().remove_column(
      column_name='name'
   )


== ===== =====
Before
--------------
id name  value
== ===== =====
1  hello world
2  test  table
== ===== =====

|

== =====
After
--------
id value
== =====
1  world
2  table
== =====
