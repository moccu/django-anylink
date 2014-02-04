from django.db import models
from django.template.defaultfilters import slugify

from anylink.fields import AnyLinkField


class LinkableObject(models.Model):
    description = models.CharField(max_length=255)

    def __unicode__(self):
        return self.description

    def get_absolute_url(self):
        return u'/{0}/{1}/'.format(self.pk, slugify(self.description))


class Linklist(models.Model):
    description = models.CharField(max_length=255)

    def __unicode__(self):
        return self.description


class Link(models.Model):
    linklist = models.ForeignKey(Linklist)

    link = AnyLinkField()

    def __unicode__(self):
        return unicode(self.link)
