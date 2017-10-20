#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# MIT License <https://opensource.org/licenses/MIT>

import hashlib
import warnings
import functools
import collections

from . import (utils,)

import six
import path
import regex
import psutil
import pyexcel
import simplejson
from concurrent.futures import ThreadPoolExecutor


def rule(func):
    """ A meta wrapper for normalization rules.

    :param callable func: The normalization rule
    :returns: The wrapped normlaization rule
    :rtype: callable
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        self.rules.append((func, kwargs,))
        return self

    return wrapper


class SandPaper(object):
    """ The SandPaper object.

    Allows chained data normalization across multiple different table type
        data files such as ``.csv``, ``.xls``, and ``.xlsx``.
    """

    __default_apply = {
        'auto_detect_datetime': False
    }

    def __init__(self, name=None):
        """ Initializes the SandPaper object.

        .. note:: If a descriptive name is not provided, the name references a
            continually updating uid hash of the active rules.

        :param str name: The descriptive name of the SandPaper object
        """

        if name is not None:
            self.name = name

    def __repr__(self):
        """ Returns a string representation of a SandPaper instance.

        :returns: A string representation of a SandPaper instance
        :rtype: str
        """

        return (
            '<{self.__class__.__name__} ({rule_count} rules) "{self.name}">'
        ).format(rule_count=len(self.rules), **locals())

    def __hash__(self):
        """ Returns an identifying integer for the calling SandPaper instance.

        :returns: An identifying integer for the calling SandPaper instance
        :rtype: int
        """

        return int(self.uid, 16)

    @property
    def name(self):
        """ The descriptive name of the SandPaper instance.

        .. note:: If no name has been given, a continually updating uid hash
            of the active rules is used instead

        :getter: Returns the given or suitable name for a SandPaper instance
        :setter: Sets the descriptive name of the SandPaper instance
        :rtype: str
        """

        if not hasattr(self, '_name'):
            return self.uid
        return self._name

    @name.setter
    def name(self, name):
        """ Sets the descriptive name of the SandPaper instance.

        :param str name: A descriptive name for the SandPaper instance
        :returns: Nothing
        """

        assert isinstance(name, six.text_type) and len(name) > 0, (
            'name expected a string of positive length, received "{name}"'
        ).format(**locals())
        self._name = name

    @property
    def uid(self):
        """ A continually updating hash of the active rules.

        A hexadecimal digest string

        :getter: Returns a continually updating hash of the active rules
        :rtype: str
        """

        hasher = hashlib.md5()
        for (rule, rule_kwargs,) in self.rules:
            hasher.update((
                '{rule.__name__}({rule_kwargs})'
            ).format(**locals()).encode('utf-8'))
        return hasher.hexdigest()

    @property
    def rules(self):
        """ The set rules for the SandPaper instance.

        A list of tuples (rule_name, rule_arguments)

        :getter: Returns the set rules for the SandPaper instance
        :rtype: list[tuple(str, dict[str,....])]
        """

        if not hasattr(self, '_rules'):
            self._rules = []
        return self._rules

    @property
    def default_workers(self):
        """ The default amount of workers to use for processing multiple files.

        The current count of cpus as determined by ``psutil.cpu_count()``

        :getter: Returns the default amount of workers
        :rtype: int
        """

        return psutil.cpu_count()

    def _generate_filename(self, file_path, **kwargs):
        """ The default method for generating output filenames.

        :param path.Path file_path: An input Path instance
        :returns: A string filepath to save the processed results to
        :rtype: str
        """

        (base_path, base_ext,) = file_path.splitext()
        return (
            '{base_path}.sanded{base_ext}'
        ).format(**locals())

    def _filter_allowed(
        self, record,
        column_filter=None, value_filter=None, callable_filter=None,
        **kwargs
    ):
        """ Yield only allowed (column, value) pairs using filters.

        :param collections.OrderedDict record: An ordered dictionary of
            (``column_name``, ``row_value``) items
        :param str column_filter: A matched regular expression for
            ``column_name``
        :param str value_filter: A matched regular expression for ``row_value``
        :param callable callable_filter: An truthy evaluated callable
        :param dict kwargs: Any named arguments, for the kwargs of
            ``callable_filter``
        :returns: A generator yielding allowed (column, value) pairs
        """

        if isinstance(column_filter, six.string_types):
            column_filter = regex.compile(column_filter)
        if isinstance(value_filter, six.string_types):
            value_filter = regex.compile(value_filter)

        for (column, value) in record.items():

            if column_filter is not None:
                if not column_filter.match(str(column)):
                    continue
            if value_filter is not None:
                if not value_filter.match(str(value)):
                    continue
            if callable(callable_filter):
                if not callable_filter(record, column, **kwargs):
                    continue

            yield (column, value,)

    def _apply_rules(self, from_file, **kwargs):
        """ Base rule application method.

        :param str from_file: The file to apply rules to
        :param dict kwargs: Any named arguments, for the reading of the file
        :returns: Yields normalized records
        """

        for record in pyexcel.iget_records(
            file_name=from_file,
            **kwargs
        ):
            for (rule, rule_kwargs,) in self.rules:
                for (column, value,) in self._filter_allowed(
                    record,
                    **rule_kwargs
                ):
                    record[column] = \
                        rule(self, record.copy(), column, **rule_kwargs)
            yield record

    def _apply_to(self, from_file, to_file, **kwargs):
        """ Threadable rule processing method.

        .. important:: No overwrite protection is enabled for this method.
            If the ``from_file`` is equal to the ``to_file``, then
            ``from_file`` will be overwritten.

        :param str from_file: The input filepath
        :param str to_file: The output filepath
        :param dict kwargs: Any named arguments, passed to ``_apply_rules``
        :returns: The saved normalized filepath
        :rtype: str
        """

        pyexcel.isave_as(
            records=self._apply_rules(from_file, **kwargs),
            dest_file_name=to_file
        )
        return to_file

    @rule
    def lstrip(self, record, column, **kwargs):
        """ A basic lstrip rule for a given value.

        Only applies to text type variables.

        :param collections.OrderedDict record: A record whose value within
            ``column`` should be normalized and returned
        :param str column: A column that indicates what value to normalize
        :param dict kwargs: Any named arguments
        :returns: The value with left whitespace stripped
        """

        value = record[column]
        return (
            value.lstrip()
            if isinstance(value, six.text_type) else
            value
        )

    @rule
    def rstrip(self, record, column, **kwargs):
        """ A basic rstrip rule for a given value.

        Only applies to text type variables.

        :param collections.OrderedDict record: A record whose value within
            ``column`` should be normalized and returned
        :param str column: A column that indicates what value to normalize
        :param dict kwargs: Any named arguments
        :returns: The value with right whitespace stripped
        """

        value = record[column]
        return (
            value.rstrip()
            if isinstance(value, six.text_type) else
            value
        )

    @rule
    def strip(self, record, column, **kwargs):
        """ A basic strip rule for a given value.

        Only applies to text type variables.

        :param collections.OrderedDict record: A record whose value within
            ``column`` should be normalized and returned
        :param str column: A column that indicates what value to normalize
        :param dict kwargs: Any named arguments
        :returns: The value with all whitespace stripped
        """

        value = record[column]
        return (
            value.strip()
            if isinstance(value, six.text_type) else
            value
        )

    @rule
    def increment(
        self, record, column,
        amount,
        **kwargs
    ):
        """ A basic increment rule for a given value.

        Only applies to numeric (int, float) type variables.

        :param collections.OrderedDict record: A record whose value within
            ``column`` should be normalized and returned
        :param str column: A column that indicates what value to normalize
        :param amount: The amount to increment by
        :type amount: int or float
        :param dict kwargs: Any named arguments
        :returns: The value incremented by ``amount``
        """

        value = record[column]
        if isinstance(value, (int, float,)):
            return (value + amount)
        return value

    @rule
    def decrement(
        self, record, column,
        amount,
        **kwargs
    ):
        """ A basic decrement rule for a given value.

        Only applies to numeric (int, float) type variables.

        :param collections.OrderedDict record: A record whose value within
            ``column`` should be normalized and returned
        :param str column: A column that indicates what value to normalize
        :param amount: The amount to decrement by
        :type amount: int or float
        :param dict kwargs: Any named arguments
        :returns: The value incremented by ``amount``
        """

        value = record[column]
        if isinstance(value, (int, float,)):
            return (value - amount)
        return value

    @rule
    def substitute(
        self, record, column,
        substitutes,
        **kwargs
    ):
        """ A substitution rule for a given value.

        Take for example the following SandPaper instance:

        .. code-block:: python

            s = SandPaper('my-sandpaper').substitute(substitutes={
                r'^\d+.*$': 'STARTED WITH A NUMBER'
            })


        This will substitute all values that start with a number with the
        text ``STARTED WITH A NUMBER``.

        :param collections.OrderedDict record: A record whose value within
            ``column`` should be normalized and returned
        :param str column: A column that indicates what value to normalize
        :param substitutes: A dictionary of (regex, value,)
            substitute items for the value
        :type substitutes: dict[str, str]
        :param dict kwargs: Any named arguments
        :returns: The value potentially substituted by the substitutes
            dictionary
        """

        value = record[column]
        for (from_regex, to_value) in substitutes.items():
            if regex.match(from_regex, str(value)):
                return to_value
        return value

    @rule
    def translate_text(
        self, record, column,
        from_regex, to_format,
        **kwargs
    ):
        """ A text translation rule for a given value.

        Take for example the following SandPaper instance:

        .. code-block:: python

            s = SandPaper('my-sandpaper').translate_text(
                column_filter=r'^group_definition$',
                from_regex=r'^group(?P<group_id>\d+)\s*(.*)$',
                to_format='{group_id}'
            )


        This will translate all instances of the value
        ``group<GROUP NUMBER>`` to ``<GROUP NUMBER>`` only in columns named
        ``group_definition``.

        .. important:: Note that matched groups and matched groupdicts are
            passed as ``*args`` and ``**kwargs`` to the format method of the
            returned ``to_format`` string.

        :param collections.OrderedDict record: A record whose value within
            ``column`` should be normalized and returned
        :param str column: A column that indicates what value to normalize
        :param str from_regex: A value matched regex
        :param str to_format: A format for matched value translation
        :param dict kwargs: Any named arguments
        :returns: The value potentially translated value
        """

        value = record[column]
        match = regex.match(from_regex, str(value))
        if match is not None:
            return to_format.format(
                *match.groups(), **match.groupdict(),
                **kwargs
            )
        return value

    @rule
    def translate_date(
        self, record, column,
        from_formats, to_format,
        **kwargs
    ):
        """ A date translation rule for a given value.

        Take for example the following SandPaper instance:

        .. code-block:: python

            s = SandPaper('my-sandpaper').translate_date(
                column_filter=r'^(.*)_date$',
                from_formats=['%Y-%m-%d', '%m-%d'],
                to_format='%c'
            )


        This will translate all instances of a date value in columns ending
        with ``_date`` to the date format ``%c``, *prioritizing* the date
        formats described in ``from_formats``.

        .. important:: Note that the date evaluation is done through the
            `dateparser <https://dateparser.readthedocs.io/en/latest/>`_ module
            and greedily discovers date formats.

            This could lead to unexpected date changes. For this reason, it is
            implicitly required that at the very least a ``column_filter`` is
            used to filter what columns should be considered. The use of a
            ``value_filter`` would ensure even less false positive date
            evaluation.

        .. note:: Raises a UserWarning if the lack of a ``column_filter`` is
            detected.

        :param collections.OrderedDict record: A record whose value within
            ``column`` should be normalized and returned
        :param str column: A column that indicates what value to normalize
        :param list[str] from_formats: A list of prioritized date formats
        :param str to_format: A format for date format translation
        :param dict kwargs: Any named arguments
        :returns: The value potentially translated value
        """

        # NOTE: local import of dateparser, potentailly slow due to issue
        # https://github.com/scrapinghub/dateparser/issues/253
        import dateparser

        if 'column_filter' not in kwargs:
            warnings.warn((
                'translate_date usually does not function well without an '
                'explicit column_filter'
            ), UserWarning)
        value = record[column]
        parsed_date = dateparser.parse(
            str(value),
            date_formats=from_formats
        )
        if parsed_date is not None:
            return parsed_date.strftime(to_format)
        return value

    def apply(
        self, from_glob,
        max_workers=None, name_generator=None,
        **kwargs
    ):
        """ Applies a SandPaper instance rules to a given glob of files.

        .. important:: *You can use fancy brace expansion with this glob!*
            For example, the glob ``*.{csv,xls{,x}}`` will capture all files
            using the extensions ``csv``, ``xls``, and ``xlsx``!

            Learn more about this format from
            `here <https://pypi.python.org/pypi/braceexpand/0.1.1>`_!

        .. note:: The ``name_generator`` callable will be passed in a
            `path.Path <https://pathpy.readthedocs.io/en/latest/api.html>`_
            instance and expects to be returned an appropriate filepath
            as a string.

        .. note:: The default output filepaths simply prefix the input file's
            extension with the ``.sanded`` extension.

            For example, the filepath ``sample.xlsx`` will become
            ``sample.sanded.xlsx``.

        :param str from_glob: A matching glob for all desired files
        :param int max_workers: The maximum amount of files to process in
            parallel
        :param callable name_generator: A callable that
            generates output filepaths given the path.Path instance
        :returns: Yields output filepaths (not in any consistent order)
        """
        # TODO: add file metainfo to the kwargs
        from_glob = path.Path(from_glob).expand().abspath().normpath()
        futures = []
        try:
            # build a thread pool for processing files in parallel
            with ThreadPoolExecutor(max_workers=(
                max_workers
                if (
                    isinstance(max_workers, six.integer_types) and
                    max_workers > 0
                ) else
                self.default_workers
            )) as executor:
                for file_path in utils.fancy_glob(from_glob, fancy_path=True):
                    to_file = (
                        self._generate_filename
                        if not callable(name_generator) else
                        name_generator
                    )(file_path)
                    # start an async future for processing a file
                    futures.append(executor.submit(
                        self._apply_to,
                        *(str(file_path), to_file,),
                        **dict(self.__default_apply, **kwargs)
                    ))
            # yield evaluated future results
            for future in futures:
                yield future.result()
        finally:
            # NOTE: because pyexcel does some intersting memory manipulation
            # we need to free the resources allocted by the async processes
            pyexcel.free_resources()

    def export(self, to_file=None):
        """ Exports a serialization of the active rules.

        :param str to_file: The filepath to write the serialization to
        :raises ValueError:
            - if the parent directory of ``to_file`` does not exist
        :returns: ``to_file`` if specified, otherwise the serialization dict
        :rtype: str or dict[str,tuple(str,dict[str,....])]
        """

        serial = {
            self.name: [
                (rule.__name__, rule_kwargs)
                for (rule, rule_kwargs,) in self.rules
            ]
        }
        if to_file is not None:
            if not path.Path(to_file).parent.isdir():
                raise ValueError((
                    "parent directory of '{to_file}' does not exist"
                ).format(**locals()))
            with open(to_file, 'w') as fp:
                simplejson.dump(serial, fp)
            return to_file
        else:
            return serial

    @classmethod
    def load(cls, from_file):
        """ Creates a new SandPaper instance from an exported serialization.

        :param str from_file: The file where an exported serialization lives
        :raises ValueError:
            - if the given ``from_file`` cannot be found
        :returns: An SandPaper instance
        :rtype: SandPaper
        """

        if not path.Path(from_file).isfile():
            raise ValueError((
                "no such file '{from_file}' exists"
            ).format(**locals()))
        with open(from_file, 'r') as fp:
            exported_data = simplejson.load(fp)
            for (name, rules,) in exported_data.items():
                return cls(name, collections.OrderedDict(rules))
