from django.db import models
from .Recipe import Recipe


class MediaInRecipe(models.Model):
    media = models.CharField(unique=True, max_length=255)
    recipe = models.ForeignKey(Recipe)
    type = models.CharField(choices=[("main", "main_picture"), ("other", "other_picutre")], max_length=5)

    class Meta:
        unique_together = ('media', 'recipe')
