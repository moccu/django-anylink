.. _usage:

Usage
=====

Before you can use `django-anylink`, you have to install the module and
configure it. Please see :ref:`installation` for more details.

Adding an link to your model
----------------------------

To add a link field to your model, just use the ``AnyLinkField``

.. code-block:: python

    from django.db import models

    from anylink.fields import AnyLinkField


    class MyModel(models.Model):
        whatever = models.CharField(max_length=255)

        link = AnyLinkField()

Now, you have an ``link`` field in your model. This link field is a
``ForeignKey`` internally.

Get the link url and other attributes
-------------------------------------

Lets assume, you implemented your Django model like the example above.
Here is a example, how you would access the attributes of the link.

.. code-block:: python

    url = obj.link.get_absolute_url()  # URL to link.
    name = obj.link.text  # link text/link name
    title = obj.link.title  # title attribute of the link
    target = obj.link.target  # target of the link, for example _self or _blank
    css_class = obj.link.css_class  # optional css class

.. hint::

    Please remember, only the ``get_absolute_url`` method and ``target`` always
    return a values. All other attributes (``text``, ``title``, ``css_class``
    can be blank.

Please see the example projects for more details.
