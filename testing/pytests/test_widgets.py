from __future__ import unicode_literals
import pytest

from django.forms.models import modelform_factory

from anylink.models import AnyLink

from testing.testproject.models import DummyModel


DummyForm = modelform_factory(DummyModel, exclude=[])


@pytest.mark.django_db
class TestAnyLinkAddOrChangeWidget:

    def test_form_output_empty(self):
        out = DummyForm().as_p()
        assert out == (
            '<p><label for="id_link">Link:</label> <input type="hidden" name="l'
            'ink" required id="id_link" /><strong id="name_id_link"></strong>&nbsp;<a hr'
            'ef="/admin/anylink/anylink/?_to_field=id" class="anylink-button sh'
            'ow-popup" id="lookup_id_link" onclick="return window.AnyLinkAddOrCh'
            'angeWidget.show(this, true);" data-add="Add link" data-change="Ch'
            'ange link">Add link</a>&nbsp;<img src="/static/admin/img/icon-deletelink.svg" id="'
            'delete_id_link" onclick="return window.AnyLinkAddOrChangeWidget.de'
            'lete(this);" style="cursor:pointer;display:none" /></p>'
        )

    def test_form_output_with_instance(self):
        link = AnyLink.objects.create(
            link_type='external_url', external_url='/fake/')
        obj = DummyModel.objects.create(link=link)

        form = DummyForm(instance=obj)
        assert form.as_p() == (
            '<p><label for="id_link">Link:</label> <input type="hidden" name="li'
            'nk" value="1" required id="id_link" /><strong id="name_id_link">/fake/</'
            'strong>&nbsp;<a href="/admin/anylink/anylink/?_to_field=id" class="a'
            'nylink-button show-popup" id="lookup_id_link" onclick="return wind'
            'ow.AnyLinkAddOrChangeWidget.show(this, true);" data-add="Add link"'
            ' data-change="Change link">Change link</a>&nbsp;<img src="/static/'
            'admin/img/icon-deletelink.svg" id="delete_id_link" onclick="return window.AnyLinkA'
            'ddOrChangeWidget.delete(this);" style="cursor:pointer" /></p>'
        )

    def test_form_media(self):
        out = str(DummyForm().media)
        assert out == (
            '<script type="text/javascript" src="/static/anylink/anylink-'
            'addorchangewidget.js"></script>'
        )
