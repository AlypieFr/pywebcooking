from django.db import models
from .Recipe import Recipe


class Instruction(models.Model):
    nb = models.IntegerField()
    level = models.IntegerField(default=0)
    text_inst = models.TextField()
    recipe = models.ForeignKey(Recipe)
