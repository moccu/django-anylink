from anylink.fields import AnyLinkField
from django.db import models
from django.template.defaultfilters import slugify


class LinkableObject(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return u'/{0}/{1}/'.format(self.pk, slugify(self.description))


class DummyModel(models.Model):
    link = AnyLinkField()

    def __str__(self):
        return '[{0}] - {1}'.format(self.pk, self.link)


class AnotherDummyModel(models.Model):
    link = AnyLinkField()

    def __str__(self):
        return '[{0}] - {1}'.format(self.pk, self.link)
