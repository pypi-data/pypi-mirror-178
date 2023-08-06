import setuptools
from pathlib import Path


setuptools.setup(
    name="mankspdf",
    version="1.0",
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests","data"])   #to find all packages and exclude tests and data

) 