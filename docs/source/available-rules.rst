===============
Available Rules
===============

Below are a list of available rules that can be attached to a :class:`~sandpaper.sandpaper.SandPaper` instance.
All of these rules first must pass several optional filters discussed in :ref:`getting_started-rule-filters`.

**In the following examples of these rules the symbol □ represents whitespace.**

Value Rules
-----------

These rules are applied to every value that passes the specified rule filters documented in :ref:`getting_started-rule-filters`.

:func:`~sandpaper.sandpaper.SandPaper.lower`
''''''''''''''''''''''''''''''''''''''''''''
A basic rule that lowercases the text in a value.

.. code-block:: python

   SandPaper().lower()


====== ======
Input  Output
====== ======
DATa   data
====== ======


:func:`~sandpaper.sandpaper.SandPaper.upper`
''''''''''''''''''''''''''''''''''''''''''''
A basic rule that uppercases the text in a value.

.. code-block:: python

   SandPaper().upper()


====== ======
Input  Output
====== ======
daTa   DATA
====== ======


:func:`~sandpaper.sandpaper.SandPaper.capitalize`
'''''''''''''''''''''''''''''''''''''''''''''''''
A basic rule that capitalizes the text in a value.

.. code-block:: python

   SandPaper().capitalize()


====== ======
Input  Output
====== ======
daTa   Data
====== ======


:func:`~sandpaper.sandpaper.SandPaper.title`
''''''''''''''''''''''''''''''''''''''''''''
A basic rule that titlecases the text in a value.

.. code-block:: python

   SandPaper().title()


======= =======
Input   Output
======= =======
mY dAta My Data
======= =======


:func:`~sandpaper.sandpaper.SandPaper.lstrip`
'''''''''''''''''''''''''''''''''''''''''''''
A basic rule that strips all *left* whitespace from a value.

.. code-block:: python

   SandPaper().lstrip()


====== ======
Input  Output
====== ======
□□data data
====== ======


:func:`~sandpaper.sandpaper.SandPaper.rstrip`
'''''''''''''''''''''''''''''''''''''''''''''
A basic rule that strips all *right* whitespace from a value.

.. code-block:: python

   SandPaper().rstrip()


====== ======
Input  Output
====== ======
data□□ data
====== ======


:func:`~sandpaper.sandpaper.SandPaper.strip`
''''''''''''''''''''''''''''''''''''''''''''
A basic rule that strips *all* whitespace from a value.

.. code-block:: python

   SandPaper().strip()


====== ======
Input  Output
====== ======
□data□ data
====== ======


:func:`~sandpaper.sandpaper.SandPaper.translate_text`
'''''''''''''''''''''''''''''''''''''''''''''''''''''
A translation rule that translate regex matches to a specified format.

.. code-block:: python

   SandPaper().translate_text({
      r'group_(?P<group_id>\d+)$': '{group_id}'
   })


========= ==============
Input     Output
========= ==============
group_47  47
group_123 123
group_0   0
========= ==============


:func:`~sandpaper.sandpaper.SandPaper.translate_date`
'''''''''''''''''''''''''''''''''''''''''''''''''''''
A translation rule that translate greedily evaluated dates to a specified datetime format.

.. note:: This rule is very greedy and can potentailly evaluate dates incorrectly.
   It is **highly recommended** that at the very least a ``column_filter`` is supplied with this rule.

.. code-block:: python

   SandPaper().translate_date({
      '%Y-%m-%d': '%Y',
      '%Y-%m': '%Y',
      '%Y': '%Y'
   })

========== ==============
Input      Output
========== ==============
2017-01-32 2017
2017-01    2017
2017       2017
========== ==============


Record Rules
------------

These rules are applied to every record regardless to most rule filters documented in :ref:`getting_started-rule-filters`.

:func:`~sandpaper.sandpaper.SandPaper.add_columns`
''''''''''''''''''''''''''''''''''''''''''''''''''
Adds a column to every record.

The given dictionary should be a key value pairing where the key is a new column name and the paired value is either a callable, string, or other low level data type for the newly added column's value.
If the value is a callable it should expect to receive the record as the only parameter and should return the value desired for the newly added column.

.. code-block:: python

   import uuid

   def gen_uuid(record):
      return uuid.uuid4()

   SandPaper().add_columns({
      'uuid': gen_uuid
   })


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


:func:`~sandpaper.sandpaper.SandPaper.remove_columns`
'''''''''''''''''''''''''''''''''''''''''''''''''''''
Removes a column from every record.

.. code-block:: python

   SandPaper().remove_columns([
      'name'
   ])


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


:func:`~sandpaper.sandpaper.SandPaper.keep_columns`
'''''''''''''''''''''''''''''''''''''''''''''''''''''
Removes all other columns for every record.

.. code-block:: python

   SandPaper().keep_columns([
      'id',
      'name'
   ])


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
id name
== =====
1  hello
2  test
== =====


:func:`~sandpaper.sandpaper.SandPaper.rename_columns`
'''''''''''''''''''''''''''''''''''''''''''''''''''''
Renames a column for every record.

.. code-block:: python

   SandPaper().rename_columns([
      'old_name': 'new_name'
   ])


== ======== =====
Before
-----------------
id old_name value
== ======== =====
1  hello    world
2  test     table
== ======== =====

|

== ======== =====
After
-----------------
id new_name value
== ======== =====
1  hello    world
2  test     table
== ======== =====


:func:`~sandpaper.sandpaper.SandPaper.order_columns`
''''''''''''''''''''''''''''''''''''''''''''''''''''
Reorders columns from every record.

.. code-block:: python

   SandPaper().order_columns([
      'value',
      'name',
      'id'
   ])


== ===== =====
Before
--------------
id name  value
== ===== =====
1  hello world
2  test  table
== ===== =====

|

===== == =====
After
--------------
value id name
===== == =====
world 1  hello
table 2  test
===== == =====
