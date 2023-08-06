import datetime

import planetext_table as pt


def datetime2str(d):
    return datetime.datetime.strftime(d, r'%Y/%m/%d %H:%M:%S.%f')


def test_empty_list():
    text = pt.to_ascii([])
    assert text == ''
    text = pt.to_csv([])
    assert text == ''
    text = pt.to_markdown([])
    assert text == ''


def test_one_line():
    text = pt.to_ascii([[1, 2, 3]])
    output = (
        '+---+---+---+\n'
        '| 1 | 2 | 3 |\n'
        '+---+---+---+\n'
    )
    assert text == output

    text = pt.to_csv([[1, 2, 3]])
    output = '"1","2","3"\n'
    assert text == output

    text = pt.to_markdown([[1, 2, 3]])
    output = '| 1 | 2 | 3 |\n'
    assert text == output


def test_ascii():
    input_data = [
        ['aaa', 'bbb', 'ccc'],
        ['aaa', 'bb\nb'],
        [11, datetime.datetime(2001, 2, 3, 4, 5, 6, 789)],
        ['ＦＵＬＬ', '全角', '＃＄％', '☀🌞'],
    ]

    # default args
    output_data = (
        '+----------+----------------------------+--------+------+\n'
        '| aaa      | bbb                        | ccc    |      |\n'
        '+----------+----------------------------+--------+------+\n'
        '| aaa      | bbb                        |        |      |\n'
        '| 11       | 2001-02-03 04:05:06.000789 |        |      |\n'
        '| ＦＵＬＬ | 全角                       | ＃＄％ | ☀🌞 |\n'
        '+----------+----------------------------+--------+------+\n'
    )
    text = pt.to_ascii(input_data)
    assert output_data == text

    # set args
    output_data = (
        '+----------+----------------------------+--------+------+\n'
        '| aaa      |            bbb             |    ccc |      |\n'
        '+----------+----------------------------+--------+------+\n'
        '| aaa      |            bb_b            |        |      |\n'
        '| 11       | 2001/02/03 04:05:06.000789 |        |      |\n'
        '| ＦＵＬＬ |            全角            | ＃＄％ | ☀🌞 |\n'
        '+----------+----------------------------+--------+------+\n'
    )
    aligns = [pt.Align.LEFT, pt.Align.CENTER, pt.Align.RIGHT]
    text = pt.to_ascii(input_data, newline='\n', internal_newline='_', aligns=aligns,
                       converters=[(datetime.datetime, datetime2str)])
    assert output_data == text


def test_csv():
    input_data = [
        ['aaa', 'bbb', 'ccc'],
        ['aaa', 'bb\nb'],
        [11, datetime.datetime(2001, 2, 3, 4, 5, 6, 789)],
        ['ＦＵＬＬ', '全角', '＃＄％', '☀🌞'],
    ]

    # default args
    output_data = (
        '"aaa","bbb","ccc",""\n'
        '"aaa","bb\nb","",""\n'
        '"11","2001-02-03 04:05:06.000789","",""\n'
        '"ＦＵＬＬ","全角","＃＄％","☀🌞"\n'
    )
    text = pt.to_csv(input_data)
    assert text == output_data

    # set args
    output_data = (
        'aaa\tbbb\tccc\t\n'
        'aaa\tbb\rb\t\t\n'
        '11\t2001/02/03 04:05:06.000789\t\t\n'
        'ＦＵＬＬ\t全角\t＃＄％\t☀🌞\n'
    )
    text = pt.to_csv(input_data, delimiter='\t', quotechar=None,
                     internal_newline='\r', newline='\n',
                     converters=[(datetime.datetime, datetime2str)])
    assert text == output_data


def test_markdown():
    input_data = [
        ['aaa', 'bbb', 'ccc'],
        ['aaa', 'bb\nb'],
        [11, datetime.datetime(2001, 2, 3, 4, 5, 6, 789)],
        ['ＦＵＬＬ', '全角', '＃＄％', '☀🌞'],
    ]

    # default args
    output_data = (
        '| aaa      | bbb                        | ccc    |      |\n'
        '|----------|----------------------------|--------|------|\n'
        '| aaa      | bb<br/>b                   |        |      |\n'
        '| 11       | 2001-02-03 04:05:06.000789 |        |      |\n'
        '| ＦＵＬＬ | 全角                       | ＃＄％ | ☀🌞 |\n'
    )
    text = pt.to_markdown(input_data)
    assert output_data == text

    # set args
    output_data = (
        '| aaa      | bbb                        | ccc    |      |\n'
        '|:---------|:--------------------------:|-------:|------|\n'
        '| aaa      | bb</br>b                   |        |      |\n'
        '| 11       | 2001/02/03 04:05:06.000789 |        |      |\n'
        '| ＦＵＬＬ | 全角                       | ＃＄％ | ☀🌞 |\n'
    )
    aligns = [pt.Align.LEFT, pt.Align.CENTER, pt.Align.RIGHT]
    text = pt.to_markdown(input_data, newline='\n', internal_newline='</br>', aligns=aligns,
                          converters=[(datetime.datetime, datetime2str)])
    assert output_data == text
