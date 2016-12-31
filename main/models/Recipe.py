from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from .Category import Category
from .Equipment import Equipment


class Recipe(models.Model):
    # Translators : recipe fields
    title = models.CharField(max_length=255, verbose_name=_("title"))
    description = models.TextField(verbose_name=_("description"))
    tps_prep = models.IntegerField(verbose_name=_("prep time"))  # Preparation time, in seconds
    tps_rep = models.IntegerField(null=True, default=None, verbose_name=_("break time"))  # Break ("repos") time,
    # in seconds
    tps_cuis = models.IntegerField(null=True, default=None, verbose_name=_("cook time"))  # Cooking ("cuisson") time
    picture_file = models.CharField(max_length=255, verbose_name=_("Picture file"))  # Filename of the illustration of
    # the recipe
    nb_people = models.IntegerField(verbose_name=_("number of people"))  # Number of people for indicated quantities
    nb_people_max = models.IntegerField(null=True, default=None, verbose_name=_("max number of people"))  # Max number
    # of people for indicated quantities
    # [if defined, np_people is the min value of the range]
    precision = models.CharField(max_length=150, default=None, null=True, verbose_name=_("precision"))  # Add a
    # precision to nb_people
    pub_date = models.DateTimeField(auto_now=True, verbose_name=_("publication date"))  # Date of recipe publishing
    last_modif = models.DateTimeField(auto_now=True, verbose_name=_("last modification"))
    author = models.ForeignKey(User, verbose_name=_("author"))
    category = models.ManyToManyField(Category, verbose_name=_("category"))  # Recipe
    # category
    equipment = models.ManyToManyField(Equipment, through='EquipmentInRecipe', verbose_name=_("equipment"))
    excerpt = models.TextField(verbose_name=_("excerpt"))
    enable_comments = models.BooleanField(default=True, verbose_name=_("enable comments"))
    published = models.BooleanField(default=True, verbose_name=_("published"))
    slug = models.CharField(max_length=255, verbose_name=_("slug"), unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Recipe")
        verbose_name_plural = _("Recipes")
