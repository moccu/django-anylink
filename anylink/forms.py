from django import forms
from django.conf import settings
from django.utils.encoding import force_text
from django.utils.translation import ugettext

from .compat import add_error
from .models import AnyLink


class AnyLinkAdminForm(forms.ModelForm):

    confirmation = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = AnyLink

    def clean(self):
        data = self.cleaned_data

        if self.instance.pk and getattr(settings, 'ANYLINK_ALLOW_MULTIPLE_USE', False):
            objects = self.instance.get_used_by()
            if len(objects) > 1 and not data.get('confirmation'):
                self.fields['confirmation'].widget = forms.CheckboxInput()
                self.fields['confirmation'].required = True
                add_error(self, 'confirmation', ugettext('Confirm your changes.'), data)

                objects_used = u', '.join([force_text(obj) for obj in objects])
                msg = ugettext(u'The following objects are using this link already: {0}'.format(
                    objects_used))
                raise forms.ValidationError(msg)
        return data
