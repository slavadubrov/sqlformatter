import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = ["sqlparse==0.4.1"]

setuptools.setup(
    name="sql-formatter",
    version="0.1",
    author="Viacheslav Dubrov",
    author_email="slavadubrov@gmail.com",
    description="SQL Formatter based on sqlparse",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/slavadubrov/sqlformatter",
    classifiers=["Programming Language :: Python :: 3"],
    python_requires=">=3.6",
    install_requires=requirements,
)
