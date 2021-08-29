import shutil
import tempfile
import unittest
from testfixtures import LogCapture


class TestHelpers(unittest.TestCase):

    path = "tests/test_sqls"

    file_paths = dict(
        original=f"{path}/original_1.sql",
        expected=f"{path}/expected_1.sql",
    )

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_check_path_one(self):
        from sqlformatter.helpers import check_path

        found_files = check_path(self.file_paths["original"])

        self.assertListEqual([self.file_paths["original"]], found_files)

    def test_check_path_few(self):
        from sqlformatter.helpers import check_path

        found_files = check_path(self.path)

        self.assertSetEqual(set(self.file_paths.values()), set(found_files))

    def test_check_path_exception(self):
        from sqlformatter.helpers import check_path

        not_sql_file = f"{self.test_dir}/file.txt"
        with open(not_sql_file, "w") as file_object:
            file_object.write("select * from table")

        with self.assertRaises(Exception):
            check_path(not_sql_file)

    def test_process_query_check(self):
        from sqlformatter.helpers import process_query
        from sqlformatter.sql_query import SQLQuery
        from sqlformatter.sqlformatter import SQLFormatter

        query_to_save = "select * from datatable"
        file_path = f"{self.test_dir}/query.csv"
        with open(file_path, "w") as file:
            file.write(query_to_save)

        with LogCapture() as log_capture:
            sql_query = SQLQuery(file_path)
            sql_query.read_query()
            sql_query.format_query(SQLFormatter())
            sql_query.compare_queries()
            process_query(sql_query=sql_query, to_check=True)

        log_capture.check(
            ("root", "INFO", f"would reformat {sql_query.path}"),
        )

    def test_process_query_format(self):
        from sqlformatter.helpers import process_query
        from sqlformatter.sql_query import SQLQuery
        from sqlformatter.sqlformatter import SQLFormatter

        query_to_save = "select * from datatable"
        file_path = f"{self.test_dir}/query.csv"
        with open(file_path, "w") as file:
            file.write(query_to_save)

        with LogCapture() as log_capture:
            sql_query = SQLQuery(file_path)
            sql_query.read_query()
            sql_query.format_query(SQLFormatter())
            sql_query.compare_queries()
            process_query(sql_query=sql_query, to_check=False)

        log_capture.check(
            ("root", "INFO", f"{sql_query.path} is formatted"),
        )

        with open(file_path) as file:
            formatted_file = file.read()

        self.assertEqual(formatted_file, sql_query.formatted_query)

    def test_make_report_1(self):
        from sqlformatter.helpers import make_report
        from sqlformatter.sql_query import SQLQuery
        from sqlformatter.sqlformatter import SQLFormatter

        with LogCapture() as log_capture:
            sql_query = SQLQuery(self.file_paths["original"])
            sql_query.read_query()
            sql_query.format_query(SQLFormatter())
            sql_query.compare_queries()
            make_report(sql_queries=[sql_query], to_check=True)

        log_capture.check(
            (
                "root",
                "INFO",
                "Oh no! 💥 💔 💥 \n1 sql files sql files would be reformatted, 0 sql files would be left unchanged.",
            ),
        )

    def test_make_report_2(self):
        from sqlformatter.helpers import make_report
        from sqlformatter.sql_query import SQLQuery
        from sqlformatter.sqlformatter import SQLFormatter

        with LogCapture() as log_capture:
            sql_query = SQLQuery(self.file_paths["expected"])
            sql_query.read_query()
            sql_query.format_query(SQLFormatter())
            sql_query.compare_queries()
            make_report(sql_queries=[sql_query], to_check=True)

        log_capture.check(
            (
                "root",
                "INFO",
                "All done! ✨ 🍰 ✨ \n1 sql files would be left unchanged.",
            ),
        )

    def test_define_exit(self):
        from sqlformatter.helpers import define_exit

        with self.assertRaises(SystemExit) as cm:
            define_exit(reformat_number=1, to_check=True)
        self.assertEqual(cm.exception.code, 1)

        with self.assertRaises(SystemExit) as cm:
            define_exit(reformat_number=0, to_check=True)
        self.assertEqual(cm.exception.code, 0)
