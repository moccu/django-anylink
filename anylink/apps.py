# This model is for Django 1.7 compatibility. It should not be imported anywhere.
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AnyLinkConfig(AppConfig):

    name = 'anylink'
    verbose_name = _("AnyLink")

    def ready(self):
        from anylink.models import do_anylink_extension_setup

        for model in self.get_models():
            do_anylink_extension_setup(model)
