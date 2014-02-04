.. _installation:

Installation
============

To install `django-anylink` just use your preferred Python package installer::

    pip install django-anylink

Add ``anylink`` to your Django settings

.. code-block:: python

    INSTALLED_APPS = (
        # other apps
        'anylink',
    )

Now, you should define at least one link extension, for example external links.

.. code-block:: python


    ANYLINK_EXTENSIONS = (
        'anylink.extensions.ExternalLink',
    )

Furthermore, you should consider using `South` for adding extensions.
Because `South` would try to put the schema migrations inside the Python site
packages directory, add the following (or something similar) to your settings.

.. code-block:: python

    SOUTH_MIGRATION_MODULES = {
        'anylink': 'migrations.anylink',
    }

Details on how to use `django-anylink` in your Django application can be found
in the :ref:`configuration` section.
