from __future__ import unicode_literals
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.base import ModelBase
from django.utils.functional import curry
from django.utils.module_loading import import_by_path
from django.utils.translation import ugettext_lazy as _
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible


SELF, BLANK, PARENT, TOP = ('_self', '_blank', '_parent', '_top')
TARGET_CHOICES = (
    (SELF, _('same window')),
    (BLANK, _('new window')),
    (PARENT, _('parent frame')),
    (TOP, _('top frame')),
)


class AnyLinkMetaclass(ModelBase):
    def __new__(cls, name, bases, attrs):
        new_class = super(AnyLinkMetaclass, cls).__new__(cls, name, bases, attrs)

        if not hasattr(new_class, '_meta'):
            return new_class

        new_class.extensions = {}
        new_class.extension_choices = []
        for extension in getattr(settings, 'ANYLINK_EXTENSIONS', []):
            extension_kwargs = {}

            if not isinstance(extension, six.text_type):
                extension_kwargs = extension[1]
                extension = extension[0]

            extension = import_by_path(extension)(**extension_kwargs)

            extension_name = extension.get_name().lower()

            if extension_name in new_class.extensions:
                raise ImproperlyConfigured(
                    'AnyLink extension named "{0}" already exists.'.format(
                        extension_name))

            new_class.extensions[extension_name] = extension
            new_class.extension_choices.append((extension_name, extension.get_verbose_name()))
            extension.configure_model(new_class)

        link_type = new_class._meta.get_field('link_type')
        link_type.choices.extend(new_class.extension_choices)

        # Manually add display function.
        new_class.get_link_type_display = curry(new_class._get_FIELD_display, field=link_type)

        return new_class


@python_2_unicode_compatible
class AnyLink(six.with_metaclass(AnyLinkMetaclass, models.Model)):
    text = models.CharField(_('text'), max_length=150, blank=True)
    title = models.CharField(_('title'), max_length=150, blank=True)
    target = models.CharField(
        _('target'), max_length=7, choices=TARGET_CHOICES, default=SELF)

    css_class = models.CharField(_('css class'), max_length=255, blank=True)

    link_type = models.CharField(
        _('type'), max_length=100, choices=[])

    class Meta:
        verbose_name = _('Link')
        verbose_name_plural = _('Links')

    def __str__(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        return self.extensions[self.link_type].get_absolute_url(self)

    def get_rtelink_id(self):
        return '#AL{0}'.format(self.pk)

    def clean(self):
        if self.link_type:
            self.extensions[self.link_type].clean(self)


try:
    # If south is available, add rules for anylink field.
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^anylink'])
except ImportError:
    pass
