import os
from django.views.generic import View
from django.shortcuts import render, redirect
from pywebcooking import settings
from django.utils.translation import ugettext as _
from pywebcooking.settings import MEDIA_ROOT, LOCALE
from main.models import Recipe, Comment
from main.config import RecipeConfig
from django.contrib.auth.models import User
from django_gravatar.helpers import get_gravatar_url
from .GenericView import GenericView
import locale


class RecipesView(View):

    @staticmethod
    def __sort_dates(a):
        return a[0] + a[2]

    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        recipes = Recipe.objects.all().order_by("pub_date").reverse()
        nb_recipes = recipes.count()
        recipes_user = Recipe.objects.filter(author__user=self.request.user)
        nb_my_recipes = recipes_user.count()
        nb_recipes_published = recipes.filter(published=True).count()
        locale.setlocale(locale.LC_TIME, LOCALE)
        all_dates = set()
        show_recipes = []
        for recipe in recipes:
            month_int = recipe.pub_date.month
            month = recipe.pub_date.strftime("%B")
            year = recipe.pub_date.year
            all_dates.add((month_int, month, year))

            categories = []
            for category in recipe.category.all():
                categories.append(category.name)

            pict_file = MEDIA_ROOT + recipe.author.user.username + "/" + recipe.picture_file
            parts = os.path.splitext(pict_file)
            thumb_file = parts[0] + "_thumb_" + RecipeConfig.photo_in_recipe_width + parts[1]

            show_recipe = {
                "title": recipe.title,
                "author": recipe.author.user.first_name,
                "author_id": recipe.author.user.id,
                "categories": ", ".join(categories),
                "published": recipe.published,
                "pub_date": recipe.pub_date,
                "nb_comments": recipe.comment_set.count(),
                "thumb": thumb_file,
            }
            show_recipes.append(show_recipe)
        all_dates = list(all_dates)
        all_dates.sort(key=lambda x: self.__sort_dates(x))
        all_dates.reverse()
        context = {
            "title": _("User panel") + " - " + settings.SITE_NAME,
            "staff": request.user.is_staff,
            "user_name": request.user.first_name + " " + request.user.last_name,
            "user": request.user,
            "avatar": get_gravatar_url(request.user.email, size=160),
            "page": "recipes",
            "nb_recipes": nb_recipes,
            "nb_my_recipes": nb_my_recipes,
            "nb_recipes_published": nb_recipes_published,
            "all_dates": all_dates,
            "categories": GenericView.categories(),
            "recipes": show_recipes,
        }
        return render(request, 'panel/recipes.html', context)
