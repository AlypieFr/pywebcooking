from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from pywebcooking import settings

from main.models.Recipe import Recipe
from main.models.Category import Category

from panel.forms import RecipeForm

from django_gravatar.helpers import get_gravatar_url
from django.utils.translation import ugettext as _


class RecipeView(View):
    @staticmethod
    def categories():
        cats = []
        cats_get = Category.objects.order_by('order')
        for cat in cats_get:
            cats.append({"name": cat.name, "url": cat.url})
        return cats

    def get(self, request, slug):
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        recipe = Recipe.objects.get(slug=slug)
        r_cats = []
        for cat in recipe.category.all():
            r_cats.append(cat.url)

        form = RecipeForm({"title": recipe,
                           "slug": recipe.slug,
                           "categories": [cat.id for cat in recipe.category.all()],
                           "tps_prep_hr": int(recipe.tps_prep / 60),
                           "tps_prep_min": recipe.tps_prep % 60,
                           "tps_break_j": int(recipe.tps_rep / 1440),
                           "tps_break_hr": int((recipe.tps_rep % 1440) / 60),
                           "tps_break_min": recipe.tps_rep % 60,
                           "tps_cook_hr": int(recipe.tps_cuis / 60),
                           "tps_cook_min": recipe.tps_cuis % 60,
                           "description": recipe.description,
                           "pub_date": recipe.pub_date.strftime("%d/%m/%y %H:%M"),
                           "status": int(recipe.published)})

        context = {
            "recipe": recipe,
            "categories": self.categories(),
            "staff": request.user.is_staff,
            "user_name": request.user.first_name + " " + request.user.last_name,
            "avatar": get_gravatar_url(request.user.email, size=160),
            "page": "recipe",
            "lang": settings.LANGUAGE_CODE,
            "title": _("Edit") + " \"" + recipe.title + "\" | " + settings.SITE_NAME,
            "form": form
        }
        return render(request, 'panel/recipe.html', context)

    def post(self, request, slug):
        print(request, slug)
        return JsonResponse({
            "success": True
        })
