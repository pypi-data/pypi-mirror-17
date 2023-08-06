# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import collections
import os

import pytest

import pytablereader
from pytablereader.interface import TableLoader
from pytablereader.data import TableData
from pytablereader.markdown.formatter import MarkdownTableFormatter


Data = collections.namedtuple("Data", "value expected")

test_data_empty = Data(
    """[]""",
    [
        TableData("tmp", [], []),
    ])

test_data_01 = Data(
    """{| class="wikitable"
! a
! b
! c
|-
| style="text-align:right"| 1
| style="text-align:right"| 123.1
| a
|-
| style="text-align:right"| 2
| style="text-align:right"| 2.2
| bb
|-
| style="text-align:right"| 3
| style="text-align:right"| 3.3
| ccc
|}
""",
    [
        TableData(
            table_name=u"markdown1",
            header_list=[u'a', u'b', u'c'],
            record_list=[
                [u'1', u'123.1', u'a'],
                [u'2', u'2.2', u'bb'],
                [u'3', u'3.3', u'ccc'],
            ]
        ),
    ])

test_data_02 = Data(
    """{| class="wikitable"
|+tablename
! a
! b
! c
|-
| style="text-align:right"| 1
| style="text-align:right"| 123.1
| a
|-
| style="text-align:right"| 2
| style="text-align:right"| 2.2
| bb
|-
| style="text-align:right"| 3
| style="text-align:right"| 3.3
| ccc
|}
""",
    [
        TableData(
            table_name=u"tablename",
            header_list=[u'a', u'b', u'c'],
            record_list=[
                [u'1', u'123.1', u'a'],
                [u'2', u'2.2', u'bb'],
                [u'3', u'3.3', u'ccc'],
            ]
        ),
    ])

test_data_03 = Data(
    """
<html>
  <head>
    header
  </head>
  <body>
    hogehoge
  </body>
</html>
""",
    [])

test_data_04 = Data(
    """{| class="wikitable"
|+tablename
! a
! b
! c
|-
| style="text-align:right"| 1
| style="text-align:right"| 123.1
| a
|-
| style="text-align:right"| 2
| style="text-align:right"| 2.2
| bb
|-
| style="text-align:right"| 3
| style="text-align:right"| 3.3
| ccc
|}
{| class="wikitable"
! a
! b
|-
| style="text-align:right"| 1
| style="text-align:right"| 123.1
|-
| style="text-align:right"| 2
| style="text-align:right"| 2.2
|-
| style="text-align:right"| 3
| style="text-align:right"| 3.3
|}
""",
    [
        TableData(
            table_name=u"tmp_tablename",
            header_list=[u'a', u'b', u'c'],
            record_list=[
                [u'1', u'123.1', u'a'],
                [u'2', u'2.2', u'bb'],
                [u'3', u'3.3', u'ccc'],
            ]
        ),
        TableData(
            table_name=u"tmp_markdown2",
            header_list=[u'a', u'b'],
            record_list=[
                [u'1', u'123.1'],
                [u'2', u'2.2'],
                [u'3', u'3.3'],
            ]
        ),
    ])


@pytest.mark.xfail
class MarkdownTableFormatter_constructor(object):

    @pytest.mark.parametrize(["value", "source", "expected"], [
        ["tablename", None, pytablereader.InvalidDataError],
        ["tablename", "", pytablereader.InvalidDataError],
    ])
    def test_exception(
            self, monkeypatch, value, source, expected):
        with pytest.raises(expected):
            MarkdownTableFormatter(source)


