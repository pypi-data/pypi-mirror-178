# -*- coding: UTF-8 -*-

import setuptools
from setuptools import setup, find_packages

# read the contents of your README file
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="napalm-aruba505",
    version="0.0.163",
    author="David Johnnes",
    author_email="david.johnnes@gmail.com",
    description=("Network Automation and Programmability Abstraction Layer driver for ArubaOs Wi-Fi devices: [505,505H, 515] "),
    keywords="napalm driver",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
    ],
    url="https://github.com/djohnnes/napalm-arubaOS",
    include_package_data=True,
    install_requires=('napalm>=3.*',),
)   
