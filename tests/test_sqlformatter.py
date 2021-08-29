import unittest

from sqlformatter.sqlformatter import SQLFormatter


class TestSQLFormatter(unittest.TestCase):

    paths = dict(
        original="tests/test_sqls/original_1.sql",
        expected="tests/test_sqls/expected_1.sql",
    )

    def test_format_query(self):
        sqls = dict()
        for name, path in self.paths.items():
            with open(path) as file:
                sqls[name] = file.read()

        formatter = SQLFormatter()
        sqls["formatted"] = formatter.format_query(sqls["original"])

        self.assertEqual(sqls["expected"], sqls["formatted"])
