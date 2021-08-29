"""

"""
from sqlformatter.sqlformatter import SQLFormatter


class SQLQuery:
    def __init__(self, path: str):
        self._path = path
        self._original_query = None
        self._formatted_query = None
        self._middle_query = None
        self._to_format = None

        self._max_format_iterations = 5
        self._format_iterations = 0

    @property
    def path(self):
        return self._path

    @property
    def original_query(self):
        return self._original_query

    @property
    def formatted_query(self):
        return self._formatted_query

    @property
    def to_format(self):
        return self._to_format

    def format_query(self, formatter: SQLFormatter):
        self._format_query(formatter=formatter)
        while (self._middle_query != self._formatted_query) or (
            self._format_iterations >= self._max_format_iterations
        ):
            self._middle_query = self._formatted_query
            self._format_query(formatter=formatter)
            self._format_iterations += 1

    def _format_query(self, formatter: SQLFormatter):
        self._formatted_query = formatter.format_query(self._middle_query)

    def compare_queries(self):
        assert self._original_query is not None
        assert self._formatted_query is not None

        self._to_format = self._original_query != self._formatted_query

    def save_query(self):
        assert self._formatted_query is not None

        with open(self.path, "w") as file_object:
            file_object.write(self._formatted_query)

    def read_query(self):
        with open(self.path) as file_object:
            self._original_query = file_object.read()
            self._middle_query = self._original_query
