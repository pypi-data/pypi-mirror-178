#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = [ ]

setup(
    author="Iwan Nugraha",
    author_email='iwan.nugraha.e@thalesdigital.io',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="add number for thales",
    entry_points={
        'console_scripts': [
            'addthalesnumbers=addthalesnumbers.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='addthalesnumbers',
    name='addthalesnumbers',
    packages=find_packages(include=['addthalesnumbers', 'addthalesnumbers.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Archangelix/addthalesnumbers',
    version='0.1.3',
    zip_safe=False,
)
