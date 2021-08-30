"""
    Main script for running sql-formatter
"""
import argparse
import json
import logging

from sqlformatter.helpers import check_path, define_exit, make_report, process_query
from sqlformatter.sql_query import SQLQuery
from sqlformatter.sqlformatter import SQLFormatter

logging.basicConfig(level=logging.INFO)


def parse_args():
    """
    Function for parsing input arguments
    """
    parser = argparse.ArgumentParser(description="SQL formatter")
    parser.add_argument("--path")
    parser.add_argument("--check", dest="check", action="store_true")
    parser.add_argument(
        "--parameters",
        type=json.loads,
        default="""{
            "reindent":1, 
            "indent_width":4, 
            "keyword_case":"upper", 
            "identifier_case":"lower", 
            "comma_first":1
            }""",
    )
    return vars(parser.parse_args())


def main(args=None):
    """
    Entry-point function for sql formatting
    """
    args = parse_args()

    paths = check_path(path=args["path"])
    if paths:
        sql_formatter = SQLFormatter(**args["parameters"])
        sql_queries = [SQLQuery(path=path) for path in paths]
        for sql_query in sql_queries:
            sql_query.read_query()
            sql_query.format_query(formatter=sql_formatter)
            sql_query.compare_queries()
            process_query(
                sql_query=sql_query,
                to_check=args["check"],
            )
        reformat_number = make_report(sql_queries=sql_queries, to_check=args["check"])
        define_exit(reformat_number=reformat_number, to_check=args["check"])
    logging.info("No SQL files are present to be formatted. Nothing to do 😴")
