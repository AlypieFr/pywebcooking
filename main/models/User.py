from django.db import models
from .Group import Group


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    date_created = models.DateTimeField('date published', auto_now=True)
    date_last_connection = models.DateTimeField('date published', auto_now=True)
    group = models.ForeignKey(Group, null=True, default=None)

    def __str__(self):
        return self.first_name + " " + self.last_name
