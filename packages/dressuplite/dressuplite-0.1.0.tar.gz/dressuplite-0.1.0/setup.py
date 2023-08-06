"""Package installation setup."""
import os
import re
from pathlib import Path
from typing import Match, cast

from setuptools import find_packages, setup

_DIR = Path(__file__).parent

setup(
    name="dressuplite",
    author="Ouroboros Chrysopoeia",
    author_email="impredicative@users.nomail.github.com",
    version=cast(Match, re.fullmatch(r"refs/tags/v?(?P<ver>\S+)", os.environ["GITHUB_REF"]))["ver"],  # Ex: GITHUB_REF="refs/tags/1.2.3"; version="1.2.3"
    description="Dependency-free fork of `dressup`",
    keywords="unicode text",
    long_description=(_DIR / "README.md").read_text().strip(),
    long_description_content_type="text/markdown",
    url="https://github.com/impredicative/dressuplite/",
    packages=find_packages(exclude=["archive", "scripts"]),
    python_requires=">=3.11",
    classifiers=[  # https://pypi.org/classifiers/
        # For feature compatibility, see https://nedbatchelder.com/text/which-py.html
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing :: General",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
