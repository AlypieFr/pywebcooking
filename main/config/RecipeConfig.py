from django.utils.translation import ugettext as _


class RecipeConfig:
    photo_in_recipe_width = "254"
    photo_in_index_width = "350"
    # Translators: terms used in a recipe
    ingredients_short = _("Ingredients (for %d people):")
    ingredients_short_1p = _("Ingredients (for %d person):")
    ingredients_long = _("Ingredients (for %d people (%s)):")
    ingredients_long_1p = _("Ingredients (for %d person (%s)):")
    ingredients_range_short = _("Ingredients (from %d to %d people):")
    ingredients_range_long = _("Ingredients (from %d to %d people (%s)):")
    equipment = _("Required equipment:")
    instructions = _("Instructions:")
    proposals = _("Proposals:")
    timePreparation = _("Prep:")
    timeCuis = _("Cook:")
    timeRep = _("Break:")
