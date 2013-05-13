from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as README:
    DESCRIPTION = README.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='OpenReader',
    version='0.1',
    packages = find_packages(),
    include_package_data = True,
    author = "Not Google",
    license='LICENSE.md',
    long_description=DESCRIPTION,
    description="Reading RSS feeds like it's 2012",
    url="https://github.com/craigsonoffergus/OpenReader",
    install_requires=required,
)