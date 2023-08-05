# -*- coding: UTF-8 -*-
from django.conf import settings


USER_SETTINGS = getattr(settings, 'DJANGO_DATAWATCH', {})


DEFAULT_SETTINGS = dict(
    QUEUE_NAME='django_datawatch'
)

ddw_settings = DEFAULT_SETTINGS.copy()
ddw_settings.update(USER_SETTINGS)
ddw_settings = type('settings', (object, ), ddw_settings)
