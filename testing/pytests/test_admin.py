from __future__ import unicode_literals

import json

import mock
import pytest

from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.forms.models import ModelForm, modelform_factory
from django.utils.encoding import force_text

from anylink.admin import AnyLinkAdmin
from anylink.models import AnyLink

from testing.testproject.models import TestModel, AnotherTestModel


TestForm = modelform_factory(TestModel, exclude=[])


class MyCustomAnyLinkForm(ModelForm):

    class Meta:
        model = AnyLink
        exclude = ()


@pytest.mark.django_db
class TestAnyLinkAdmin:
    edit_url = '/admin/anylink/anylink/{0}/'

    def setup(self):
        self.modeladmin = AnyLinkAdmin(AnyLink, admin.site)
        self.edit_url = '/admin/anylink/anylink/{0}/change/'

    def test_form_can_be_customized(self, rf, settings, admin_client):
        req = rf.get('/')
        req.user = User.objects.get(pk=admin_client.session['_auth_user_id'])
        assert issubclass(self.modeladmin.get_form(req), ModelForm)

        settings.ANYLINK_ADMIN_FORM = 'testing.pytests.test_admin.MyCustomAnyLinkForm'
        assert issubclass(self.modeladmin.get_form(req), MyCustomAnyLinkForm)

    def test_model_perms(self, rf):
        request = rf.get('/')
        request.user = mock.Mock()
        request.user.has_perm.return_value = False
        assert self.modeladmin.get_model_perms(request) == {
            'add': False,
            'change': False,
            'delete': False,
        }

        request.user.has_perm.return_value = True
        assert self.modeladmin.get_model_perms(request) == {
            'add': False,
            'change': True,
            'delete': True,
        }

    def test_is_rtelink_popup(self, rf):
        assert self.modeladmin.is_rtelink_popup(rf.post('/?ed=ed1', data={
            'foo': 'bar'
        })) is False
        assert self.modeladmin.is_rtelink_popup(rf.post('/?foo=ed1', data={
            '_popup': '1'
        })) is False
        assert self.modeladmin.is_rtelink_popup(rf.post('/?ed=/ed1', data={
            '_popup': '1'
        })) is False
        assert self.modeladmin.is_rtelink_popup(rf.post('/?ed=ed1', data={
            '_popup': '1'
        })) is True

    def test_is_addorchange_popup(self, rf):
        assert self.modeladmin.is_addorchange_popup(rf.post('/?aoc=1', data={
            'foo': 'bar'
        })) is False
        assert self.modeladmin.is_addorchange_popup(rf.post('/?foo=1', data={
            '_popup': '1'
        })) is False
        assert self.modeladmin.is_addorchange_popup(rf.post('/?aoc=1', data={
            '_popup': '1'
        })) is True

    def test_response_rtelink_popup_add(self, admin_client):
        response = admin_client.post('/admin/anylink/anylink/add/?ed=ed1', data={
            '_popup': '1',
            'link_type': 'external_url',
            'target': '_self',
            'external_url': 'http://test.de'
        })

        assert response.status_code == 200
        assert (
            "opener.tinymce.plugins.AnyLink.popupCallback('ed1', '{0}');"
        ).format(AnyLink.objects.get().get_rtelink_id()) in force_text(response.content)

    def test_response_addorchange_popup_add(self, admin_client):
        response = admin_client.post('/admin/anylink/anylink/add/?aoc=1', data={
            '_popup': '1',
            'link_type': 'external_url',
            'target': '_self',
            'external_url': 'http://test.de/'
        })

        assert response.status_code == 200
        assert (
            "opener.AnyLinkAddOrChangeWidget.callback(window, {0}, 'http://test.de/')"
        ).format(AnyLink.objects.get().pk) in force_text(response.content)

    def test_response_popup_add(self, admin_client):
        response = admin_client.post('/admin/anylink/anylink/add/', data={
            '_popup': '1',
            'link_type': 'external_url',
            'target': '_self',
            'external_url': 'http://test.de/'
        })

        assert response.status_code == 200
        assert 'data-popup-response=' in force_text(response.content)
        assert 'http://test.de/' in force_text(response.content)

    def test_response_rtelink_popup_change(self, admin_client):
        obj = AnyLink.objects.create(link_type='external_url', external_url='http://foo')

        edit_url = '{0}?ed=ed1'.format(self.edit_url)

        response = admin_client.post(edit_url.format(obj.pk), data={
            '_popup': '1',
            'link_type': 'external_url',
            'target': '_self',
            'external_url': 'http://test.de/'
        })

        assert response.status_code == 200
        assert (
            "opener.tinymce.plugins.AnyLink.popupCallback('ed1', '{0}');"
        ).format(AnyLink.objects.get().get_rtelink_id()) in force_text(response.content)

    def test_response_addorchange_popup_change(self, admin_client):
        obj = AnyLink.objects.create(link_type='external_url', external_url='http://foo')

        edit_url = '{0}?aoc=1'.format(self.edit_url)

        response = admin_client.post(edit_url.format(obj.pk), data={
            '_popup': '1',
            'link_type': 'external_url',
            'target': '_self',
            'external_url': 'http://test.de/'
        })

        assert response.status_code == 200
        assert (
            "opener.AnyLinkAddOrChangeWidget.callback(window, {0}, 'http://test.de/')"
        ).format(AnyLink.objects.get().pk) in force_text(response.content)

    def test_response_popup_change(self, admin_client):
        obj = AnyLink.objects.create(link_type='external_url', external_url='http://foo')
        response = admin_client.post(self.edit_url.format(obj.pk), data={
            '_popup': '1',
            'link_type': 'external_url',
            'target': '_self',
            'external_url': 'http://test.de/'
        })

        context_data = json.loads(response.context_data['popup_response_data'])

        assert response.status_code == 200
        assert context_data == {
            'action': 'change',
            'new_value': '1',
            'obj': 'http://test.de/',
            'value': '1'
        }

    def test_change_view_context(self, admin_client, settings):
        obj = AnyLink.objects.create(link_type='external_url', external_url='http://foo')
        response = admin_client.get(self.edit_url.format(obj.pk))

        assert response.status_code == 200
        assert len(response.context_data['link_extensions']) == len(settings.ANYLINK_EXTENSIONS)

    def test_change_view_reusable_disabled(self, admin_client, settings):
        settings.ANYLINK_ALLOW_MULTIPLE_USE = False

        obj = AnyLink.objects.create(link_type='external_url', external_url='http://foo/')
        response = admin_client.get(self.edit_url.format(obj.pk))

        assert response.status_code == 200
        field = response.context['adminform'].form.fields['confirmation']
        assert not field.required
        assert isinstance(field.widget, forms.HiddenInput)

    def test_change_view_reusable_enabled(self, admin_client, settings):
        settings.ANYLINK_ALLOW_MULTIPLE_USE = True

        link1 = AnyLink.objects.create(link_type='external_url', external_url='http://foo1/')
        link2 = AnyLink.objects.create(link_type='external_url', external_url='http://foo2/')

        obj1 = TestModel.objects.create(link=link1)
        obj2 = TestModel.objects.create(link=link1)
        obj3 = TestModel.objects.create(link=link2)
        obj4 = AnotherTestModel.objects.create(link=link1)

        data = {
            '_popup': '1',
            'link_type': 'external_url',
            'target': '_self',
            'external_url': 'http://test.de/'
        }
        response = admin_client.post(self.edit_url.format(link1.pk), data=data)

        assert response.status_code == 200
        form = response.context['adminform'].form
        assert not form.is_valid()
        field = form.fields['confirmation']
        assert field.required
        assert isinstance(field.widget, forms.CheckboxInput)
        assert str(obj1) in form.errors['__all__'][0]
        assert str(obj2) in form.errors['__all__'][0]
        assert str(obj3) not in form.errors['__all__'][0]
        assert str(obj4) in form.errors['__all__'][0]
