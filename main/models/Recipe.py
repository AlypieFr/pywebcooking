from django.db import models
from .User import User
from .Category import Category
from .Equipment import Equipment


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    tps_prep = models.IntegerField()  # Preparation time, in seconds
    tps_rep = models.IntegerField(null=True, default=None)  # Break ("repos") time, in seconds
    tps_cuis = models.IntegerField(null=True, default=None)  # Cooking ("cuisson") time
    picture_file = models.CharField(max_length=255)  # Filename of the illustration of the recipe
    nb_people = models.IntegerField()  # Number of people for indicated quantities
    nb_people_max = models.IntegerField(null=True, default=None)  # Max number of people for indicated quantities
    # [if defined, np_people is the min value of the range]
    precision = models.CharField(max_length=150, default=None, null=True)  # Add a precision to nb_people
    pub_date = models.DateTimeField('date published', auto_now=True)  # Date of recipe publishing
    last_modif = models.DateTimeField('lase modification', auto_now=True)
    author = models.ForeignKey(User)
    category = models.ManyToManyField(Category)  # Recipe category
    equipment = models.ManyToManyField(Equipment, through='EquipmentInRecipe')
    excerpt = models.TextField()
    enable_comments = models.BooleanField(default=True)
    published = models.BooleanField(default=True)
    slug = models.CharField(max_length=255)
