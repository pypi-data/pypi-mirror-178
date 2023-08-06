#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="duanjunjie",
    version='1.0.0',
    description=(
        "自己用的工具包"
    ),
    long_description=open('README.md').read(),
    author='junjieduan',
    author_email='merch_nerve@163.com',
    maintainer='junjieduan',
    maintainer_email='merch_nerve@163.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://gitee.com/junjieduan/pytools/tree/master',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)