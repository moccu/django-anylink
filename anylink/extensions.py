from __future__ import unicode_literals
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from .compat import get_model


@python_2_unicode_compatible
class BaseLink(object):
    name = None
    verbose_name = None
    provided_fields = None

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def get_name(self):
        return self.kwargs.get(
            'name', self.name or self.__class__.__name__.lower())

    def get_verbose_name(self):
        retval = self.kwargs.get('verbose_name', None)
        if retval is None and self.verbose_name is not None:
            retval = self.verbose_name
        return retval or self.__class__.__name__

    def __str__(self):
        return self.get_verbose_name()

    def configure_model(self, model):
        pass

    def configure_modeladmin(self, modeladmin):
        pass

    def get_absolute_url(self, obj):
        raise NotImplementedError('`get_absolute_url` is not implemented yet')

    def get_provided_fields(self):
        return self.provided_fields or (self.get_name(),)

    def clean(self, link):
        if not getattr(link, self.get_name()):
            raise ValidationError(_('{0} is required').format(self.get_verbose_name()))


class ExternalLink(BaseLink):
    name = 'external_url'
    verbose_name = _('external url')
    provided_fields = ('external_url',)

    def configure_model(self, model):
        model.add_to_class(
            self.get_name(),
            models.URLField(self.get_verbose_name(), max_length=255, blank=True)
        )

    def get_absolute_url(self, link):
        return getattr(link, self.get_name()) or None


class ModelLink(BaseLink):
    def __init__(self, **kwargs):
        super(ModelLink, self).__init__(**kwargs)

        if 'model' not in self.kwargs:
            raise ImproperlyConfigured('Please provide a model path')

        self.model = get_model(*self.kwargs['model'].split('.', 1))

        if not hasattr(self.model, 'get_absolute_url'):
            raise ImproperlyConfigured(
                '{0} does not implement `get_absolute_url`'.format(
                    self.model.__name__))

    def get_name(self):
        return self.kwargs.get('name', self.model.__name__.lower())

    def get_verbose_name(self):
        return self.kwargs.get('verbose_name', self.model._meta.verbose_name)

    def configure_model(self, model):
        model.add_to_class(self.get_name(), models.ForeignKey(
            self.model, blank=True, null=True, verbose_name=self.get_verbose_name()))

    def configure_modeladmin(self, modeladmin):
        modeladmin.raw_id_fields = list(modeladmin.raw_id_fields) + [self.get_name()]

    def get_absolute_url(self, link):
        obj = getattr(link, self.get_name())
        return obj and str(obj.get_absolute_url()) or None
