from django.db import models
from .Equipment import Equipment
from .Recipe import Recipe


class EquipmentInRecipe(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    isComment = models.BooleanField(default=False)
    nb = models.IntegerField()

    class Meta:
        unique_together = ('nb', 'recipe')