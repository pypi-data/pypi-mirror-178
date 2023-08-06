import datetime

from planetext_table.normalized_list import NormalizedList
from planetext_table.normalized_list import Align


def test_basic():
    input_data = [
        [1, 2, 33],
        [4, 5],
        [6, 777, 8, 9],
    ]
    output_data = [
        [' 1 ', ' 2 ', ' 33 ', ' '],
        [' 4 ', ' 5 ', ' ', ' '],
        [' 6 ', ' 777 ', ' 8 ', ' 9 '],
    ]
    nlist = NormalizedList(input_data)

    assert nlist.rows == 3
    assert nlist.cols == 4
    assert nlist.widths == [3, 5, 4, 3]
    assert nlist.aligns == [Align.NONE] * 4
    assert nlist.data == output_data


def test_full_width_char():
    input_data = [
        ['abc', 'xyz🌞', 'ＡＢＣ', '！＃％', '漢字'],
    ]
    output_data = [
        [' abc ', ' xyz🌞 ', ' ＡＢＣ ', ' ！＃％ ', ' 漢字 '],
    ]
    nlist = NormalizedList(input_data)

    assert nlist.widths == [5, 7, 8, 8, 6]
    assert nlist.data == output_data


def test_str_converter():
    input_data = [
        [datetime.datetime(2001, 2, 3, 4, 5, 6, 789), 100],
    ]
    output_data = [
        [' 2001/02/03 04:05:06.000789 ', ' 100 '],
    ]

    def datetime2str(d):
        return datetime.datetime.strftime(d, r'%Y/%m/%d %H:%M:%S.%f')

    converters = [(datetime.datetime, datetime2str)]
    nlist = NormalizedList(input_data, converters=converters)

    assert nlist.widths == [28, 5]
    assert nlist.data == output_data


def test_newline():
    input_data = [
        ['\n\n', 'bb\rbbb', 'ccc\ncc', 'dd\r\ndd'],
    ]
    output_data = [
        [' \n \n ', ' bb \n bbb ', ' ccc \n cc ', ' dd \n dd '],
    ]
    nlist = NormalizedList(input_data)

    assert nlist.widths == [1, 5, 5, 4]
    assert nlist.data == output_data

    input_data = [
        ['aaaa', 'bb\rbbb', 'ccc\ncc', 'dd\r\ndd'],
    ]
    output_data = [
        [' aaaa ', ' bb<br/>bbb ', ' ccc<br/>cc ', ' dd<br/>dd '],
    ]
    nlist = NormalizedList(input_data, newline='<br/>')

    assert nlist.widths == [6, 12, 12, 11]
    assert nlist.data == output_data


def test_padding():
    input_data = [
        ['aaa', 'bbbb', ''],
    ]
    output_data = [
        ['__aaa__', '__bbbb__', '__'],
    ]
    nlist = NormalizedList(input_data, padding='__')

    assert nlist.widths == [7, 8, 2]
    assert nlist.data == output_data


def test_aligns():
    input_data = [
        ['aaa', 'bbb', 'ccc', 'ddd', 'eee'],
        ['aaa', 'bbb'],
    ]
    nlist = NormalizedList(input_data, aligns=[Align.CENTER, Align.RIGHT])

    assert nlist.aligns == [Align.CENTER, Align.RIGHT,
                            Align.NONE, Align.NONE, Align.NONE]
