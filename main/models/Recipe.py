from django.utils import timezone

from django.db import models
from django.utils.translation import ugettext as _, pgettext as __
from .Category import Category
from .Equipment import Equipment
from .UserProfile import UserProfile
from django.conf import settings

from django.db.models.signals import post_delete


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
    pub_date = models.DateTimeField(verbose_name=_("publication date"))  # Date of recipe publishing
    last_modif = models.DateTimeField(verbose_name=_("last modification"))
    author = models.ForeignKey(UserProfile, verbose_name=_("author"))
    category = models.ManyToManyField(Category, verbose_name=_("category"))  # Recipe
    # category
    equipment = models.ManyToManyField(Equipment, through='EquipmentInRecipe', verbose_name=_("equipment"))
    excerpt = models.TextField(verbose_name=_("excerpt"))
    enable_comments = models.BooleanField(default=True, verbose_name=_("enable comments"))
    published = models.BooleanField(default=True, verbose_name=_("published"))
    slug = models.CharField(max_length=255, verbose_name=_("slug"), unique=True)
    html = models.TextField(null=True, default=None)
    coup_de_coeur = models.IntegerField(choices=((0, __("coup_de_coeur", "Not favorite")),
                                                 (1, __("coup_de_coeur", "Good")),
                                                 (2, __("coup_de_coeur", "Very good")),
                                                 (3, __("coup_de_coeur", "Best of"))), default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.pub_date = timezone.now()
        self.last_modif = timezone.now()
        return super(Recipe, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Recipe")
        verbose_name_plural = _("Recipes")
