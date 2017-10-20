sandpaper
=========

Simplified table data normalization.

.. image:: https://readthedocs.org/projects/sandpaper/badge/?version=latest
:target: http://sandpaper.readthedocs.io/en/latest/?badge=latest
:alt: Documentation Status


Basic Usage
-----------

.. code:: python

    from sandpaper import SandPaper

    paper = SandPaper('my-sandpaper').strip(  # strip whitespace from column comment
        column_filter=r'comment'
    ).translate_text(                         # get group id from column group
        column_filter=r'group',
        from_regex=r'^group_(\d+)$',
        to_format='{0}'
    ).translate_date(                         # normalize date from column date
        column_filter=r'date',
        from_formats=['%Y-%m-%d', '%m-%d'],
        to_format='%c'
    )

    for result in s.apply('~/Downloads/exported_data.{1..3}.{csv,xls{,x}}'):
        # apply sandpaper rules to all files matching the brace expanded glob given
        print(result)

Available Rules
---------------

| Every rule has 3 pre-filters, ``column_filter``, ``value_filter``, and
  ``callable_filter`` which are evaluated before any rules are applied.
| Both ``column_filter`` and ``value_filter`` receive regular
  expressions that are evaluated against the column name and the value
  respectively before determining if the rules should be applied.

--------------

lstrip
''''''

*Strips all left whitespace from the value.*

The below example strips all left whitespace from a column ``comments``
where the text ``group`` is found in the value.

.. code:: python

    SandPaper().lstrip(column_filter=r'comments', value_filter=r'.*group.*')

rstrip
''''''

*Strips all right whitespace from the value.*

The below example strips all right whitespace from a column ``comments``
where the text ``group`` is found in the value.

.. code:: python

    SandPaper().rstrip(column_filter=r'comments', value_filter=r'.*group.*')

strip
'''''

*Strips all whitespace from the value.*

The below example strips all whitespace from a column ``comments`` where
the text ``group`` is found in the value.

.. code:: python

    SandPaper().strip(column_filter=r'comments', value_filter=r'.*group.*')

substitute
''''''''''

*Substitutes a matching regular expression with a value.*

The below example substitutes several badly named flags within the
``flag`` column with some good descriptions on what the field means.

.. code:: python

    SandPaper().substitute(column_filter=r'flag', substitutes={
        r'ZF': 'Zeta Field',
        r'BF': 'Beta Field',
        r'AF': 'Alpha Field',
        r'DF': 'Delta Field'
    })

translate\_text
'''''''''''''''

*Translates a matching regular expression to a given format.*

The below example will extract the id of the group within a
``group_<ID>`` format within the ``group`` column.

.. code:: python

    SandPaper().translate_text(
        column_filter=r'group',
        from_regex=r'.*group_(?P<group_id>\d+)$',
        to_format='{group_id}'
    )

translate\_date
'''''''''''''''

*Translates a greedily evaluated date to a given format.*

| The below example translates dates similar to the given formats
  ``%Y-%m-%d``, ``%Y/%m/%d`` and ``%m-%d`` with the format ``%c``.
| This rule is very greedy and is potentially wrong since it utilizes
  the `dateparser`_ module to guess the best datetime format.
| This rule should **always** specify a ``column_filter`` and is **recommended** to also specify a ``value_filter`` to better limit the formats to normalize.

.. code:: python

   SandPaper().translate_date(
       column_filter=r'date',
       from_formats=['%Y-%m-%d', '%Y/%m/%d', '%m-%d'],
       to_format='%c'
   )


.. _dateparser: https://dateparser.readthedocs.io/en/latest/
