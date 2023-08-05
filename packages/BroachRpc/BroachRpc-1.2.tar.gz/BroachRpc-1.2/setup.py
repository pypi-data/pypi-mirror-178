#!/usr/bin/env python
# coding=utf-8

from distutils.core import setup
from setuptools import find_packages

setup(
    name='BroachRpc',
    version='1.2',
    description=(
        '基于python的一个rpc微服务框架，开箱即用，无需注册中心'
    ),
    long_description=open('README.rst').read(),
    author='kcangYan',
    author_email='842762472@qq.com',
    maintainer='kcangYan',
    maintainer_email='842762472@qq.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/KcangYan/BroachRpc',
    install_requires=[],
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