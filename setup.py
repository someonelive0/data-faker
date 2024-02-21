# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='data-faker',
    version='0.1.0',
    description='Data faker for test',
    long_description=readme,
    author='Someonelive',
    author_email='someonelive0',
    url='https://github.com/someonelive0/data-scanner',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
