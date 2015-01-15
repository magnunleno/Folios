#!/usr/bin/env python3
# encoding: utf-8

from os import walk
from os import path
from setuptools import setup
from setuptools import find_packages

entry_points = {
    'console_scripts': [
        'folios = folios:main',
    ]
}

# Generate requirements
with open('requirements.txt') as fd:
    requires = map(str.strip, fd.readlines())
    requires = [line for line in requires if line]

# Generate data folders
data_folders = []
_root = path.sep.join(['.', 'folios'])
for root, folders, files in walk(path.sep.join([_root, 'data'])):
    if root == _root:
        continue
    root = root.replace(_root + path.sep, '')
    if len(data_folders) > 0 and root.startswith(data_folders[-1]):
        data_folders.pop(-1)
    data_folders.append(root)
data_folders.sort(reverse=True)
data_folders = [path.sep.join([data, '*']) for data in data_folders]

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
        'folios': data_folders,
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

