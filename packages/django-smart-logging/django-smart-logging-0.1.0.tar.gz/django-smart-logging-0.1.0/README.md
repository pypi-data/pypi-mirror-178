django-smart-logging
====================

[![master](https://gitlab.com/os4d/django-logging-dbconfig/badges/master/pipeline.svg)](https://gitlab.com/os4d/django-logging-dbconfig/-/commits/master)
[![develop](https://gitlab.com/os4d/django-logging-dbconfig/badges/master/pipeline.svg)](https://gitlab.com/os4d/django-logging-dbconfig/-/commits/develop)
[![coverage](https://gitlab.com/os4d/django-logging-dbconfig/badges/develop/coverage.svg)](https://gitlab.com/os4d/django-logging-dbconfig/-/graphs/develop/charts)

Plugin for django-smart-admin that allows changing python logging configuration (level/handlers/propagate) without the need to restart the app



Known Limits:
-------------

- double handlers with same configuration are not detected
```
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
        "console2": {"class": "logging.StreamHandler", "formatter": "verbose"},
        "null": {
            "class": "logging.NullHandler",
        },
    }
```
