from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    date_created = models.DateTimeField('date published', auto_now=True)
    date_last_connection = models.DateTimeField('date published', auto_now=True)
