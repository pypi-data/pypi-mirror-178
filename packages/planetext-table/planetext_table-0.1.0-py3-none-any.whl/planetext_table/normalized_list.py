from typing import Callable, Any, Type, Union, Optional

from enum import Enum
import copy
import unicodedata


class Align(Enum):
    """text alignment in element"""
    NONE = 0
    LEFT = 1
    CENTER = 2
    RIGHT = 3


class NormalizedList:
    """normalize list

       1. Convert to no-jagged list (Match the row with the largest number of elements)
       2. Make all elements of type str
    """
    # inner data
    data: list[list[str]]
    # list size
    rows: int
    cols: int
    # internal newline character
    newline: str
    # width of each columns
    widths: list[int]
    # text alignment of each column
    aligns: list[Align]

    def __init__(self, data: list[list[Any]],
                 converters: Optional[list[tuple[Union[Type, tuple[Type]], Callable[[Any], str]]]] = None,
                 newline: str = '\n',
                 padding: str = ' ',
                 aligns: Optional[list[Align]] = None) -> None:
        """Constructor

        Args:
            data (_AnyList): Input list data
            converters: List of type and converter pairs
                          e.g.)
                            --------------------------------
                             type                converter
                            --------------------------------
                             [(int,              int2str),
                              ((date, datetime), date2str)]
                            --------------------------------

            newline (str): internal newline character
            padding (str): padding to be added to both ends of an element
            aligns (list[Align]): text alignment of each column
        """
        if not data:
            data = [[]]

        # save newline character
        self.newline = newline

        # find the largest number of elements from all rows
        cols = max([len(row) for row in data])

        # convert to no-jagged list
        new_data = copy.deepcopy(data)
        for row in new_data:
            row.extend([''] * (cols - len(row)))

        # convert type str all element
        # and unify newline character code
        def convert(elem):
            elem = self._convert_str(elem, converters)
            elem = self._unify_lf(elem, newline)
            elem = self._add_padding(elem, padding, newline)
            return elem
        new_data = [[convert(elem) for elem in row] for row in new_data]

        # convert to no-jagged list
        for row in new_data:
            row.extend([''] * (cols - len(row)))

        # finish normalizing
        self.data = new_data

        # list size
        self.rows = len(self.data)
        self.cols = cols

        # text alignments
        if not aligns:
            aligns = []
        aligns.extend([Align.NONE] * (cols - len(aligns)))
        self.aligns = aligns

        # count width of each columns
        self.widths = [0] * self.cols
        for row in self.data:
            for i, elem in enumerate(row):
                self.widths[i] = max(self.widths[i], self._calc_width(elem, newline))

    @staticmethod
    def _calc_width(text: str, newline: str) -> int:
        """Calculate the width of a element containing full-width characters

        Args:
            text (str): target text
            newline (str): newline character

        Returns:
            int: width
        """
        # split text with newline character
        if newline in ('\r', '\n', '\r\n'):
            texts = text.split(newline)
        else:
            texts = [text]

        # calc width
        width = 0
        for t in texts:
            w = 0
            for char in t:
                w += 2 if unicodedata.east_asian_width(char) in 'FWAN' else 1
            width = max(width, w)
        return width

    @staticmethod
    def _unify_lf(text: str, newline: str) -> str:
        """unify newline character

        Args:
            text (str): target text
            newline (str): newline character

        Returns:
            str: operated text
        """
        return text.replace('\r\n', newline).replace('\r', newline).replace('\n', newline)

    @staticmethod
    def _add_padding(text: str, padding: str, newline: str) -> str:
        """add paddings to both ends of an element

        Args:
            text (str): target text
            padding (str): padding character
            newline (str): newline character

        Returns:
            str: operated text
        """

        # split text with newline character
        if newline in ('\r', '\n', '\r\n'):
            texts = text.split(newline)
        else:
            texts = [text]

        # add padding
        new_texts = []
        for t in texts:
            # If empty string, one padding only
            if len(t) == 0:
                t = padding
            else:
                t = padding + t + padding
            new_texts.append(t)
        return newline.join(new_texts)

    @staticmethod
    def _convert_str(value: Any,
                     converters: Optional[list[tuple[Union[Type, tuple[Type]], Callable[[Any], str]]]]) -> str:
        """convert any value to str

        Args:
            value (Any): target value
            converters: List of type and converter pairs
        """
        if not converters:
            converters = []
        # Use the appropriate converter
        for types, converter in converters:
            if isinstance(value, types):
                return converter(value)
        # default: Use str()
        return str(value)

    def adjust_column_width(self, min_width: int = 0, with_align: bool = False) -> None:
        """adjust width of element to the max size for that column.

        Args:
            min_width (int): minimum width
            with_align (bool): apply alignment
        """
        padding = ' '
        for i, row in enumerate(self.data):
            new_row = []
            for elem, width, align in zip(row, self.widths, self.aligns):
                width = max(width, min_width)
                diff = width - self._calc_width(elem, self.newline)
                if not with_align:
                    align = Align.LEFT

                if align == Align.CENTER:
                    ldiff = (diff // 2)
                    rdiff = (diff // 2) + (diff % 2)
                elif align == Align.RIGHT:
                    ldiff = diff
                    rdiff = 0
                else:
                    ldiff = 0
                    rdiff = diff

                elem = (padding * ldiff) + elem + (padding * rdiff)
                new_row.append(elem)

            self.data[i] = new_row
