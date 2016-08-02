from django.db import models
from .Ingredient import Ingredient
from .IngredientGroup import IngredientGroup


class IngredientInGroup(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    ingredientGroup = models.ForeignKey(IngredientGroup, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=100)
    nb = models.IntegerField()

    class Meta:
        unique_together = ('ingredientGroup', 'nb')
