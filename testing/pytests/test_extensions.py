import mock
import pytest

from django.core.exceptions import ValidationError, ImproperlyConfigured

from anylink.extensions import BaseLink, ExternalLink, ModelLink


class TestBaseLink:
    def test_configure_model(self):
        model_mock = mock.Mock()

        BaseLink().configure_model(model_mock)
        assert len(model_mock.method_calls) == 0

    def test_get_absolute_url(self):
        with pytest.raises(NotImplementedError):
            BaseLink().get_absolute_url(mock.Mock())


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
    @mock.patch('anylink.extensions.models.get_model')
    def test_init(self, get_model_mock):
        model_mock = mock.Mock()
        model_mock.__name__ = 'MockModel'
        delattr(model_mock, 'get_absolute_url')
        get_model_mock.return_value = model_mock

        with pytest.raises(ImproperlyConfigured):
            ModelLink()

        with pytest.raises(ImproperlyConfigured):
            ModelLink(model='mock.Model')

        get_model_mock.assert_called_with('mock', 'Model')

        model_mock.get_absolute_url = lambda s: 'mock-url'
        ModelLink(model='mock.Model')

    @mock.patch('anylink.extensions.models.get_model')
    def test_get_absolute_url(self, get_model_mock):
        model_mock = mock.Mock()
        model_mock.__name__ = 'MockModel'
        model_mock.get_absolute_url = lambda: 'mock-url'
        get_model_mock.return_value = model_mock

        link_mock = mock.Mock()
        link_mock.mockmodel = model_mock
        url = ModelLink(model='mock.Model').get_absolute_url(link_mock)
        assert url == 'mock-url'
