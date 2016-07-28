from website.models import IngredientGroup, IngredientInGroup, Ingredient, Recipe

from website.functions.exceptions import RequiredParameterException, MissingKeyException


class CIngredientGroup:
    @staticmethod
    def add_new(title: str, nb: int, recipe: Recipe, level: int = 0, ingredients: list = None) \
            -> IngredientGroup:
        """
        Add new ingredient group
        :param title:
        :param nb:
        :param level:
        :param ingredients:
        :param recipe:
        :return:
        """
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
        if recipe is None:
            raise RequiredParameterException("recipe is required")
        if not isinstance(level, int):
            raise TypeError("level must be an integer")
        if ingredients is not None:
            if not isinstance(ingredients, list):
                raise TypeError("ingredients must be a dict")
            required_keys = ["name", "quantity", "unit", "nb"]
            for ingr in ingredients:
                for req in required_keys:
                    if req not in ingr:
                        raise MissingKeyException("missing key for ingredient: " + req)

        # Add new IngredientGroup:
        ig = IngredientGroup(title=title, nb=nb, recipe=recipe, level=level)

        ig.save()

        # Add ingredients:
        if ingredients is not None:
            for ingr in ingredients:
                ingredient = Ingredient.objects.get_or_create(name=ingr["name"])[0]
                iig = IngredientInGroup(quantity=ingr["quantity"], unit=ingr["unit"], nb=ingr["nb"],
                                        ingredient=ingredient, ingredientGroup=ig)
                iig.save()

        return ig
