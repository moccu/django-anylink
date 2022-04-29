import codecs
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as test_command


version = '2.0.1'


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    print('You probably want to also tag the version now:')
    print('  git tag -a %s -m "version %s"' % (version, version))
    print('  git push --tags')
    sys.exit()


test_requires = [
    'pytest',
    'pytest-cache',
    'pytest-cov',
    'pytest-flakes',
    'pytest-pycodestyle',
    'pytest-isort',
    'pytest-django',
    'coverage',
    'tox',
]


install_requires = [
    'Django<4',
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Framework :: Django',
    ],
    zip_safe=False,
)
