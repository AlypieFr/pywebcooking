from django.db import models
from .Equipment_model import Equipment
from .Recipe_model import Recipe


class EquipmentInRecipe(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.FloatField()
    nb = models.IntegerField()
