from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'hello package'

# Setting up
setup(
    name="numupi",
    version=VERSION,
    author="nandan",
    author_email="<nandanpadia@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=[],
    classifiers=[]
)