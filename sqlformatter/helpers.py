"""Helper functions"""

import logging
import os
from glob import glob
from typing import List
import sys

from sqlformatter.config import SUPPORTED_FILES
from sqlformatter.sql_query import SQLQuery


def check_path(path: str) -> List[str]:
    """
        Function searches the provided directory and return list of the sql file paths that finds.
    Args:
        path: path of the directory to search for sqls to process

    Returns:
        List of the sql file paths to process

    """
    if os.path.isfile(path):
        if any(path.endswith(ending) for ending in SUPPORTED_FILES):
            return [path]
        raise Exception(f"works only with {SUPPORTED_FILES}")
    paths = [
        glob(os.path.join(dir, f"*{file_type}"))
        for file_type in SUPPORTED_FILES
        for dir, _, _ in os.walk(path)
    ]
    return [item for sublist in paths for item in sublist]


def process_query(sql_query: SQLQuery, to_check: bool):
    """
        Function based on the status of to_check argument
        either informs about possible changes to the file
        or applies changes to the sql file
    Args:
        sql_query: sql query object
        to_check: boolean variable informing to check or apply changes

    Returns:

    """
    if sql_query.to_format:
        if to_check:
            logging.info("would reformat %s", sql_query.path)
        else:
            sql_query.save_query()
            logging.info("%s is formatted", sql_query.path)


def make_report(sql_queries: List[SQLQuery], to_check: bool = False):
    """
        Function prints report based on the amount of the processed sql queries
    Args:
        sql_queries: List of the SQLQuery objects that have been processed
        to_check: boolean variable informing to check or apply changes

    Returns:

    """
    reformat_number = sum([sql_query.to_format for sql_query in sql_queries])
    not_reformat_number = len(sql_queries) - reformat_number

    part_1 = (
        "Oh no! 💥 💔 💥 \n"
        if (to_check and (reformat_number > 0))
        else "All done! ✨ 🍰 ✨ \n"
    )
    part_2 = f"{reformat_number} sql files " if reformat_number > 0 else ""
    part_3 = (
        ""
        if reformat_number == 0
        else "sql files would be reformatted, "
        if to_check
        else "sql files reformatted, "
    )
    part_4 = f"{not_reformat_number} sql files "
    part_5 = "would be left unchanged." if to_check else "left unchanged."

    report_message = "".join([part_1, part_2, part_3, part_4, part_5])

    logging.info(report_message)

    return reformat_number


def define_exit(reformat_number: int, to_check: bool):
    if to_check and (reformat_number > 0):
        sys.exit(1)
    sys.exit(0)
