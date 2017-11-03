=========
Changelog
=========

All notable changes to `SandPaper <https://github.com/stephen-bunn/sandpaper/>`_ will be documented in this file.

The format is based on `Keep a Changelog <http://keepachangelog.com/en/1.0.0/>`_ and this project adheres to `Semantic Versioning <http://semver.org/spec/v2.0.0.html>`_.

*unreleased*
------------


`0.0.5`_ (*2017-11-03*)
-----------------------
* added enforcement for strict date parsing in ``translate_date`` rule
* added ``rename_columns`` and ``order_columns`` record rules
* fixed the naming of ``add_columns`` and ``remove_columns``
* fixed the messy structure of all rules (cleaner and more intuitive use)
* fixed documentation to match new rule structure
* fixed all existing tests to match new rule structure
* removed the ``substitute`` value rule (utilize ``translate_text`` instead)
* removed extraneous badges from README and documentation index


`0.0.4`_ (*2017-10-26*)
-----------------------
* added a better badge provider for PyPi package status
* added support for a ``sheet_filter`` applied to both value rules and record rules
* added precompilation of filter regexes before application
* added rule application statistics which is now returned from ``apply`` in a tuple (output_filepath, output_statistics,)
* removed callable filters causing exporting and loading errors (just ignoring callable filters for now)


`0.0.3`_ (*2017-10-25*)
-----------------------
* added more badges to documentation and the README
* fixed (hopefully) the building of documentation for readthedocs.io
* fixed README example with an example that acutally makes sense


`0.0.2`_ (*2017-10-24*)
-----------------------
* added even more badges to the README
* added documentation improvements (linking rules to function references)
* added several small improvements to the tests (better code coverage)


`0.0.1`_ (*2017-10-24*)
-----------------------
* added README formatting fixes for PyPi
* fixed the PyPi configuration issues in setup.py


`0.0.0`_ (*2017-10-24*)
-----------------------
* added the project's base structure (wish i could include change logs for prior structure updates)
* fixed the project's base structure for PY2 compatability


.. _0.0.5: https://github.com/stephen-bunn/sandpaper/releases/tag/v0.0.5
.. _0.0.4: https://github.com/stephen-bunn/sandpaper/releases/tag/v0.0.4
.. _0.0.3: https://github.com/stephen-bunn/sandpaper/releases/tag/v0.0.3
.. _0.0.2: https://github.com/stephen-bunn/sandpaper/releases/tag/v0.0.2
.. _0.0.1: https://github.com/stephen-bunn/sandpaper/releases/tag/v0.0.1
.. _0.0.0: https://github.com/stephen-bunn/sandpaper/releases/tag/v0.0.0
