# This model is for Django 1.7 compatibility. It should not be imported anywhere.
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AnylinkConfig(AppConfig):

    name = 'anylink'
    verbose_name = _("Anylink")

    def ready(self):
        from anylink.models import do_anylink_extension_setup
        from django.apps import apps

        has_admin = apps.is_installed('django.contrib.admin')

        for model in self.get_models():
            do_anylink_extension_setup(model, setup_admin=False)

            if has_admin:
                for extension in list(model.extensions.values()):
                    # TODO: Support non-default admin site configuration.
                    admin = apps.get_app_config('admin').module

                    for model, modeladmin in admin.site._registry.items():
                        extension.configure_modeladmin(modeladmin)
