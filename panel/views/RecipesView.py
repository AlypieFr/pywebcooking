import os
from django.views.generic import View
from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from pywebcooking import settings
from django.utils.translation import ugettext as _
from pywebcooking.settings import MEDIA_ROOT, LOCALE
from main.models import Recipe, UserProfile
from main.config import RecipeConfig
from django_gravatar.helpers import get_gravatar_url
from .GenericView import GenericView
import locale
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import urllib.parse


class RecipesView(View):

    @staticmethod
    def __sort_dates(a):
        return a[0] + a[2]

    def get(self, request, page=1, mine=False, published=False, trash=False):
        """
        Rendre list of recipes
        :param request: request object
        :param page: page to show
        :param mines: if True, show only my recipes
        :param published: if True, show only published recipes
        :param trash: if True, show trash
        :return:
        """
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        recipes = Recipe.objects.all().order_by("pub_date").reverse()
        select = "all"
        nb_recipes = recipes.filter(trash=False).count()
        nb_my_recipes = recipes.filter(author__user=self.request.user, trash=False).count()
        nb_recipes_published = recipes.filter(published=True, trash=False).count()
        if not request.user.is_staff:
            nb_trash = recipes.filter(trash=True, author__user=request.user).count()
        else:
            nb_trash = recipes.filter(trash=True).count()
        if not trash:
            recipes = recipes.filter(trash=False)
        else:
            select = "trash"
            recipes = recipes.filter(trash=True)
            if not request.user.is_staff:
                recipes = recipes.filter(author__user=request.user)
            if len(recipes) == 0:
                return HttpResponseRedirect(reverse("recipes"))
        if not trash:  # Must be done here to not affect previous counts
            if mine:
                recipes = recipes.filter(author__user=request.user)
                select = "mine"
            elif published:
                recipes = recipes.filter(published=True)
                select = "published"
        locale.setlocale(locale.LC_TIME, LOCALE)
        user_slug = UserProfile.objects.get(user=request.user).url
        kwargs = {}
        all_dates = set()
        for recipe in recipes:
            month_int = recipe.pub_date.month
            month = recipe.pub_date.strftime("%B")
            year = recipe.pub_date.year
            all_dates.add((month_int, month, year))
        filter_date = ["all", "all"]
        filter_cat = "all"
        if "filter-month" in request.GET and request.GET["filter-month"] != "0":
            filter_date = request.GET["filter-month"]
            filter_date = list(map(int, filter_date.split("-")))
            recipes = recipes.filter(pub_date__month=filter_date[0], pub_date__year=filter_date[1])
        if "filter-cat" in request.GET and request.GET["filter-cat"] != "0":
            filter_cat = request.GET["filter-cat"]
            recipes = recipes.filter(category__name=filter_cat)

        show_recipes = []
        paginator = Paginator(recipes, 25)
        try:
            page_recipe = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            page_recipe = paginator.page(1)
        for recipe in page_recipe:
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
                "id": recipe.id
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
            "user_slug": user_slug,
            "avatar": get_gravatar_url(request.user.email, size=160),
            "page": "recipes",
            "nb_recipes": nb_recipes,
            "nb_my_recipes": nb_my_recipes,
            "nb_recipes_published": nb_recipes_published,
            "nb_trash": nb_trash,
            "all_dates": all_dates,
            "categories": GenericView.categories(),
            "recipes": show_recipes,
            "page_recipe": page_recipe,
            "additionnal_kwargs": kwargs,
            "select": select,
            "filter_date": filter_date,
            "filter_cat": filter_cat,
        }
        return render(request, 'panel/recipes.html', context)
