from django.db import models
from .User_model import User
from .Category_model import Category
from .Equipment_model import Equipment
from website.functions.exceptions import RequiredParameterException, BadParameterException
import datetime


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

    @staticmethod
    def add_new(title: str, description: str, tps_prep: int, picture_file: str, nb_people: int, author: User,
                categories: "list of Category", pub_date: datetime, tps_rep: int, tps_cuis: int) -> "Recipe":
        """
        Add new recipe
        :param title: title of the recipe {string} [REQ]
        :param description: description of the recipe {string} [REQ]
        :param tps_prep: time needed to prepare the recipe, without "cuisson" time - in minutes {int} [REQ]
        :param picture_file: the illustration filename of the recipe {string} [REQ]
        :param nb_people: the number of people for this recipe {int} [REQ]
        :param author: the author of this recipe {User} [REQ]
        :param categories: the list of categories for this recipe {list<Category>} [REQ]
        :param pub_date: the publication date - if not sent, use current date {datetime} [OPT]
        :param tps_rep: the break ("repos") time {int} [OPT]
        :param tps_cuis: the cooking ("cuisson") time {int} [OPT]
        :return: the recipe created {Recipe}
        """

        # Check parameters:
        if title is not None and (not isinstance(title, str)):
            raise TypeError("title must be a string")
        if title is None or len(title) == 0:
            raise RequiredParameterException("title is required and must be not empty")
        if description is not None and (not isinstance(description, str)):
            raise TypeError("description must be a string")
        if description is None or len(description) == 0:
            raise RequiredParameterException("description is required and must be not empty")
        if tps_prep is not None and (not isinstance(tps_prep, int)):
            raise TypeError("tps_prep must be an integer")
        if tps_prep is None or tps_prep == 0:
            raise RequiredParameterException("tps_prep is required and must be greater than 0")
        if tps_rep is not None and (not isinstance(tps_rep, int)):
            raise TypeError("tps_rep must be an integer")
        if tps_rep is not None and tps_rep == 0:
            raise BadParameterException("tps_rep is given but is equal to 0")
        if tps_cuis is not None and (not isinstance(tps_cuis, int)):
            raise TypeError("tps_cuis must be an integer")
        if tps_cuis is not None and tps_cuis == 0:
            raise BadParameterException("tps_cuis is given but is equal to 0")
        if picture_file is not None and (not isinstance(picture_file, str)):
            raise TypeError("picture_file must be a string")
        if picture_file is None or len(picture_file) == 0:
            raise RequiredParameterException("picture_file is required and must be not empty")
        if nb_people is not None and (not isinstance(nb_people, int)):
            raise TypeError("nb_people must be an integer")
        if nb_people is None or nb_people == 0:
            raise RequiredParameterException("nb_people is required and must be greater than 0")
        if author is not None and (not isinstance(author, User)):
            raise TypeError("author must be an instance of User object")
        if author is None:
            raise RequiredParameterException("author is required")
        if categories is None:
            raise RequiredParameterException("categories is required")
        else:
            if not isinstance(categories, list):
                raise TypeError("categories must be a list")
            for cat in categories:
                if not isinstance(cat, Category):
                    raise TypeError("categories must be a list of Category object")

        # Assign missing values (that are not required):
        if pub_date is None:
            pub_date = datetime.datetime.now()

        # Create recipe:
        r = Recipe(title=title, description=description, tps_prep=tps_prep, tps_rep=tps_rep, tps_cuis=tps_cuis,
                   picture_file=picture_file, nb_people=nb_people, author=author, pub_date=pub_date)
        r.save()

        # Add categories:
        r.add_categories(categories)

    def add_categories(self, categories: "list of Categories"):
        # Check parameters:
        if not isinstance(categories, list):
            raise TypeError("categories must be a list")
        for cat in categories:
            if not isinstance(cat, Category):
                raise TypeError("categories must be a list of Category object")

        # Do the staff:
        for cat in categories:
            self.category.add(cat)