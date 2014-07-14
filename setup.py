from __future__ import unicode_literals
import codecs
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


test_requires = [
    'py>=1.4.20',
    'pyflakes>=0.7.3',
    'pytest>=2.5.2',
    'pytest-cache>=1.0',
    'pytest-cov>=1.6',
    'pytest-flakes==0.2',
    'pytest-pep8==1.0.5',
    'pytest-django==2.6',
    'coverage==3.7.1',
    'mock==1.0.1',
    'pep8==1.4.6',
]


install_requires = [
    'Django>=1.5',
]


dev_requires = [
    'tox',
]


docs_requires = [
    'sphinx',
    'sphinx_rtd_theme'
]


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='django-anylink',
    version='0.1.0',
    description='Generic links for Django models.',
    long_description=read('README.rst') + '\n\n' + read('CHANGES.rst'),
    author='Moccu GmbH & Co. KG',
    author_email='info@moccu.com',
    url='https://github.com/moccu/django-anylink/',
    extras_require={
        'docs': docs_requires,
        'tests': test_requires,
        'dev': dev_requires,
    },
    tests_require=test_requires,
    install_requires=install_requires,
    cmdclass={'test': PyTest},
    packages=find_packages(exclude=[
        'testing',
        'testing.pytests',
        'testing.testproject',
        'examples',
    ]),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Framework :: Django',
    ],
    zip_safe=False,
)
