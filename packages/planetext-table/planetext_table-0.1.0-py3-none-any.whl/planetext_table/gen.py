from typing import Callable, Any, Type, Union, Optional

import os
import io
import csv

from .normalized_list import NormalizedList, Align


def to_ascii(data: list[list[Any]], newline: str = '\n',
             internal_newline: str = '',
             aligns: Optional[list[Align]] = None,
             converters: Optional[list[tuple[Union[Type, tuple[Type]], Callable[[Any], str]]]] = None) -> str:
    """generate ascii table

    Args:
        data (list[list[Any]]): input list data
        newline (str): newline character at end of line
        internal_newline (str): newline character at inside element
        aligns (list[Align]): text alignment of each column
        converters: list of type and converter pairs
                    e.g.)
                    --------------------------------
                      type                converter
                    --------------------------------
                      [(int,              int2str),
                      ((date, datetime), date2str)]
                    --------------------------------
    """
    nl = NormalizedList(data, newline=internal_newline, aligns=aligns,
                        converters=converters)
    if nl.data == [[]]:
        return ''

    nl.adjust_column_width(min_width=3, with_align=True)

    def dline(row: list) -> str:
        """make data line"""
        return '|' + '|'.join(row) + '|' + newline

    def rline() -> str:
        """make ruler line"""
        row = []
        for width in nl.widths:
            elem = '-' * width
            row.append(elem)
        return '+' + '+'.join(row) + '+' + newline

    # to ascii
    text = rline()
    text += dline(nl.data[0])
    text += rline()
    if nl.data[1:]:
        for row in nl.data[1:]:
            text += dline(row)
        text += rline()
    return text


def to_csv(data: list[list[Any]], delimiter: str = ',', quotechar: Optional[str] = '"',
           newline: str = '\n', internal_newline: str = '\n',
           converters: Optional[list[tuple[Union[Type, tuple[Type]], Callable[[Any], str]]]] = None) -> str:
    """generate CSV table

    Args:
        data (list[list[Any]]): input list data
        delimiter (str): delimiter between elements
        quotechar (str): quote character at both ends of the element
        newline (str): newline character at end of line
        internal_newline (str): newline character at inside element
        converters: list of type and converter pairs
                    e.g.)
                    --------------------------------
                      type                converter
                    --------------------------------
                      [(int,              int2str),
                      ((date, datetime), date2str)]
                    --------------------------------

    Returns:
        str: CSV string
    """
    nl = NormalizedList(data, newline=internal_newline, padding='',
                        converters=converters)
    if nl.data == [[]]:
        return ''

    quoting = csv.QUOTE_ALL if quotechar else csv.QUOTE_NONE

    with io.StringIO(newline='') as stream:
        writer = csv.writer(stream, delimiter=delimiter, quotechar=quotechar,
                            quoting=quoting, lineterminator=newline)
        writer.writerows(nl.data)
        return stream.getvalue()


def to_markdown(data: list[list[Any]], newline: str = '\n',
                internal_newline: str = '<br/>',
                aligns: Optional[list[Align]] = None,
                converters: Optional[list[tuple[Union[Type, tuple[Type]], Callable[[Any], str]]]] = None) -> str:
    """generate markdown table

    Args:
        data (list[list[Any]]): input list data
        newline (str): newline character at end of line
        internal_newline (str): newline character at inside element
        aligns (list[Align]): text alignment of each column
        converters: list of type and converter pairs
                    e.g.)
                    --------------------------------
                      type                converter
                    --------------------------------
                      [(int,              int2str),
                      ((date, datetime), date2str)]
                    --------------------------------
    """
    nl = NormalizedList(data, newline=internal_newline, aligns=aligns,
                        converters=converters)
    if nl.data == [[]]:
        return ''

    nl.adjust_column_width(min_width=3)

    def dline(row: list) -> str:
        """make data line"""
        return '|' + '|'.join(row) + '|' + newline

    def rline() -> str:
        """make ruler line"""
        row = []
        for width, align in zip(nl.widths, nl.aligns):
            if align == Align.CENTER:
                elem = ':' + ('-' * (width - 2)) + ':'
            elif align == Align.RIGHT:
                elem = ('-' * (width - 1)) + ':'
            elif align == Align.LEFT:
                elem = ':' + ('-' * (width - 1))
            else:
                elem = '-' * width
            row.append(elem)
        return dline(row)

    # to markdown
    text = dline(nl.data[0])
    if nl.data[1:]:
        text += rline()
        for row in nl.data[1:]:
            text += dline(row)
    return text
