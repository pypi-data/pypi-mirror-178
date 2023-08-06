import setuptools
from pathlib import Path

setuptools.setup(
    name = "simipdf",
    version = 1.0,
    long_description=Path("D:\simipdf\README.md").read_text(),
    packages=setuptools.find_packages(exclude= ["test","data"])

)