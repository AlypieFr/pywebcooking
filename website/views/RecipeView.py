from .GenericView import GenericView
from django.views.generic import TemplateView
from django.http import Http404

from main.controllers import CRecipe


class RecipeView(TemplateView):
    categories = GenericView.categories()
    config = GenericView.config

    template_name = "website/recipe.html"

    def recipe(self):
        data = {}
        recipe = CRecipe.get_recipe_from_slug(self.kwargs["slug"])
        if recipe is None:
            raise Http404("This recipe does not exists")
        data["html"] = CRecipe.get_recipe_html(recipe)
        data["recipe"] = recipe
        data["date_published"] = recipe.pub_date.date()
        data["categories"] = []
        for cat in recipe.category.all():
            data["categories"].append("<a href='/category/" + cat.url + "'>" + cat.name + "</a>")
        data["categories"] = " - ".join(data["categories"])
        return data
