from django.db import models
from .Recipe import Recipe
from .User import User


class Comment(models.Model):
    pseudo = models.CharField(max_length=100, null=True, default=None)
    website = models.CharField(max_length=255, null=True, default=None)
    mail = models.CharField(max_length=255, null=True, default=None)
    author = models.ForeignKey(User, null=True, default=None)
    content = models.TextField()
    recipe = models.ForeignKey(Recipe)
    published = models.BooleanField(default=True)
    pub_date = models.DateTimeField('date published', auto_now=True)
