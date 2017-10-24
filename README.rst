sandpaper
=========

Simplified table data normalization.


.. image:: https://readthedocs.org/projects/sandpaper/badge/?version=latest
   :target: http://sandpaper.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://travis-ci.org/stephen-bunn/sandpaper.svg?branch=master
   :target: https://travis-ci.org/stephen-bunn/sandpaper
   :alt: Build Status

.. image:: https://codecov.io/gh/stephen-bunn/sandpaper/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/stephen-bunn/sandpaper
   :alt: Code Coverage

.. image:: https://requires.io/github/stephen-bunn/sandpaper/requirements.svg?branch=master
   :target: https://requires.io/github/stephen-bunn/sandpaper/requirements/?branch=master
   :alt: Requirements Status


Basic Usage
-----------

Learn more by reading the `documentation <https://sandpaper.readthedocs.io/en/latest/>`_!


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
