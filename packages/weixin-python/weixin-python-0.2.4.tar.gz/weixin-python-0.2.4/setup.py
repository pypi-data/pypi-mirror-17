# -*- coding: utf-8 -*-


import os

from setuptools import setup, find_packages


def fread(fname):
    filepath = os.path.join(os.path.dirname(__file__), fname)
    with open(filepath) as f:
        return f.read()

setup(
    name='weixin-python',
    description='Weixin for Python',
    long_description=fread('README.rst'),
    license = 'BSD',
    packages = find_packages(),
    version='0.2.4',
    author='zwczou',
    author_email='zwczou@gmail.com',
    url='https://github.com/zwczou/weixin-python',
    keywords=['weixin', 'weixin pay', 'weixin login'],
    zip_safe=False,
    platforms='any',
    install_requires=[
    ],
    classifiers=[],
)
