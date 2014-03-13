from __future__ import unicode_literals
import pytest

import django
from django.forms.models import modelform_factory

from anylink.models import AnyLink

from testing.testproject.models import TestModel


TestForm = modelform_factory(TestModel, exclude=[])

requires_django17 = pytest.mark.skipif(django.VERSION[:2] < (1, 7),
    reason='Django 1.7 changed form rendering behavior')

skip_django17 = pytest.mark.skipif(django.VERSION[:2] >= (1, 7),
    reason='Django 1.7 changed form rendering behavior')



@pytest.mark.django_db
class TestAnyLinkAddOrChangeWidget:

    @requires_django17
    def test_form_output_empty17(self):
        out = TestForm().as_p()
        assert out == (
            '<input id="id_link" name="l'
            'ink" type="hidden" /><strong id="name_id_link"></strong>&nbsp;<a '
            'href="/admin/anylink/anylink/?_to_field=id" class="show-popup" id="lookup'
            '_id_link" onclick="return window.AnyLinkAddOrChangeWidget.show(th'
            'is);" data-add="Add link" data-change="Change link">Add link</a>&'
            'nbsp;<img src="/static/admin/img/icon_deletelink.gif" id="delete_'
            'id_link" onclick="return window.AnyLinkAddOrChangeWidget.delete(t'
            'his);" style="cursor:pointer;display:none" />'
        )

    @skip_django17
    def test_form_output_empty(self):
        out = TestForm().as_p()
        assert out == (
            '<p><label for="id_link">Link:</label> <input id="id_link" name="l'
            'ink" type="hidden" /><strong id="name_id_link"></strong>&nbsp;<a '
            'href="/admin/anylink/anylink/?t=id" class="show-popup" id="lookup'
            '_id_link" onclick="return window.AnyLinkAddOrChangeWidget.show(th'
            'is);" data-add="Add link" data-change="Change link">Add link</a>&'
            'nbsp;<img src="/static/admin/img/icon_deletelink.gif" id="delete_'
            'id_link" onclick="return window.AnyLinkAddOrChangeWidget.delete(t'
            'his);" style="cursor:pointer;display:none" /></p>'
        )

    @requires_django17
    def test_form_output_with_instance17(self):
        link = AnyLink.objects.create(
            link_type='external_url', external_url='/fake/')
        obj = TestModel.objects.create(link=link)

        form = TestForm(instance=obj)
        assert form.as_p() == (
            '<input id="id_link" name="l'
            'ink" type="hidden" value="1" /><strong id="name_id_link">/fake/</'
            'strong>&nbsp;<a href="/admin/anylink/anylink/?_to_field=id" class="show-p'
            'opup" id="lookup_id_link" onclick="return window.AnyLinkAddOrChan'
            'geWidget.show(this);" data-add="Add link" data-change="Change lin'
            'k">Change link</a>&nbsp;<img src="/static/admin/img/icon_deleteli'
            'nk.gif" id="delete_id_link" onclick="return window.AnyLinkAddOrCh'
            'angeWidget.delete(this);" style="cursor:pointer" />'
        )

    @skip_django17
    def test_form_output_with_instance(self):
        link = AnyLink.objects.create(
            link_type='external_url', external_url='/fake/')
        obj = TestModel.objects.create(link=link)

        form = TestForm(instance=obj)
        assert form.as_p() == (
            '<p><label for="id_link">Link:</label> <input id="id_link" name="l'
            'ink" type="hidden" value="1" /><strong id="name_id_link">/fake/</'
            'strong>&nbsp;<a href="/admin/anylink/anylink/?t=id" class="show-p'
            'opup" id="lookup_id_link" onclick="return window.AnyLinkAddOrChan'
            'geWidget.show(this);" data-add="Add link" data-change="Change lin'
            'k">Change link</a>&nbsp;<img src="/static/admin/img/icon_deleteli'
            'nk.gif" id="delete_id_link" onclick="return window.AnyLinkAddOrCh'
            'angeWidget.delete(this);" style="cursor:pointer" /></p>'
        )

    def test_form_media(self):
        out = str(TestForm().media)
        assert out == (
            '<script type="text/javascript" src="/static/anylink/anylink-'
            'addorchangewidget.js"></script>'
        )