@pytest.mark.xfail
class Test_MarkdownTableFormatter_make_table_name:

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @property
    def valid_tag_property(self):
        return "markdowntable"

    @property
    def null_tag_property(self):
        return None

    FILE_LOADER_TEST_DATA = [
        ["%(filename)s", "/path/to/data.markdown", "data"],
        ["prefix_%(filename)s",  "/path/to/data.md", "prefix_data"],
        ["%(filename)s_suffix", "/path/to/data.md", "data_suffix"],
        [
            "prefix_%(filename)s_suffix",
            "/path/to/data.md",
            "prefix_data_suffix"
        ],
        [
            "%(filename)s%(filename)s",
            "/path/to/data.md",
            "datadata"
        ],
        [
            "%(format_name)s%(format_id)s_%(filename)s",
            "/path/to/data.md",
            "mediawiki0_data"
        ],
    ]

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [
            ["%(default)s",  "/path/to/data.md", "data_mediawikitable"],
        ] + FILE_LOADER_TEST_DATA)
    def test_normal_MarkdownTableFileLoader_valid_tag(
            self, monkeypatch, value, source, expected):
        monkeypatch.setattr(
            MarkdownTableFormatter, "table_id", self.valid_tag_property)

        loader = pytablereader.MarkdownTableFileLoader(source)
        loader.table_name = value
        formatter = MarkdownTableFormatter(value)
        formatter.accept(loader)

        assert formatter._make_table_name() == expected

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [
            ["%(default)s",  "/path/to/data.md", "data_mediawiki0"],
        ] + FILE_LOADER_TEST_DATA)
    def test_normal_MarkdownTableFileLoader_null_tag(
            self, monkeypatch, value, source, expected):
        monkeypatch.setattr(
            MarkdownTableFormatter, "table_id", self.null_tag_property)

        loader = pytablereader.MarkdownTableFileLoader(source)
        loader.table_name = value
        formatter = MarkdownTableFormatter(value)
        formatter.accept(loader)

        assert formatter._make_table_name() == expected

    @pytest.mark.parametrize(["value", "source", "expected"], [
        [None, "/path/to/data.md", ValueError],
        ["", "/path/to/data.md", ValueError],
        [
            "%(%(filename)s)",
            "/path/to/data.md",
            pytablereader.InvalidTableNameError  # %(data)
        ],
    ])
    def test_MarkdownTableFileLoader_exception(
            self, monkeypatch, value, source, expected):
        monkeypatch.setattr(
            MarkdownTableFormatter, "table_id", self.null_tag_property)

        loader = pytablereader.MarkdownTableFileLoader(source)
        loader.table_name = value
        formatter = MarkdownTableFormatter(source)
        formatter.accept(loader)

        with pytest.raises(expected):
            formatter._make_table_name()

    @pytest.mark.parametrize(["value", "expected"], [
        ["%(default)s", "mediawikitable"],
        ["%(key)s", "mediawikitable"],
        ["%(format_name)s%(format_id)s", "mediawiki0"],
        ["%(filename)s%(format_name)s%(format_id)s", "mediawiki0"],
        ["tablename", "tablename"],
        ["table", "table_mediawiki"],
    ])
    def test_normal_MarkdownTableTextLoader_valid_tag(
            self, monkeypatch, value, expected):
        monkeypatch.setattr(
            MarkdownTableFormatter, "table_id", self.valid_tag_property)

        source = "<table></table>"
        loader = pytablereader.MarkdownTableTextLoader(source)
        loader.table_name = value
        formatter = MarkdownTableFormatter(source)
        formatter.accept(loader)

        assert formatter._make_table_name() == expected

    @pytest.mark.parametrize(["value", "expected"], [
        ["%(default)s", "mediawiki0"],
        ["%(key)s", "mediawiki0"],
        ["%(format_name)s%(format_id)s", "mediawiki0"],
        ["%(filename)s%(format_name)s%(format_id)s", "mediawiki0"],
        ["tablename", "tablename"],
        ["table", "table_mediawiki"],
    ])
    def test_normal_MarkdownTableTextLoader_null_tag(
            self, monkeypatch, value, expected):
        monkeypatch.setattr(
            MarkdownTableFormatter, "table_id", self.null_tag_property)

        source = "<table></table>"
        loader = pytablereader.MarkdownTableTextLoader(source)
        loader.table_name = value
        formatter = MarkdownTableFormatter(source)
        formatter.accept(loader)

        assert formatter._make_table_name() == expected

    @pytest.mark.parametrize(["value", "source", "expected"], [
        [None, "<table></table>", ValueError],
        [
            "%(filename)s",
            "<table></table>",
            pytablereader.InvalidTableNameError
        ],
    ])
    def test_exception_MarkdownTableTextLoader(
            self, monkeypatch, value, source, expected):
        monkeypatch.setattr(
            MarkdownTableFormatter, "table_id", self.valid_tag_property)

        loader = pytablereader.MarkdownTableTextLoader(source)
        loader.table_name = value
        formatter = MarkdownTableFormatter(source)
        formatter.accept(loader)

        with pytest.raises(expected):
            print(formatter._make_table_name())


