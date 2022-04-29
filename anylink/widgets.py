from django import forms
from django.conf import settings
from django.contrib import admin
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


ICON_FILENAME = 'icon-deletelink.svg'

CHANGE_LINK = (
    u'<a href="{0}{1}" class="anylink-button show-popup" id="lookup_id_{2}" '
    u'onclick="return window.AnyLinkAddOrChangeWidget.show(this);" '
    u'data-add="{3}" data-change="{4}">{5}</a>'
)

SELECT_LINK = (
    u'&nbsp;<a href="{0}{1}" class="anylink-button show-popup" id="lookup_id_{2}" '
    u'onclick="return window.AnyLinkAddOrChangeWidget.select(this);">{3}</a>'
)

DELETE_IMG = (
    u'&nbsp;<img src="{0}admin/img/' + ICON_FILENAME + u'" id="delete_id_{1}" '
    u'onclick="return window.AnyLinkAddOrChangeWidget.delete(this);" '
    u'style="cursor:pointer{2}" />'
)


class AnyLinkAddOrChangeWidget(forms.TextInput):
    input_type = 'hidden'

    # We need to pretend that our widget is a non-hidden input to ensure Django
    # doesn't remove the form-row.
    is_hidden = False

    class Media:
        js = ('anylink/anylink-addorchangewidget.js',)

    def __init__(self, remote_field, admin_site=None, attrs=None, using=None):
        self.remote_field = remote_field
        self.admin_site = admin_site or admin.site
        self.db = using
        super(AnyLinkAddOrChangeWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}

        output = [super().render(name, value, attrs, renderer=renderer)]
        output.append(self.label_for_value(name, value))

        if self.remote_field.model in self.admin_site._registry:
            related_url = reverse('admin:{0}_{1}_changelist'.format(
                self.remote_field.model._meta.app_label,
                self.remote_field.model._meta.model_name
            ), current_app=self.admin_site.name)

            params = self.url_parameters()
            if params:
                url_params = '?' + '&amp;'.join(
                    ['%s=%s' % (k, v) for k, v in list(params.items())])
            else:
                url_params = ''

            output.append(CHANGE_LINK.format(
                related_url, url_params, name,
                _('Add link'), _('Change link'),
                not value and _('Add link') or _('Change link')
            ))

            if getattr(settings, 'ANYLINK_ALLOW_MULTIPLE_USE', False):
                output.append(SELECT_LINK.format(
                    related_url, url_params, name,
                    _('Select link'),
                ))

        output.append(self.delete_button(name, value))
        return mark_safe(''.join(output))

    def url_parameters(self):
        from django.contrib.admin.views.main import TO_FIELD_VAR
        return {TO_FIELD_VAR: self.remote_field.get_related_field().name}

    def label_for_value(self, name, value):
        try:
            obj_repr = escape(
                self.remote_field.model._default_manager.using(self.db).get(
                    **{self.remote_field.get_related_field().name: value}
                )
            )
        except (ValueError, self.remote_field.model.DoesNotExist):
            obj_repr = ''

        return u'<strong id="name_id_{0}">{1}</strong>&nbsp;'.format(name, obj_repr)

    def delete_button(self, name, value):
        return DELETE_IMG.format(
            settings.STATIC_URL, name, ';display:none' if not value else '')
