from django.db import models
from .Recipe_model import Recipe


class Instruction(models.Model):
    nb = models.IntegerField()
    level = models.IntegerField()
    text_inst = models.TextField()
    parent = models.ForeignKey("self", default=None, null=True)
    recipe = models.ForeignKey(Recipe)
