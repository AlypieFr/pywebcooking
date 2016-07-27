from django.db import models
from .Ingredient import Ingredient
from .Recipe import Recipe


class IngredientGroup(models.Model):
    title = models.CharField(max_length=255, default="")
    nb = models.IntegerField()
    ingredients = models.ManyToManyField(Ingredient, through='IngredientInGroup')
    parent = models.ForeignKey("self", default=None, null=True)
    recipe = models.ForeignKey(Recipe)
