from django import forms
from django.conf import settings
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from .compat import get_all_related_objects, add_error
from .models import AnyLink


class AnyLinkAdminForm(forms.ModelForm):

    confirmation = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = AnyLink

    def clean(self):
        data = self.cleaned_data

        if self.instance.pk:
            if settings.ANYLINK_REUSABLE:
                objects = self.in_use(self.instance)
                if len(objects) > 1 and not data.get('confirmation'):
                    objects_used = u', '.join([force_text(obj) for obj in objects])
                    msg = _(u'The following objects are using this link already: {0}'.format(
                        objects_used))
                    self.fields['confirmation'].widget = forms.CheckboxInput()
                    self.fields['confirmation'].required = True
                    add_error(self, 'confirmation', _('Confirm your changes here.'), data)
                    raise forms.ValidationError(msg)
        return data

    def in_use(self, obj):
        used_by = []
        related = get_all_related_objects(AnyLink)
        for rel in related:
            reversed_name = rel.get_accessor_name()
            reversed_manager = getattr(obj, reversed_name)
            used_by.extend(reversed_manager.all())

        return used_by if len(used_by) > 1 else []
