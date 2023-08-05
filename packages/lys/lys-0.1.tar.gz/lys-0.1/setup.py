# -*- coding: utf-8 -*-
from setuptools import setup

def readme():
    return open('README.rst').read()

setup(
    name='lys',
    version='0.1',
    description='Simple HTML templating for Python',
    long_description=readme(),
    url='http://github.com/mdamien/lys',
    author='Damien MARIÉ',
    author_email='damien@dam.io',
    test_suite='nose.collector',
    tests_require=['nose'],
    license='MIT',
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
    ),
    packages=['lys'],
    zip_safe=False
)
