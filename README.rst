
.. image:: docs/source/_static/logo.png
   :align: center

|

.. image:: https://img.shields.io/pypi/v/sandpaper.svg
   :target: https://pypi.org/project/sandpaper/
   :alt: PyPi Status

.. image:: https://img.shields.io/pypi/pyversions/sandpaper.svg
   :target: https://pypi.org/project/sandpaper/
   :alt: Supported Versions

.. image:: https://img.shields.io/pypi/status/sandpaper.svg
   :target: https://pypi.org/project/sandpaper/
   :alt: Release Status

.. image:: https://img.shields.io/github/license/stephen-bunn/sandpaper.svg
   :target: https://github.com/stephen-bunn/sandpaper/blob/master/LICENSE
   :alt: License

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

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
   :target: https://saythanks.io/to/stephen-bunn
   :alt: Say Thanks


Basic Usage
-----------

Learn more by reading the `documentation <https://sandpaper.readthedocs.io/en/latest/>`_!


.. code:: python

   from sandpaper import SandPaper

   paper = SandPaper('my-sandpaper')\
      .strip(                                  # strip whitespace from column comment
         column_filter=r'comment'
      )\
      .translate_text({                        # get group id from column group
         r'^group_(\d+)$': '{0}'
      }, column_filter=r'group')\
      .translate_date({                        # normalize date from column date
         '%Y-%m-%d': '%c',
         '%m-%d': '%c'
      }, column_filter=r'date')

   # apply sandpaper rules to a source file and write results to a target file
   paper.apply('/home/you/source.csv', '/home/you/target.csv')
