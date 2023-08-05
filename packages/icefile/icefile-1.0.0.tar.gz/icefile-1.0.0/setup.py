# -*- coding: utf-8 -*-
 
"""
Author: ice
Description: This module can be more convenient to operate files
"""
 
import setuptools
 
 
with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
 
 
setuptools.setup(
    name='icefile',
    version="1.0.0",
    author="ice",
    author_email="bilibili_wulihb@outlook.com",
    description="This module can be more convenient to operate files",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
