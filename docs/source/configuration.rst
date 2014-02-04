.. _configuration:

Configuration
=============

Luckily you don't have to configure that much to use `django-anylink`.

``ANYLINK_EXTENSIONS``
----------------------

To add a new link target, you have to update the ``ANYLINK_EXTENSIONS``
setting.

This directive is a list of linkable target (external urls, Django models with
``get_absolute_url`` methods and so on). Every entry can be a single class path
or a tuple consisting of a class path and a configuration dictionary.

ExternalLink
````````````

This extension provides a external url field. No other configuration is needed.

.. code-block:: python

    # Example with external links
    ANYLINK_EXTENSIONS = (
        'anylink.extensions.ExternalLink',
    )

ModelLink
`````````

The ModelLink extension provides a foreign key the configured model. It is
required that the model is registered in the Django admin interface. Also, the
model needs to have a ``get_absolute_url`` method.

.. code-block:: python

    # Example with model links with MyModel
    ANYLINK_EXTENSIONS = (
        ('anylink.extensions.ModelLink', {'model': 'myapp.MyModel'}),
    )

For details on writing your own extensions, please see the :ref:`extension` section.
