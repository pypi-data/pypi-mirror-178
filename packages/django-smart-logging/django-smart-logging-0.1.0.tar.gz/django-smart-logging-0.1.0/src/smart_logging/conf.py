from django.conf import settings
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.utils.functional import lazy

SMART_LOG_ONLINE = getattr(settings, "SMART_LOG_ONLINE", False)
SMART_LOG_MAXSIZE = getattr(settings, "SMART_LOG_MAXSIZE", 100)
SMART_LOG_FORMAT = "%(levelname)s %(asctime)s %(module)s: %(message)s"
SMART_LOG_PREFIX = getattr(settings, "SMART_LOG_PREFIX", "smart-log") or "smart-log"
SMART_LOG_REDIS = getattr(settings, "SMART_LOG_REDIS", "redis://localhost/9")
SMART_LOG_DEBUG = getattr(settings, "SMART_LOG_DEBUG", False)

EVENTS = "%s:%s" % (SMART_LOG_PREFIX, "events")
REGISTRY = "%s:%s" % (SMART_LOG_PREFIX, "registry")
LOGGER = "%s:%s" % (SMART_LOG_PREFIX, "logs")
ONLINE_LOGGER_NAME = "__online__"


@receiver(setting_changed)
def update_settings(setting, value, **kwargs):
    if setting.startswith("SMART_LOG"):
        globals()[setting] = value


# def get_setting(entry):
#     return globals()[entry]
#
#
# def get_setting_lazy(entry):
#     return lazy(str, str)(get_setting(entry))
