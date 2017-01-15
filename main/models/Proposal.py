from django.db import models
from .Recipe import Recipe


class Proposal(models.Model):
    nb = models.IntegerField()
    text_prop = models.TextField()
    recipe = models.ForeignKey(Recipe)

    class Meta:
        unique_together = ('nb', 'recipe')