from django.views.generic import TemplateView
from django.http import Http404

from main.controllers import CRecipe


class RecipeView(TemplateView):
    template_name = "website/recipe.html"

    website_name = "PyWebCooking"

    def recipe(self):
        data = {}
        recipe = CRecipe.get_recipe_from_slug(self.kwargs["slug"])
        if recipe is None:
            raise Http404("This recipe does not exists")
        data["html"] = CRecipe.get_recipe_html(recipe)
        data["recipe"] = recipe
        return data
