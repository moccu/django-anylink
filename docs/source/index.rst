django-anylink documentation
============================

Generic linking in Django. Includes support for RichText editors like TinyMCE.

What is django-anylink
----------------------

`django-anylink` is a generic linking module for Django. Using this module, you
can create links for many usecases. You'll find yourself just jusing the
``AnyLinkField`` to create links to different Django models or external urls.
You don't have to take care for changing urls. AnyLink resolves links on request.

`django-anylink` provides a Link database, an model field and some handy widgets
for the daily use.

Besides that, `django-anylink` is easy extendable. By default, the module provides
external urls and model links wich have a ``get_absolute_url`` method.

Contents
--------

.. toctree::

   installation
   configuration
   usage
   extension
   contribution

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