@pytest.mark.xfail
class Test_MarkdownTableFileLoader_load:

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(
        [
            "test_id",
            "table_text",
            "filename",
            "table_name",
            "expected_tabledata_list",
        ],
        [
            [
                1,
                test_data_01.value,
                "tmp.md",
                "%(key)s",
                test_data_01.expected
            ],
            [
                2,
                test_data_02.value,
                "tmp.md",
                "%(key)s",
                test_data_02.expected,
            ],
            [
                3,
                test_data_03.value,
                "tmp.md",
                "%(default)s",
                test_data_03.expected,
            ],
            [
                4,
                test_data_04.value,
                "tmp.md",
                "%(default)s",
                test_data_04.expected,
            ],
        ])
    def test_normal(
            self, tmpdir, test_id, table_text, filename,
            table_name, expected_tabledata_list):
        p_file_path = tmpdir.join(filename)

        parent_dir_path = os.path.dirname(str(p_file_path))
        if not os.path.isdir(parent_dir_path):
            os.makedirs(parent_dir_path)

        with open(str(p_file_path), "w") as f:
            f.write(table_text)

        loader = pytablereader.MarkdownTableFileLoader(str(p_file_path))
        loader.table_name = table_name

        for tabledata, expected in zip(loader.load(), expected_tabledata_list):
            print("test {}".format(test_id))
            print("  tabledata: {}".format(tabledata))
            print("  expected:  {}".format(expected))
            print("")
            assert tabledata == expected

    @pytest.mark.parametrize(
        [
            "table_text",
            "filename",
            "expected",
        ],
        [
            [
                "",
                "tmp.md",
                pytablereader.InvalidDataError,
            ],
        ])
    def test_exception(
            self, tmpdir, table_text, filename, expected):
        p_file_path = tmpdir.join(filename)

        with open(str(p_file_path), "w") as f:
            f.write(table_text)

        loader = pytablereader.MarkdownTableFileLoader(str(p_file_path))

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass

    @pytest.mark.parametrize(["filename", "expected"], [
        ["", pytablereader.InvalidDataError],
        [None, pytablereader.InvalidDataError],
    ])
    def test_null(
            self, tmpdir, filename, expected):
        loader = pytablereader.MarkdownTableFileLoader(filename)

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass


@pytest.mark.xfail
class Test_MarkdownTableTextLoader_load:

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(
        [
            "test_id",
            "table_text",
            "table_name",
            "expected_tabletuple_list",
        ],
        [
            [
                1,
                test_data_01.value,
                "%(default)s",
                test_data_01.expected,
            ],
            [
                2,
                test_data_02.value,
                "%(default)s",
                test_data_02.expected,
            ],
            [
                3,
                test_data_03.value,
                "%(default)s",
                test_data_03.expected,
            ],
        ])
    def test_normal(self, test_id, table_text, table_name, expected_tabletuple_list):
        loader = pytablereader.MarkdownTableTextLoader(table_text)
        loader.table_name = table_name

        for tabledata in loader.load():
            print("id: {}".format(test_id))
            print("  tabledata: {}".format(tabledata))
            print("  expected:")
            for expected in expected_tabletuple_list:
                print("    {}".format(expected))
            print("")

            assert tabledata in expected_tabletuple_list

    @pytest.mark.parametrize(["table_text", "expected"], [
        [
            "",
            pytablereader.InvalidDataError,
        ],
    ])
    def test_exception(self, table_text, expected):
        loader = pytablereader.MarkdownTableTextLoader(table_text)
        loader.table_name = "dummy"

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass

    @pytest.mark.parametrize(["table_text", "expected"], [
        ["", pytablereader.InvalidDataError],
        [None, pytablereader.InvalidDataError],
    ])
    def test_null(self, table_text, expected):
        loader = pytablereader.MarkdownTableTextLoader(table_text)
        loader.table_name = "dummy"

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass
