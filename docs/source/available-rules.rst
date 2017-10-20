===============
Available Rules
===============

Below are a list of available rules that can be attached to a :class:`~sandpaper.sandpaper.SandPaper` instance.
All of these rules first must pass several optional filters discussed in :ref:`getting_started-rule-filters`.

**In the following examples of these rules the symbol □ represents whitespace.**

lstrip
------
A basic rule that strips all *left* whitespace from a value.

.. code-block:: python

   SandPaper().lstrip()


====== ======
Input  Output
====== ======
□□data data
====== ======


rstrip
------
A basic rule that strips all *right* whitespace from a value.

.. code-block:: python

   SandPaper().rstrip()


====== ======
Input  Output
====== ======
data□□ data
====== ======


strip
-----
A basic rule that strips *all* whitespace from a value.

.. code-block:: python

   SandPaper().strip()


====== ======
Input  Output
====== ======
□data□ data
====== ======


substitute
----------
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
--------------
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
--------------
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
