import setuptools
from pathlib import Path

setuptools.setup(
    # set to name which don't conflict with other pypi package
    name='hccpdf',
    version=1.0,
    long_description=Path("README.md").read_text(),
    # exclude tests & data, because they donnot contain source code
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
