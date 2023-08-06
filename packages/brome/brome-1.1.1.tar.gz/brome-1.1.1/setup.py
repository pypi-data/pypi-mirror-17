#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = []
with open('requirements.txt', 'r') as fd:
    for line in fd:
        requirements.append(line)

setup(
    name='brome',
    version='1.1.1',
    description="Selenium Framework",
    long_description=readme,
    author="Jean-Francois Parent",
    author_email='parent.j.f@gmail.com',
    url='https://github.com/jf-parent/brome',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords=['brome', 'selenium'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 3.5",
    ]
)
