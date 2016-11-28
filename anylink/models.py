from __future__ import unicode_literals
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.base import ModelBase
try:
    from django.utils.module_loading import import_string as import_by_path
except ImportError:
    from django.utils.module_loading import import_by_path
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible, force_text

SELF, BLANK = ('_self', '_blank')
TARGET_CHOICES = (
    (SELF, _('same window')),
    (BLANK, _('new window')),
)


def do_anylink_extension_setup(cls, **kwargs):
    extensions = {}

    for extension in getattr(settings, 'ANYLINK_EXTENSIONS', []):
        extension_kwargs = {}

        if not isinstance(extension, six.string_types):
            extension_kwargs = extension[1]
            extension = extension[0]

        extension = import_by_path(extension)(**extension_kwargs)

        extension_name = extension.get_name().lower()

        if extension_name in extensions:
            raise ImproperlyConfigured(
                'AnyLink extension named "{0}" already exists.'.format(
                    extension_name))

        extensions[extension_name] = extension
        extension.configure_model(cls)

    choices = [(name, ext.get_verbose_name()) for name, ext in extensions.items()]

    cls.extensions = extensions
    cls.extension_choices = choices

    link_type = cls._meta.get_field('link_type')
    link_type.choices.extend(cls.extension_choices)
    link_type.choices.sort(key=lambda item: item[0])

    # Manually add display function.
    cls.get_link_type_display = curry(cls._get_FIELD_display, field=link_type)

    # Configure django modeladmin
    has_admin = apps.is_installed('django.contrib.admin')
    anylink_admin = apps.get_app_config('admin').module

    if has_admin:
        for extension in list(cls.extensions.values()):

            modeladmin = anylink_admin.site._registry.get(cls, None)
            if modeladmin:
                extension.configure_modeladmin(modeladmin)


class AnyLinkModelBase(ModelBase):
    """
    Metaclass for all models.
    """
    def __new__(cls, name, bases, attrs):
        new_class = ModelBase.__new__(cls, name, bases, attrs)
        return new_class


@python_2_unicode_compatible
class AnyLink(six.with_metaclass(AnyLinkModelBase, models.Model)):
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
        return force_text(self.get_absolute_url())

    def get_absolute_url(self):
        return self.extensions[self.link_type].get_absolute_url(self)

    def get_rtelink_id(self):
        return '#AL{0}'.format(self.pk)

    def clean(self):
        if self.link_type:
            self.extensions[self.link_type].clean(self)

    def get_used_by(self):
        used_by = []
        related_models = [
            f for f in self.__class__._meta.get_fields()
            if f.one_to_many and f.auto_created
        ]
        for relation in related_models:
            reversed_name = relation.get_accessor_name()
            reversed_manager = getattr(self, reversed_name)
            used_by.extend(reversed_manager.all())

        return used_by


try:
    # If south is available, add rules for anylink field.
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^anylink'])
except ImportError:
    pass
