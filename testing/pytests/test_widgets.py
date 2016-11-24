from __future__ import unicode_literals
import pytest

import django
from django.forms.models import modelform_factory

from anylink.models import AnyLink
from anylink.widgets import ICON_FILENAME

from testing.testproject.models import TestModel


TestForm = modelform_factory(TestModel, exclude=[])

requires_django17 = pytest.mark.skipif(
    django.VERSION[:2] < (1, 7),
    reason='Django 1.7 changed form rendering behavior')

skip_django17 = pytest.mark.skipif(
    django.VERSION[:2] >= (1, 7),
    reason='Django 1.7 changed form rendering behavior')


@pytest.mark.django_db
class TestAnyLinkAddOrChangeWidget:

    @requires_django17
    def test_form_output_empty17(self):
        out = TestForm().as_p()
        assert out == (
            '<p><label for="id_link">Link:</label> <input id="id_link" name="li'
            'nk" type="hidden" /><strong id="name_id_link"></strong>&nbsp;<a hr'
            'ef="/admin/anylink/anylink/?_to_field=id" class="anylink-button sh'
            'ow-popup" id="lookup_id_link" onclick="return window.AnyLinkAddOrC'
            'hangeWidget.show(this, {1});" data-add="Add link" data-change="Ch'
            'ange link">Add link</a>&nbsp;<img src="/static/admin/img/{0}" id="'
            'delete_id_link" onclick="return window.AnyLinkAddOrChangeWidget.de'
            'lete(this);" style="cursor:pointer;display:none" /></p>'
        ).format(ICON_FILENAME, ('true' if django.VERSION[:2] >= (1, 9) else 'false'))

    @skip_django17
    def test_form_output_empty(self):
        out = TestForm().as_p()
        assert out == (
            '<p><label for="id_link">Link:</label> <input id="id_link" name="li'
            'nk" type="hidden" /><strong id="name_id_link"></strong>&nbsp;<a hr'
            'ef="/admin/anylink/anylink/?t=id" class="anylink-button show-popup'
            '" id="lookup_id_link" onclick="return window.AnyLinkAddOrChangeWid'
            'get.show(this, false);" data-add="Add link" data-change="Change li'
            'nk">Add link</a>&nbsp;<img src="/static/admin/img/{0}" id="delete_'
            'id_link" onclick="return window.AnyLinkAddOrChangeWidget.delete(th'
            'is);" style="cursor:pointer;display:none" /></p>'
        ).format(ICON_FILENAME)

    @requires_django17
    def test_form_output_with_instance17(self):
        link = AnyLink.objects.create(
            link_type='external_url', external_url='/fake/')
        obj = TestModel.objects.create(link=link)

        form = TestForm(instance=obj)
        assert form.as_p() == (
            '<p><label for="id_link">Link:</label> <input id="id_link" name="li'
            'nk" type="hidden" value="1" /><strong id="name_id_link">/fake/</st'
            'rong>&nbsp;<a href="/admin/anylink/anylink/?_to_field=id" class="a'
            'nylink-button show-popup" id="lookup_id_link" onclick="return wind'
            'ow.AnyLinkAddOrChangeWidget.show(this, {1});" data-add="Add link"'
            ' data-change="Change link">Change link</a>&nbsp;<img src="/static/'
            'admin/img/{0}" id="delete_id_link" onclick="return window.AnyLinkA'
            'ddOrChangeWidget.delete(this);" style="cursor:pointer" /></p>'
        ).format(ICON_FILENAME, ('true' if django.VERSION[:2] >= (1, 9) else 'false'))

    @skip_django17
    def test_form_output_with_instance(self):
        link = AnyLink.objects.create(
            link_type='external_url', external_url='/fake/')
        obj = TestModel.objects.create(link=link)

        form = TestForm(instance=obj)
        assert form.as_p() == (
            '<p><label for="id_link">Link:</label> <input id="id_link" name="li'
            'nk" type="hidden" value="1" /><strong id="name_id_link">/fake/</st'
            'rong>&nbsp;<a href="/admin/anylink/anylink/?t=id" class="anylink-b'
            'utton show-popup" id="lookup_id_link" onclick="return window.AnyLi'
            'nkAddOrChangeWidget.show(this, false);" data-add="Add link" data-c'
            'hange="Change link">Change link</a>&nbsp;<img src="/static/admin/i'
            'mg/{0}" id="delete_id_link" onclick="return window.AnyLinkAddOrCha'
            'ngeWidget.delete(this);" style="cursor:pointer" /></p>'
        ).format(ICON_FILENAME)

    def test_form_media(self):
        out = str(TestForm().media)
        assert out == (
            '<script type="text/javascript" src="/static/anylink/anylink-'
            'addorchangewidget.js"></script>'
        )
