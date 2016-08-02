from django.db import models
from .Ingredient import Ingredient
from .Recipe import Recipe


class IngredientGroup(models.Model):
    title = models.CharField(max_length=255, default="")
    nb = models.IntegerField()
    level = models.IntegerField(default=0)
    ingredients = models.ManyToManyField(Ingredient, through='IngredientInGroup')
    recipe = models.ForeignKey(Recipe)

    class Meta:
        unique_together = ('nb', 'recipe')
