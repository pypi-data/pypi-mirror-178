from setuptools import setup

import compileall

from os import path

# 读取readme文件，这样可以直接显示在主页上
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

compileall.compile_dir("src")

setup(
    name="hero_auto_sql",
    version="1.0.0",
    packages=["core", "model", "sql_parser", "utils"],
    url="",
    license="Apache 2.0",
    author="dawndevil",
    author_email="",
    description="",
    keywords="",
    python_requires=">=3.8",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["sqlalchemy", "sqlalchemy-utils", "pymysql", "pytest"],
)
