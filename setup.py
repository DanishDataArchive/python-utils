#!/usr/bin/env python

from setuptools import setup, find_packages
from version import get_git_version

setup(
    name = "py-utils-dda",
    version = get_git_version(),
    packages = find_packages(),

    install_requires = ["GitPython>=0.3.2.RC1", "python-magic>=0.4.3"],

    author = "Martin Jensby",
    author_email = "marj@dda.dk",
    description = "Collection of python utils for dda",
    license = "GPL",

    entry_points = {
        'console_scripts': [
            'directorycleaner = utils.DirectoryCleaner:main',
            'fileexists = utils.FileExists:main',
            'jenkins = utils.Jenkins:main',
            'magic = utils.Magic:main',
            'searchjarsforclass = utils.SearchJarsForClass:main',
            'splitstring = utils.SplitString:main',
            'travis = utils.Travis:main',
            'git-projects = utils.GitProjects:main',
        ]
    }
)


