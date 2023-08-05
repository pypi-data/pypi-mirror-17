import codecs
import os
import re
from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)

    raise RuntimeError("Unable to find version string.")

setup(
    name='pytest-asyncio',
    version=find_version('pytest_asyncio', '__init__.py'),
    packages=find_packages(),
    url='https://github.com/pytest-dev/pytest-asyncio',
    license='Apache 2.0',
    author='Tin Tvrtkovic',
    author_email='tinchester@gmail.com',
    description='Pytest support for asyncio.',
    long_description=readme,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Testing",
        "Framework :: Pytest",
    ],
    install_requires=[
        'pytest >= 3.0.2',
    ],
    extras_require={
        ':python_version == "3.3"': ['asyncio']
    },
    entry_points={
        'pytest11': ['asyncio = pytest_asyncio.plugin'],
    },
)
