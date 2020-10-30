Changes
=======

2.0.0 (2020-10-30)
------------------

* Add support for Django 2.1 and 2.2
* Drop support for Python < 3.6


1.0.0 (2018-06-19)
------------------

* Add support for Django 2
* Drop support for Python < 2.7
* Drop support for Django < 1.11


0.4.2 (2016-11-24)
------------------

* Fix AddOrChangeWidget for Django 1.9


0.4.1 (2016-10-04)
------------------

* Fix translation
* Improve message formatting for multi link warning
* Order link_type choices alphabetically to avoid redundant migrations
* Update documentation


0.4.0 (2016-05-11)
------------------

* Add support for django 1.9
* Use SVG if django-version is greater than 1.8


0.3.0 (2015-09-22)
------------------

* Add support for django 1.8 and python3.5
* drop support for django 1.5


0.2.0 (2015-03-30)
------------------

* Integrate Travis CI.
* Allow customization of admin form.
* Ensure the admin widget is not recognized as hidden input.
* Add ``ANYLINK_ALLOW_MULTIPLE_USE`` setting to enable reusability of AnyLink objects.
* We don't check Python 3.3 anymore.
* Added Dutch and German translations.


0.1.0 (2014-06-17)
------------------

* Initial release for the public.

Contains the following features:

* Generic linking in Django
* Support for TinyMCE
* Supports Python 2.7, 3.3, 3.4, PyPy and Django 1.5+
