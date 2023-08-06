#!/usr/bin/env Python
"""
jgtapy
"""

from setuptools import find_packages, setup

from jgtapy import __version__ as version

INSTALL_REQUIRES = [
    'pandas>=0.25.1',
    'tapy>=1.9.5'
]

EXTRAS_DEV_LINT = [
    "flake8>=3.6.0,<3.7.0",
    "isort>=4.3.4,<4.4.0",
]

EXTRAS_DEV_TEST = [
    "coverage",
    "pytest>=3.10",
]

EXTRAS_DEV_DOCS = [
    "readme_renderer",
    "sphinx",
    "sphinx_rtd_theme>=0.4.0",
]

setup(
    name='jgtapy',
    version=version,
    description='JGT Technical Indicators',
    long_description=open('README.rst').read(),
    author='Guillaume Isabelle',
    author_email='jgi@jgwill.com',
    url='https://github.com/jgwill/jgtapy',
    packages=find_packages(exclude=['*test*']),
    install_requires=INSTALL_REQUIRES,
    extras_require={
        'dev': (EXTRAS_DEV_LINT + EXTRAS_DEV_TEST + EXTRAS_DEV_DOCS),
        'dev-lint': EXTRAS_DEV_LINT,
        'dev-test': EXTRAS_DEV_TEST,
        'dev-docs': EXTRAS_DEV_DOCS,
    },
    license='MIT',
    keywords='technical analyse indicators pandas forex stocks',
    classifiers=[
        "Development Status :: 5 - Beta",
        "Intended Audience :: Developers", 
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
