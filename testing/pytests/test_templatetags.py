from __future__ import unicode_literals
import pytest

from anylink.models import AnyLink
from anylink.templatetags.anylink_tags import insert_anylinks


@pytest.mark.django_db
class TestInsertAnyLinks:

    def setup(self):
        self.link1 = AnyLink.objects.create(
            pk=1, link_type='external_url', external_url='/link1/',
            css_class='test')
        self.link2 = AnyLink.objects.create(
            pk=2, link_type='external_url', external_url='/link2/')
        self.link3 = AnyLink.objects.create(
            pk=3, link_type='external_url', external_url='/link3/',
            target='_blank')

    def test_replace(self):
        assert insert_anylinks(
            'Test <a href="#AL1"> Another blaa <strong>'
            '<a href="http://test/">'
        ) == (
            'Test <a href="/link1/" target="_self" class="test"> Another blaa '
            '<strong><a href="http://test/">'
        )

    def test_replace_multiple_reuse(self):
        out = insert_anylinks(
            'Test <a href="#AL1"> Another blaa <strong>'
            'foo <a href="#AL999"> Another blaa'
            'bar <a href="#AL2"> Another blaa <strong>'
            'bar <a href="#AL3"> Another blaa <strong>'
            'Test <a href="#AL2"> Another blaa <strong>'
            '<a href="http://test/">'
        )
        expected = (
            'Test <a href="/link1/" target="_self" class="test"> Another blaa '
            '<strong>foo <a href="#AL999"> Another blaa'
            'bar <a href="/link2/" target="_self"> Another blaa <strong>'
            'bar <a href="/link3/" target="_blank"> Another blaa <strong>'
            'Test <a href="/link2/" target="_self"> Another blaa <strong>'
            '<a href="http://test/">'

        )

        assert out == expected
