import sqlparse


class SQLFormatter:
    def __init__(
        self,
        reindent=True,
        indent_width=4,
        keyword_case="lower",
        identifier_case="lower",
        comma_first=True,
    ):
        self.reindent = reindent
        self.indent_width = indent_width
        self.keyword_case = keyword_case
        self.identifier_case = identifier_case
        self.comma_first = comma_first

    def format_query(
        self,
        original_query: str,
    ) -> str:
        return sqlparse.format(
            original_query,
            reindent=self.reindent,
            indent_width=self.indent_width,
            keyword_case=self.keyword_case,
            identifier_case=self.identifier_case,
            comma_first=self.comma_first,
        )
