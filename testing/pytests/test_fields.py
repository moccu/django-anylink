from __future__ import unicode_literals
from django.forms.models import modelform_factory

from anylink.widgets import AnyLinkAddOrChangeWidget

from testing.testproject.models import TestModel


def test_anylinkfield():
    form_class = modelform_factory(TestModel)
    assert isinstance(
        form_class().fields['link'].widget, AnyLinkAddOrChangeWidget)
