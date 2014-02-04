from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.base import ModelBase
from django.utils.functional import curry
from django.utils.module_loading import import_by_path
from django.utils.translation import gettext_lazy as _


SELF, BLANK, PARENT, TOP = ('_self', '_blank', '_parent', '_top')
TARGET_CHOICES = (
    (SELF, _('same window')),
    (BLANK, _('new window')),
    (PARENT, _('parent frame')),
    (TOP, _('top frame')),
)


class AnyLinkMetaclass(ModelBase):
    def __new__(mcs, *args, **kwargs):
        cls = super(AnyLinkMetaclass, mcs).__new__(mcs, *args, **kwargs)

        cls.extensions = {}
        cls.extension_choices = []
        for extension in getattr(settings, 'ANYLINK_EXTENSIONS', []):
            extension_kwargs = {}

            if not isinstance(extension, basestring):
                extension_kwargs = extension[1]
                extension = extension[0]

            extension = import_by_path(extension)(**extension_kwargs)

            extension_name = extension.get_name().lower()

            if extension_name in cls.extensions:
                raise ImproperlyConfigured(
                    'AnyLink extension named "{0}" already exists.'.format(
                        extension_name))

            cls.extensions[extension_name] = extension
            cls.extension_choices.append((extension_name, extension.get_verbose_name()))
            extension.configure_model(cls)

        link_type = cls._meta.get_field('link_type')
        link_type.choices.extend(cls.extension_choices)

        # Manually add display function.
        cls.get_link_type_display = curry(cls._get_FIELD_display, field=link_type)

        return cls


class AnyLink(models.Model):
    __metaclass__ = AnyLinkMetaclass

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

    def __unicode__(self):
        # return u'{0}: {1}'.format(self.get_link_type_display(), self.get_absolute_url())
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
