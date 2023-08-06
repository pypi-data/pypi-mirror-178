"""Python setup.py for godule package"""
import io
import os
from pathlib import Path
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("godule", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    filename = Path(Path(__file__).absolute().parent, *paths)
    with io.open(
        filename,
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]

setup(
    name="godule",
    version="0.1.0.dev",
    description="__god__ule",
    url="https://github.com/carlosejimenez/godule",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Carlos E. Jimenez",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=['more_itertools', 'matplotlib>=3.1,!=3.6.1'],
)
