from distutils.core import setup
from setuptools import find_packages
from pip.req import parse_requirements as parse


setup(
    name='talka2z',
    version='0.3',
    packages=find_packages(exclude=('tests', 'tests.*')),
    install_requires=[
    ]
)
