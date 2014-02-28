from __future__ import unicode_literals
from django import forms
from django.db import models

from .widgets import AnyLinkAddOrChangeWidget


class AnyLinkAddOrChangeField(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = AnyLinkAddOrChangeWidget(kwargs.pop('rel'))
        super(AnyLinkAddOrChangeField, self).__init__(*args, **kwargs)


class AnyLinkField(models.ForeignKey):
    def __init__(self, verbose_name='Link', to='anylink.AnyLink', **kwargs):
        super(AnyLinkField, self).__init__(to, verbose_name=verbose_name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': AnyLinkAddOrChangeField,
            'rel': self.rel,
        }
        defaults.update(kwargs)
        return super(AnyLinkField, self).formfield(**defaults)
