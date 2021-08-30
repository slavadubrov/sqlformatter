# sql-formatter

Python library with CLI interface for sql formatting based on sqlparse

## Installation

```bash
pip install sql-formatter
```

## Using

### Format with default parameters (reindent=True, indent_width=4, keyword_case="lower", identifier_case="lower", comma_first=True,)

```bash
sqlformatter --path /path/with/files/to/format
```

### Format with custom parameters

```bash
sqlformatter --path /path/with/files/to/format --parameters '{"comma_first":0}'
```

### Check with custom parameters

```bash
sqlformatter --path /path/with/files/to/format --check
```
