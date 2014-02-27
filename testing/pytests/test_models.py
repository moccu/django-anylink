import mock
import pytest

from django.core.exceptions import ImproperlyConfigured

from anylink.models import AnyLink


class TestAnyLinkMetaclass:
    def test_extension_registration(self, settings):
        settings.ANYLINK_EXTENSIONS = (
            'anylink.extensions.ExternalLink',
        )

        class AnyLinkTest(AnyLink):
            pass

        assert len(AnyLinkTest.extensions) == 1
        assert hasattr(AnyLinkTest, 'get_link_type_display')

    def test_extension_registration_twice(self, settings):
        settings.ANYLINK_EXTENSIONS = (
            'anylink.extensions.ExternalLink',
            'anylink.extensions.ExternalLink',
        )

        with pytest.raises(ImproperlyConfigured):
            class AnyLinkTest(AnyLink):
                pass

    def test_extension_registration_with_options(self, settings):
        settings.ANYLINK_EXTENSIONS = (
            ('anylink.extensions.ExternalLink', {'test': 'foo'}),
        )

        class AnyLinkTest(AnyLink):
            pass

        assert len(AnyLinkTest.extensions) == 1
        assert AnyLinkTest.extensions['external_url'].kwargs == {'test': 'foo'}
        assert hasattr(AnyLinkTest, 'get_link_type_display')


class TestAnyLink:
    def test_clean_no_type_selected(self):
        link = AnyLink(link_type='')
        # Nothing happens, no extension has to clean the value.
        link.clean()

    @mock.patch('anylink.extensions.ExternalLink.clean')
    def test_clean_type_selected(self, clean_mock):
        link = AnyLink(link_type='external_url')

        link.clean()
        clean_mock.assert_called_with(link)

    @mock.patch('anylink.extensions.ExternalLink.get_absolute_url')
    def test_unicode_repr(self, get_absolute_url_mock):
        get_absolute_url_mock.return_value = 'fakeurl'

        link = AnyLink(link_type='external_url')
        assert unicode(link) == get_absolute_url_mock.return_value

    @mock.patch('anylink.extensions.ExternalLink.get_absolute_url')
    def test_get_absolute_url(self, get_absolute_url_mock):
        link = AnyLink(link_type='external_url')

        assert link.get_absolute_url() == get_absolute_url_mock.return_value
        get_absolute_url_mock.assert_called_with(link)

    def test_get_rtelink_id(self):
        link = AnyLink(link_type='external_url', pk=23)
        assert link.get_rtelink_id() == '#AL23'
