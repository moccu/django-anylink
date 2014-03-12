from __future__ import unicode_literals
import mock
import pytest

from django.core.exceptions import ValidationError, ImproperlyConfigured

from anylink.extensions import BaseLink, ExternalLink, ModelLink


class TestBaseLink:
    def test_configure_model(self):
        model_mock = mock.Mock()

        BaseLink().configure_model(model_mock)
        assert len(model_mock.method_calls) == 0

    def test_configure_modeladmin(self):
        model_admin_mock = mock.Mock()

        BaseLink().configure_modeladmin(model_admin_mock)
        assert len(model_admin_mock.method_calls) == 0

    def test_get_absolute_url(self):
        with pytest.raises(NotImplementedError):
            BaseLink().get_absolute_url(mock.Mock())

    def test_get_provided_fields(self):
        link = BaseLink()
        link.name = 'test123'
        assert link.get_provided_fields() == ('test123',)

        link.provided_fields = ('test1', 'test2')
        assert link.get_provided_fields() == ('test1', 'test2')


class TestExternalLink:
    def test_configure_model(self):
        model_mock = mock.Mock()

        ExternalLink().configure_model(model_mock)
        assert model_mock.add_to_class.called is True

    def test_clean(self):
        link_mock = mock.Mock()
        link_mock.external_url = None
        with pytest.raises(ValidationError):
            ExternalLink().clean(link_mock)

        link_mock.external_url = 'mock-test'
        ExternalLink().clean(link_mock)

    def test_get_absolute_url(self):
        link_mock = mock.Mock()
        link_mock.external_url = 'mock-test'

        assert ExternalLink().get_absolute_url(link_mock) == 'mock-test'


class TestModelLink:
    def setup(self):
        self.model_mock = mock.Mock()
        self.model_mock.__name__ = 'MockModel'
        self.model_mock._meta.verbose_name = 'Mock Model'
        self.model_mock.return_value.get_absolute_url = lambda: 'mock-url'

    @mock.patch('anylink.extensions.get_model')
    def test_init_error(self, get_model_mock):
        delattr(self.model_mock, 'get_absolute_url')
        get_model_mock.return_value = self.model_mock

        with pytest.raises(ImproperlyConfigured):
            ModelLink()

        with pytest.raises(ImproperlyConfigured):
            ModelLink(model='mock.Model')

        assert get_model_mock.call_count == 1
        assert get_model_mock.call_args[0] == ('mock', 'Model')

    @mock.patch('anylink.extensions.get_model')
    def test_init_success(self, get_model_mock):
        get_model_mock.return_value = self.model_mock

        link = ModelLink(model='mock.Model')

        assert link.model == self.model_mock

    @mock.patch('anylink.extensions.get_model')
    def test_name(self, get_model_mock):
        get_model_mock.return_value = self.model_mock

        link = ModelLink(model='mock.Model')
        assert link.get_name() == 'mockmodel'

        link.kwargs['name'] = 'asdmodel'
        assert link.get_name() == 'asdmodel'

    @mock.patch('anylink.extensions.get_model')
    def test_verbose_name(self, get_model_mock):
        get_model_mock.return_value = self.model_mock

        link = ModelLink(model='mock.Model')
        assert link.get_verbose_name() == 'Mock Model'

        link.kwargs['verbose_name'] = 'asd Model'
        assert link.get_verbose_name() == 'asd Model'

    @mock.patch('anylink.extensions.get_model')
    @mock.patch('anylink.extensions.models.ForeignKey')
    def test_configure_model(self, foreignkey_mock, get_model_mock):
        get_model_mock.return_value = self.model_mock

        link_mock = mock.Mock()
        ModelLink(model='mock.Model').configure_model(link_mock)

        assert link_mock.add_to_class.call_count == 1

    @mock.patch('anylink.extensions.get_model')
    def test_configure_modeladmin(self, get_model_mock):
        get_model_mock.return_value = self.model_mock

        link_admin_mock = mock.Mock()
        link_admin_mock.raw_id_fields = []

        ModelLink(model='mock.Model').configure_modeladmin(link_admin_mock)
        assert link_admin_mock.raw_id_fields == ['mockmodel']

        link_admin_mock.raw_id_fields = ['field1', 'field2']
        ModelLink(model='mock.Model').configure_modeladmin(link_admin_mock)
        assert link_admin_mock.raw_id_fields == ['field1', 'field2', 'mockmodel']

    @mock.patch('anylink.extensions.get_model')
    def test_get_absolute_url(self, get_model_mock):
        get_model_mock.return_value = self.model_mock

        link_mock = mock.Mock()
        link_mock.mockmodel = self.model_mock()
        url = ModelLink(model='mock.Model').get_absolute_url(link_mock)
        assert url == 'mock-url'
