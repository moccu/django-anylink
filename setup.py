from __future__ import unicode_literals
import codecs
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as test_command


version = '0.4.0'


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    print('You probably want to also tag the version now:')
    print('  git tag -a %s -m "version %s"' % (version, version))
    print('  git push --tags')
    sys.exit()


test_requires = [
    'py>=1.4.26',
    'pyflakes==1.1.0',
    'pytest>=2.8.0',
    'pytest-cache>=1.0',
    'pytest-cov>=2.1.0',
    'pytest-flakes>=1.0.1',
    'pytest-pep8>=1.0.6',
    'pytest-django>=2.8.0',
    'coverage>=4.0',
    'mock>=1.3.0',
    'pep8>=1.6.2',
    'tox',
    'tox-pyenv',
]


install_requires = [
    'Django>=1.6',
]


docs_requires = [
    'sphinx',
    'sphinx_rtd_theme'
]


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


class PyTest(test_command):

    def finalize_options(self):
        test_command.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='django-anylink',
    version=version,
    description='Generic links for Django models.',
    long_description=read('README.rst') + '\n\n' + read('CHANGES.rst'),
    author='Moccu GmbH & Co. KG',
    author_email='info@moccu.com',
    url='https://github.com/moccu/django-anylink/',
    extras_require={
        'docs': docs_requires,
        'tests': test_requires,
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Framework :: Django',
    ],
    zip_safe=False,
)
