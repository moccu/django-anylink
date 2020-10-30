import pytest
from anylink.models import AnyLink
from django.forms.models import modelform_factory

from testing.testproject.models import DummyModel


DummyForm = modelform_factory(DummyModel, exclude=[])


@pytest.mark.django_db
class TestAnyLinkAddOrChangeWidget:

    def test_form_output_empty(self):
        out = DummyForm().as_p()
        assert '/admin/anylink/anylink/' in out
        assert 'class="anylink-button show-popup"' in out
        assert 'onclick="return window.AnyLinkAddOrChangeWidget' in out

    def test_form_output_with_instance(self):
        link = AnyLink.objects.create(
            link_type='external_url', external_url='/fake/')
        obj = DummyModel.objects.create(link=link)

        form = DummyForm(instance=obj)
        out = form.as_p()
        assert '/admin/anylink/anylink/' in out
        assert 'class="anylink-button show-popup"' in out
        assert 'onclick="return window.AnyLinkAddOrChangeWidget' in out

    def test_form_media(self):
        out = str(DummyForm().media)
        assert out == (
            '<script type="text/javascript" src="/static/anylink/anylink-'
            'addorchangewidget.js"></script>'
        )
