from django import forms
from django.conf import settings
from django.utils.encoding import force_str
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from .models import AnyLink


class AnyLinkAdminForm(forms.ModelForm):

    confirmation = forms.BooleanField(
        label=_('Confirmation'), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = AnyLink
        fields = '__all__'

    def clean(self):
        data = self.cleaned_data

        if self.instance.pk and getattr(settings, 'ANYLINK_ALLOW_MULTIPLE_USE', False):
            objects = self.instance.get_used_by()
            if len(objects) > 1 and not data.get('confirmation'):
                self.fields['confirmation'].widget = forms.CheckboxInput()
                self.fields['confirmation'].required = True
                self.fields['confirmation'].label = gettext('Please confirm your changes.')

                objects_used = u', '.join([force_str(obj) for obj in objects])
                msg = gettext(
                    u'The following objects are using this link already: {0}').format(
                        objects_used)
                raise forms.ValidationError(msg)
        return data
