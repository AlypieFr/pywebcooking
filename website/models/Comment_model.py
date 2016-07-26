from django.db import models
from .Recipe_model import Recipe
from .Author_model import Author


class Comment(models.Model):
    pseudo = models.CharField(max_length=100, null=True, default=None)
    website = models.CharField(max_length=255, null=True, default=None)
    mail = models.CharField(max_length=255, null=True, default=None)
    author = models.ForeignKey(Author, null=True, default=None)
    content = models.TextField()
    recipe = models.ForeignKey(Recipe)
