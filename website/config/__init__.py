import re

from pywebcooking import settings

if re.match('^fr-\w+$', settings.LANGUAGE_CODE):
    from .UrlConfig import UrlConfigFr as UrlConfig
else:  # Default is english
    from .UrlConfig import UrlConfigEn as UrlConfig
