# coding=utf-8
from setuptools import setup

setup(
    name='putio.py',
    description='Python client for put.io API v2',
    version='3.1.0',
    author=u'Cenk Altı',
    author_email='cenkalti@gmail.com',
    url='http://github.com/cenk/putio.py',
    py_modules=['putio'],
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=['requests'],
)
