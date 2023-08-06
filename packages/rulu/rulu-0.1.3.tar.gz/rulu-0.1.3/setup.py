import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand
from os import path


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)
    

setup(
    name='rulu',
    version='0.1.3',
    url='http://github.com/ubarkai/rulu',
    license='LGPL',
    author='Uri Barkai',
    author_email='ubarkai@gmail.com',
    description='Python interface for building rule-based expert systems over PyCLIPS',
    install_requires = ['bunch', 'pyclips'],
    tests_require=['pytest'],
    extras_require={'testing': ['pytest']},
    cmdclass={'test': PyTest},
    test_suite='test.test_ruleengine',
    packages=['rulu']
)
