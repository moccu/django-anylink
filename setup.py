import codecs
import os
from setuptools import setup, find_packages


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-anylink',
    version='0.0.1',
    description='Generic links for Django models.',
    long_description=read('README.md'),
    author='Moccu',
    author_email='info@moccu.com',
    url='https://github.com/moccu/django-anylink/',
    packages=find_packages(exclude=[
        'testing',
        'testing.pytests',
        'examples',
    ]),
    package_data={
        'anylink': [
            'static/anylink/*.js',
            'static/tiny_mce/plugins/anylink/*/*',
            'templates/admin/anylink/anylink/*'
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
)
