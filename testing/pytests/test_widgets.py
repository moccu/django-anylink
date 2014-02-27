import pytest

from django.forms.models import modelform_factory
from django.db import models

from anylink.fields import AnyLinkField
from anylink.models import AnyLink


class TestModel(models.Model):
    link = AnyLinkField()

TestForm = modelform_factory(TestModel)


@pytest.mark.django_db
class TestAnyLinkAddOrChangeWidget:
    def test_form_output_empty(self):
        out = TestForm().as_p()
        assert out == (
            '<p><label for="id_link">Link:</label> <input id="id_link" '
            'name="link" type="hidden" /><strong id="name_id_link"></strong>'
            '&nbsp;&nbsp;<img src="/static/admin/img/icon_deletelink.gif" '
            'id="delete_id_link" onclick="return window.AnyLinkAddOrChange'
            'Widget.delete(this);" style="cursor:pointer;display:none" /></p>'
        )

    def test_form_output_with_instance(self):
        link = AnyLink.objects.create(
            link_type='external_url', external_url='/fake/')
        obj = TestModel(link=link)

        form = TestForm(instance=obj)
        assert form.as_p() == (
            '<p><label for="id_link">Link:</label> <input id="id_link" '
            'name="link" type="hidden" value="1" /><strong id="name_id_link">'
            '/fake/</strong>&nbsp;&nbsp;<img src="/static/admin/img/icon_'
            'deletelink.gif" id="delete_id_link" onclick="return window.'
            'AnyLinkAddOrChangeWidget.delete(this);" style="cursor:pointer" '
            '/></p>'
        )

    def test_form_media(self):
        out = unicode(TestForm().media)
        assert out == (
            '<script type="text/javascript" src="/static/anylink/anylink-'
            'addorchangewidget.js"></script>'
        )
