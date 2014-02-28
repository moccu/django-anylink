from __future__ import unicode_literals
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible

from anylink.fields import AnyLinkField


@python_2_unicode_compatible
class LinkableObject(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return u'/{0}/{1}/'.format(self.pk, slugify(self.description))


@python_2_unicode_compatible
class TestModel(models.Model):
    link = AnyLinkField()

    def __str__(self):
        return str(self.link)
