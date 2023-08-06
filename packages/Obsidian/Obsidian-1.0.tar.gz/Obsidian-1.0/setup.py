#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = "Obsidian",
    version = "1.0",
    packages = find_packages(),
    scripts = ['obsidian'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = [
    ],
    requires = [
        'scrapy',
    ],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.md'],
    },

    # metadata for upload to PyPI
    author = "amoblin",
    author_email = "amoblin@gmail.com",
    description = "Obsidian make web crawl easier",
    license = "MIT",
    keywords = "web crawl json",
    url = "https://github.com/amoblin/Obsidian",

    # could also include long_description, download_url, classifiers, etc.
)
