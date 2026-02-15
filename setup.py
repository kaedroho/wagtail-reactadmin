#!/usr/bin/env python

from os import path

from setuptools import find_packages, setup
from wagtail_reactadmin import __version__

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="wagtail_reactadmin",
    version=__version__,
    description="React Admin for Wagtail CMS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="",
    author_email="",
    url="",
    packages=find_packages(),
    include_package_data=True,
    license="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Framework :: Django",
        "Framework :: Django :: 6",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 7.2",
        "Framework :: Wagtail :: 7.3",
    ],
    install_requires=[],
    extras_require={},
    zip_safe=False,
)
