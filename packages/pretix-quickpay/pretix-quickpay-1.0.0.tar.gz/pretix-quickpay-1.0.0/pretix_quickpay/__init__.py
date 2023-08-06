from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")

__version__ = "1.0.0"


class PluginApp(PluginConfig):
    name = "pretix_quickpay"
    verbose_name = "Quickpay payments for pretix"

    class PretixPluginMeta:
        name = gettext_lazy("Quickpay")
        author = gettext_lazy("the pretix team")
        description = gettext_lazy(
            "Use Quickpay as a payment provider, where you can activate various payment methods for your customers."
        )
        visible = True
        version = __version__
        category = "PAYMENT"
        picture = "pretix_quickpay/logo.svg"
        compatibility = "pretix>=2.7.0"

    def ready(self):
        from . import signals  # NOQA


default_app_config = "pretix_quickpay.PluginApp"
