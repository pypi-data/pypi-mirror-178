import setuptools
from pathlib import Path

setuptools.setup(
    name="PyTitanium",
    version=3.2,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"]))