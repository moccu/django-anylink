.. _extension:

Writing your own link extension
===============================

To extend `django-anylink` lets assume you have a Download model. This model
doesn't have a ``get_absolute_url`` method. Theirfore you want to write your own
link extension.

Lets have a look at the code first.

.. code-block:: python

    from django.core.urlresolvers import reverse

    from anylink.extensions import BaseLink


    class DownloadLink(BaseLink):
        def configure_model(self, model):
            # configure_model is called by django-anylink upon initialization.
            # We add a field to anylink model to keep the object reference.
            # Make sure the field is null-able, anylink will ensure its filled out
            # if the link type is set to DownloadLink.
            model.add_to_class(self.get_name(), models.ForeignKey(
                'myapp.Download', blank=True, null=True)

        def get_absolute_url(self, link):
            # Get the obj instance using the get_name method.
            obj = getattr(link, self.get_name())
            # return a reverse'd url or None if no obj is set.
            return obj and reverse('myurl', kwargs={'id': obj.pk}) or None


As you can see here, the Link extension has two important methods.
The ``configure_model`` method and the ``get_absolute_url`` method. Please refer
to the comments and the code for more details on this topic.
