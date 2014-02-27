from django.forms.models import modelform_factory
from django.db import models

from anylink.fields import AnyLinkField
from anylink.widgets import AnyLinkAddOrChangeWidget


def test_anylinkfield():
    # Force loading of the model.
    models.get_model('anylink', 'AnyLink')

    class TestModel(models.Model):
        link = AnyLinkField()

    form_class = modelform_factory(TestModel)
    assert isinstance(form_class().fields['link'].widget, AnyLinkAddOrChangeWidget)
