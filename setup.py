# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='timur',
    version='0.0.1',
    description='Fnite-state morphology for German',
    long_description=readme,
    author='Kay-Michael Würzner',
    author_email='wuerzner@gmail.com',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
    ],
    entry_points={
          'console_scripts': [
              'timur=timur.scripts.timur:cli',
          ]
    },
)
