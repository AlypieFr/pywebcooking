from django.db import models
from .Recipe_model import Recipe


class Proposal(models.Model):
    nb = models.IntegerField()
    text_cons = models.TextField()
    recipe = models.ForeignKey(Recipe)