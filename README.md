# sqlmakeuper

Python library with CLI interface for sql formatting based on [sqlparse](https://github.com/andialbrecht/sqlparse)

## Installation

```bash
pip install sqlmakeuper
```

## Using

### Format with default parameters

```bash
sqlmakeup --path /path/with/files/to/format
```

- Default parameters are `(reindent=True, indent_width=4, keyword_case="lower", identifier_case="lower", comma_first=True,)`

### Format with custom parameters

```bash
sqlmakeup --path /path/with/files/to/format --parameters '{"comma_first":0}'
```

### Check with custom parameters

```bash
sqlmakeup --path /path/with/files/to/format --check
```
