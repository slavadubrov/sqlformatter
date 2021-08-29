import shutil
import tempfile
import unittest

from sqlformatter.sql_query import SQLQuery
from sqlformatter.sqlformatter import SQLFormatter


class TestSQLQuery(unittest.TestCase):

    paths = dict(
        original="tests/test_sqls/original_1.sql",
        expected="tests/test_sqls/expected_1.sql",
    )

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_read_query(self):
        with open(self.paths["original"]) as file:
            standard_read = file.read()

        sql_query = SQLQuery(self.paths["original"])
        sql_query.read_query()

        self.assertEqual(standard_read, sql_query.original_query)

    def test_format_query(self):

        sql_query = SQLQuery(self.paths["original"])
        sql_query.read_query()
        sql_query.format_query(SQLFormatter())

        with open(self.paths["expected"]) as file:
            expected_sql = file.read()

        self.assertEqual(expected_sql, sql_query.formatted_query)

    def test_save_query(self):

        query_to_save = "select * from datatable"
        file_path = f"{self.test_dir}/query.csv"
        with open(file_path, "w") as file:
            file.write(query_to_save)

        sql_query = SQLQuery(file_path)
        sql_query.read_query()
        sql_query.format_query(SQLFormatter())
        sql_query.save_query()

        with open(file_path) as file:
            saved_query = file.read()

        self.assertEqual(sql_query.formatted_query, saved_query)

    def test_compare_queries_true(self):

        sql_query = SQLQuery(self.paths["original"])
        sql_query.read_query()
        sql_query.format_query(SQLFormatter())
        sql_query.compare_queries()

        self.assertTrue(sql_query.to_format)

    def test_compare_queries_false(self):

        sql_query = SQLQuery(self.paths["expected"])
        sql_query.read_query()
        sql_query.format_query(SQLFormatter())
        sql_query.compare_queries()

        self.assertFalse(sql_query.to_format)
