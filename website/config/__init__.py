import re
from pywebcooking import settings

if re.match('^fr-\w+$', settings.LANGUAGE_CODE):
    from .RecipeConfig import RecipeConfigFr as RecipeConfig
else:  # Default is english
    from .RecipeConfig import RecipeConfigEn as RecipeConfig
