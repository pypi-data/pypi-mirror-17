# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup, find_packages


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('src/bslint.py').read(),
    re.M
    ).group(1)


with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "bslint",
    packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_dir={'src': 'src'},
    package_data={'src': ['config/*.json']},
    entry_points = { "console_scripts": ['bslint = src.bslint:main'] },
    version = version,
    description = "A linter tool for the BrightScript language.",
    long_description = long_descr,
    author = "BSLint",
    author_email = "zachary.robinson@sky.uk",
    url = "https://github.com/sky-uk/roku-linter",
    download_url = 'https://github.com/sky-uk/bslint/archive/0.2.0.tar.gz'
    )
