#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pathlib

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from pkg_resources import require
import setuptools

# Steps:
# 1. cd internal
# 2. modify kclvm version in setup.py
# 3. run `python3 setup.py sdist` to build package
# 4. run `python3 -m pip install twine && python3 -m twine upload dist/kclvm-x.y.z.tar.gz` to upload package to PyPI
# 5. input username and password of PyPI

setup(
    name="kclvm",
    author="KCL Authors",
    version="0.4.5.2",
    license="Apache License 2.0",
    description="KCLVM",
    long_description="""A constraint-based record & functional language mainly used in configuration and policy scenarios.""",
    author_email="",
    url="https://kusionstack.io/",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=True,
    # 依赖包
    install_requires=[
        "PyYAML==5.4",
        "lark-parser==0.11.3",
        "filelock==3.6.0",
        "yapf==0.29.0",
        "pypeg2==2.15.2",
        "protobuf==3.19.5",
        "schema",
        "ruamel.yaml",
        "toml",
        "numpydoc",
        "pygls==0.10.3",
        "fastapi",
        "uvicorn",
        "gunicorn==20.1.0",
        "parsy==1.3.0",
        "wasmer==1.0.0",
        "wasmer_compiler_cranelift==1.0.0",
        "pyopenssl==21.0.0",
    ],
)
