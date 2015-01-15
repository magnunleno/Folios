#!/usr/bin/env python3
# encoding: utf-8

from setuptools import setup
from setuptools import find_packages

with open('requirements.txt') as fd:
    requires = map(str.strip, fd.readlines())
    requires = [line for line in requires if line]

entry_points = {
    'console_scripts': [
        'folios = folios:main',
    ]
}


setup(
    name="Folios",
    version="0.1.0",
    url='https://github.com/magnunleno/Folios',
    author='Magnun Leno',
    author_email='magnun.leno@gmail.com',
    description="My own static site generator.",
    long_description="No long description yet :D",
    packages=find_packages(),
    package_data={
        'folios': ['data/*/*'],
        },
    include_package_data=True,
    install_requires=requires,
    entry_points=entry_points,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='nose.collector',
)

