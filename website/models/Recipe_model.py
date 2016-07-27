from django.db import models
from .User_model import User
from .Category_model import Category
from .Equipment_model import Equipment


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    tps_prep = models.IntegerField()  # Preparation time, in seconds
    tps_rep = models.IntegerField(null=True, default=None)  # Break ("repos") time, in seconds
    tps_cuis = models.IntegerField(null=True, default=None)  # Cooking ("cuisson") time
    picture_file = models.CharField(max_length=255)  # Filename of the illustration of the recipe
    nb_people = models.IntegerField()  # Number of people for indicated quantities
    pub_date = models.DateTimeField('date published', auto_now=True)  # Date of recipe publishing
    last_modif = models.DateTimeField('lase modification', auto_now=True)
    author = models.ForeignKey(User)
    category = models.ManyToManyField(Category)  # Recipe category
    equipment = models.ManyToManyField(Equipment, through='EquipmentInRecipe')