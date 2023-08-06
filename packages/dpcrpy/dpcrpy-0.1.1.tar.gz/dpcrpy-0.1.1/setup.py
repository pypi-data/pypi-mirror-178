#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Cai Jianping
# Mail: jpingcai@163.com
# Created Time:  2022-7-9 11:25:34 AM
#############################################


from setuptools import setup, find_packages

setup(
    name = "dpcrpy",
    version = "0.1.1",
    keywords = ("dpcr","optimization"),
    description = "A package for differential privacy continuous data release (DPCR)",
    long_description = "A package for differential privacy continuous data release (DPCR)",
    license = "MIT Licence",

    url = "https://github.com/imcjp/Opacus-DPCR",
    author = "Cai Jianping",
    author_email = "jpingcai@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)
