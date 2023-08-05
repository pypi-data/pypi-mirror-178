# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name="convertpath",
    version="0.2.5",
    py_modules=["convertpath"],
    package_dir = {"": "convertpath"},
    install_requires=['pathlib'],

    # metadata to display on PyPI
    author="Shinya Akagi",
    description="Simple Path Convertor",
    long_description=readme,
    long_description_content_type='text/markdown',
    url="https://github.com/ShinyaAkagiI/convertpath", 
    license="PSF",
)
