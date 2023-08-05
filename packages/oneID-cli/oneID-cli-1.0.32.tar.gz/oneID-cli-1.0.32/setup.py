import os

from setuptools import setup, find_packages
from codecs import open


base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, "README.rst")) as f:
    long_description = f.read()

setup(
    name='oneID-cli',
    version='1.0.32',
    description='oneID-cli is a command line interface for oneID Connect',
    long_description=long_description,
    url='https://www.oneID.com',
    author='oneID Inc.',
    author_email='support@oneID.com',
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        'Topic :: Security :: Cryptography',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='oneID IoT Identity Authentication',
    package_dir={"": "src"},
    packages=find_packages(where='src',
                           exclude=['contrib', 'docs', 'tests*',
                                    'venv', 'example*']),
    install_requires=['oneID-connect>=0.11.0,<0.12',
                      'requests[security]>=2.9.1,<2.10',
                      'ruamel.yaml>=0.12.5,<0.13'],
    scripts=['bin/oneid-cli'],

)
