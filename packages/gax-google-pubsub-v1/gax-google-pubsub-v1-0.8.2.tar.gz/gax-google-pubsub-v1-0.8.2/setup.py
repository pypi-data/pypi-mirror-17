"""A setup module for the GAX Pubsub library.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
import sys

install_requires = [
    'googleapis-common-protos>=1.1.0, <1.2.0',
    'google-gax>=0.12.5, <0.13.0',
    'grpc-google-pubsub-v1>=0.8.1, <0.9.0',
    'oauth2client>=1.4.11',
]

setup(
    name='gax-google-pubsub-v1',
    version='0.8.2',
    author='Google Inc',
    author_email='googleapis-packages@google.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    description='GAX library for the Google Pubsub API',
    include_package_data=True,
    long_description=open('README.rst').read(),
    install_requires=install_requires,
    license='Apache-2.0',
    packages=find_packages(),
    namespace_packages=['google', 'google.cloud', 'google.cloud.pubsub', ],
    url='https://github.com/googleapis/googleapis'
)
