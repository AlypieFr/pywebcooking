from django.db import models
from .Recipe import Recipe


class Instruction(models.Model):
    nb = models.IntegerField()
    level = models.IntegerField()
    text_inst = models.TextField()
    parent = models.ForeignKey("self", default=None, null=True)
    recipe = models.ForeignKey(Recipe)
