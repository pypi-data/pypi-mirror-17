#!/usr/bin/env python
from setuptools import setup

files = [
    "ansible/module_utils",
    "ansible/modules/hashivault",
]

long_description=open('README.rst', 'r').read()

setup(
    name='ansible-modules-hashivault',
    version='2.5.6',
    description='Ansible Modules for Hashicorp Vault',
    long_description=long_description,
    author='Terry Howe',
    author_email='terrylhowe@example.com',
    url='https://github.com/TerryHowe/ansible-modules-hashivault',
    packages=files,
    install_requires = [
        'ansible>=2.0.0',
        'hvac',
    ],
)
