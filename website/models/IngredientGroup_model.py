from django.db import models
from .Ingredient_model import Ingredient
from .IngredientInGroup_model import IngredientInGroup
from .Recipe_model import Recipe
from website.functions.exceptions import RequiredParameterException, MissingKeyException


class IngredientGroup(models.Model):
    title = models.CharField(max_length=255, default="")
    nb = models.IntegerField()
    ingredients = models.ManyToManyField(Ingredient, through='IngredientInGroup')
    parent = models.ForeignKey("self", default=None, null=True)
    recipe = models.ForeignKey(Recipe)

    @staticmethod
    def add_new(title: str, nb: int, ingredients: list, parent: "IngredientGroup", recipe: Recipe):
        # Check parameters:
        if title is not None and (not isinstance(title, str)):
            raise TypeError("title must be a string")
        if title is None or len(title) == 0:
            raise RequiredParameterException("title is required and must be not empty")
        if nb is not None and (not isinstance(nb, int)):
            raise TypeError("nb must be an integer")
        if nb is None:
            raise RequiredParameterException("nb is required")
        if recipe is not None and (not isinstance(recipe, Recipe)):
            raise TypeError("recipe must be a Recipe")
        if ingredients is not None:
            if not isinstance(ingredients, list):
                raise TypeError("ingredients must be a dict")
            required_keys = ["name", "quantity", "unit", "nb"]
            for ingr in ingredients:
                for req in required_keys:
                    if req not in ingr:
                        raise MissingKeyException("missing key for ingredient: " + req)
        if parent is not None and (not isinstance(parent, IngredientGroup)):
            raise TypeError("parent must be an IngredientGroup or None")

        # Add new IngredientGroup:
        ig = IngredientGroup(title=title, nb=nb, recipe=recipe)
        if parent is not None:
            ig.parent = parent

        ig.save()

        # Add ingredients:
        if ingredients is not None:
            for ingr in ingredients:
                ingredient = Ingredient(name=ingr["name"])
                ingredient.save()
                iig = IngredientInGroup(quantity=ingr["quantity"], unit=ingr["unit"], nb=ingr["nb"],
                                        ingredient=ingredient, ingredientGroup=ig)
                iig.save()
