#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pycurl',
    'six',
]

test_requirements = [
    'mock',
    'pytest',
]

setup(
    name='ftps',
    version='0.1.0',
    description="ftps client based on pycurl",
    long_description=readme + '\n\n' + history,
    author="Javier Collado",
    author_email='javier.collado@gmail.com',
    url='https://github.com/jcollado/ftps',
    packages=[
        'ftps',
    ],
    package_dir={'ftps':
                 'ftps'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='ftps',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
