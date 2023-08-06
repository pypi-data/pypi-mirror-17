#!/usr/bin/env python

from os.path import exists
from setuptools import setup, find_packages

setup(
    name='swiftwind',
    version=open('VERSION').read().strip(),
    author='Adam Charnock',
    author_email='adam@adamcharnock.com',
    packages=find_packages(),
    scripts=[],
    url='https://github.com/waldocollective/swiftwind',
    license='MIT',
    description='User-friendly billing for communal households',
    long_description=open('README.rst').read() if exists("README.rst") else "",
    install_requires=[
        'django>=1.8',
        'path.py',
        'django-model-utils>=2.5.0',
        'gunicorn',
        'django-bootstrap3>=5',
        'dj-database-url',
        'dj-static',
        'psycopg2',
        'django-extensions',
    ],
)
