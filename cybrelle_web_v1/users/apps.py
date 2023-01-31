from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "cybrelle_web_v1.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import cybrelle_web_v1.users.signals  # noqa F401
        except ImportError:
            pass
