from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import Http404

from main.controllers import CRecipe

# Create your views here.


class IndexView(TemplateView):
    template_name = "website/index.html"


class RecipeView(TemplateView):
    template_name = "website/recipe.html"

    def recipe(self):
        data = {}
        recipe = CRecipe.get_recipe_from_slug(self.kwargs["slug"])
        if recipe is None:
            raise Http404("This recipe does not exists")
        data["html"] = CRecipe.get_recipe_html(recipe)
        data["recipe"] = recipe
        return data


#def index(request):
#    return HttpResponse("Hello, world. You're at the main index.")


#def recipe(request):
#    return HttpResponse("Hello, world. You're at a recipe.")