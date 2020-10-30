from anylink.widgets import AnyLinkAddOrChangeWidget
from django.forms.models import modelform_factory

from testing.testproject.models import DummyModel


def test_anylinkfield():
    form_class = modelform_factory(DummyModel, fields='__all__')
    assert isinstance(
        form_class().fields['link'].widget, AnyLinkAddOrChangeWidget)
