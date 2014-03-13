from __future__ import unicode_literals
import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models import signals
from django.utils.module_loading import import_by_path
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible

from . import compat

SELF, BLANK, PARENT, TOP = ('_self', '_blank', '_parent', '_top')
TARGET_CHOICES = (
    (SELF, _('same window')),
    (BLANK, _('new window')),
    (PARENT, _('parent frame')),
    (TOP, _('top frame')),
)


def do_anylink_extension_setup(sender, **kwargs):
    if sender is not AnyLink and not issubclass(sender, AnyLink):
        return

    from .admin import admin as anylink_admin

    extensions = {}

    for extension in getattr(settings, 'ANYLINK_EXTENSIONS', []):
        extension_kwargs = {}

        if not isinstance(extension, six.text_type):
            extension_kwargs = extension[1]
            extension = extension[0]

        extension = import_by_path(extension)(**extension_kwargs)

        extension_name = extension.get_name().lower()

        if extension_name in extensions:
            raise ImproperlyConfigured(
                'AnyLink extension named "{0}" already exists.'.format(
                    extension_name))

        extensions[extension_name] = extension
        extension.configure_model(sender)

    choices = [(name, verbose) for name, verbose in extensions.items()]

    sender.extensions = extensions
    sender.extension_choices = choices

    link_type = sender._meta.get_field('link_type')
    link_type.choices.extend(sender.extension_choices)

    # Manually add display function.
    sender.get_link_type_display = curry(sender._get_FIELD_display, field=link_type)

    # Configure django modeladmin
    has_admin = compat.is_installed('django.contrib.admin')

    if has_admin:
        for extension in list(sender.extensions.values()):

            modeladmin = anylink_admin.site._registry.get(sender, None)
            if modeladmin:
                extension.configure_modeladmin(modeladmin)


# In Django 1.7 anylink extensions get initialized in anylink.apps
if django.VERSION[:2] < (1, 7):
    signals.class_prepared.connect(do_anylink_extension_setup)


@python_2_unicode_compatible
class AnyLink(models.Model):
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
