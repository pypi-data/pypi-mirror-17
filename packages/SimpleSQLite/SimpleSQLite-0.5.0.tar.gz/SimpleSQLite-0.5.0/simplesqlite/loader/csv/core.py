# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import csv

import six

from ..constant import TableNameTemplate as tnt
from ..interface import TableLoader
from .formatter import CsvTableFormatter


class CsvTableLoader(TableLoader):
    """
    Abstract class of CSV table loader.

    .. py:attribute:: header_list

        Attribute names of the table. Use the first line of
        the csv file as attribute list if header_list is empty.

    .. py:attribute:: delimiter

        A one-character string used to separate fields.
        Defaults to ``","``.

    .. py:attribute:: quotechar

        A one-character string used to quote fields containing
        special characters, such as the ``delimiter`` or ``quotechar``,
        or which contain new-line characters.
        Defaults to ``'"'``.

    .. py:attribute:: encoding

        Encoding of the CSV data.
    """

    def __init__(self, source):
        super(CsvTableLoader, self).__init__(source)

        self._csv_reader = None

        self.header_list = ()
        self.delimiter = ","
        self.quotechar = '"'
        self.encoding = "utf-8"

    @property
    def format_name(self):
        return "csv"

    def _to_data_matrix(self):
        from dataproperty.type import FloatTypeChecker

        return [
            [
                six.b(data).decode(self.encoding, "ignore")
                if not FloatTypeChecker(data).is_type() else data
                for data in row
            ]
            for row in self._csv_reader
        ]


class CsvTableFileLoader(CsvTableLoader):
    """
    Concrete class of CSV file loader.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(filename)s``.
    """

    def __init__(self, file_path=None):
        super(CsvTableFileLoader, self).__init__(file_path)

    def make_table_name(self):
        """
        |make_table_name|

            ===================  ==================================
            format specifier     value after the replacement
            ===================  ==================================
            ``%(filename)s``     filename (without extention)
            ``%(format_name)s``  ``csv``
            ``%(format_id)s``    unique number in the same format
            ``%(global_id)s``    unique number in all of the format
            ===================  ==================================

        :return: Table name.
        :rtype: str
        """

        return self._make_file_table_name()

    def load(self):
        """
        Load table data from a CSV file.

        :return:
            Loaded table data.
            Table name is determined by
            :py:meth:`~.CsvTableFileLoader.make_table_name`.
        :rtype: iterator of |TableData|
        :raises simplesqlite.loader.InvalidDataError:
            If the CSV data is invalid.

        .. seealso:: :py:func:`csv.reader`
        """

        self._validate()

        self._csv_reader = csv.reader(
            open(self.source, "r"),
            delimiter=self.delimiter, quotechar=self.quotechar)
        formatter = CsvTableFormatter(self._to_data_matrix())
        formatter.accept(self)

        return formatter.to_table_data()

    def _get_default_table_name_template(self):
        return tnt.FILENAME


class CsvTableTextLoader(CsvTableLoader):
    """
    Concrete class of CSV text loader.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(format_name)s%(format_id)s``.
    """

    def __init__(self, text):
        super(CsvTableTextLoader, self).__init__(text)

    def load(self):
        """
        Load table data from a CSV text.

        :return: Loaded table data.
        :rtype: iterator of |TableData|
        :raises simplesqlite.loader.InvalidDataError:
            If the CSV data is invalid.

        .. seealso::
            :py:func:`csv.reader`
            :py:meth:`~.CsvTableFileLoader.make_table_name`
        """

        self._validate()

        self._csv_reader = csv.reader(
            six.StringIO(self.source.strip()),
            delimiter=self.delimiter, quotechar=self.quotechar)
        formatter = CsvTableFormatter(self._to_data_matrix())
        formatter.accept(self)

        return formatter.to_table_data()

    def _get_default_table_name_template(self):
        return "{:s}{:s}".format(tnt.FORMAT_NAME, tnt.FORMAT_ID)
