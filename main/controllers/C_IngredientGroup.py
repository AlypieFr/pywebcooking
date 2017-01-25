import django
from main.models import IngredientGroup, IngredientInGroup, Ingredient, Recipe

from main.functions import Functions
from main.functions.exceptions import RequiredParameterException, MissingKeyException


class CIngredientGroup:
    @staticmethod
    def add_new(title: str, nb: int, recipe: Recipe, level: int = 0, ingredients: "list of dict" = None) \
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
        if title is None:
            raise RequiredParameterException("title is required (can be empty)")
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
                iig = IngredientInGroup(quantity=ingr["quantity"] if ingr["quantity"] > 0 else None, unit=ingr["unit"], nb=ingr["nb"],
                                        ingredient=ingredient, ingredientGroup=ig)
                iig.save()

        return ig

    @staticmethod
    def build_html_for_ig(ingredient_group: IngredientGroup) -> "str, bool":
        """
        Build html for an ingredient group
        :param ingredient_group: the ingredient group
        :return: the html, has ingredients
        """
        # Check parameters:
        if ingredient_group is not None and (not isinstance(ingredient_group, IngredientGroup)):
            raise TypeError("ingredient_group must be an instance of the IngredientGroup class")
        if ingredient_group is None:
            raise RequiredParameterException("ingredient_group is required")

        # Do the staff:
        html = ""
        has_title = ingredient_group.title is not None and len(ingredient_group.title) > 0
        level = ingredient_group.level

        if has_title and level > 0:
            html += "<li>" + ingredient_group.title + "</li>"
        elif has_title:
            html += "<p>" + ingredient_group.title + "</p>"

        ingredients_query = IngredientInGroup.objects.filter(ingredientGroup=ingredient_group)
        ingredients = []
        for ingr in ingredients_query:
            ingredients.append(ingr)
        ingredients.sort(key=lambda i: i.nb)

        quantity_transform = {
            0.2: "1/5",
            0.25: "1/4",
            0.33: "1/3",
            0.4: "2/5",
            0.5: "1/2",
            0.6: "3/5",
            0.67: "2/3",
            0.75: "3/4",
            0.8: "4/5"
        }

        has_ingr = False

        if len(ingredients) > 0:
            has_ingr = True
            if has_title:
                html += "<ul>"
            for ingr in ingredients:
                if ingr.quantity is not None:
                    qte = round(ingr.quantity, 2)
                    quantity = str(ingr.quantity)
                    if qte in quantity_transform:
                        quantity = quantity_transform[qte]
                    elif quantity[-2:] == ".0":  # Remove .0 if any
                        quantity = quantity[:-2]
                else:
                    quantity = ""
                unit = ""
                if len(ingr.unit) > 0:
                    unit = ingr.unit
                    if django.utils.translation.get_language().lower().startswith("fr"):
                        vowels = ["a", "e", "i", "o", "u", "y"]
                        if Functions.remove_accents(ingr.ingredient.name[0].lower()) in vowels:
                            unit += " d'"
                        else:
                            unit += " de "

                html += "<li>" + quantity + " " + unit + ingr.ingredient.name + "</li>"

        return html, has_ingr

    @staticmethod
    def build_html_for_ingredients(recipe: Recipe) -> str:
        """
        Build html of ingredients of a given recipe
        :param recipe: the recipe to build the html of ingredients
        :return: the html
        """
        # Check parameters:
        if recipe is not None and (not isinstance(recipe, Recipe)):
            raise TypeError("recipe must be an instance of the Recipe class")
        if recipe is None:
            raise RequiredParameterException("recipe is required")

        # Do the staff:
        ingredient_groups_query = IngredientGroup.objects.filter(recipe=recipe)
        ingredient_groups = []
        for ig in ingredient_groups_query:
            ingredient_groups.append(ig)
        ingredient_groups.sort(key=lambda k: k.nb)

        html = ""

        last_level = 0
        for ig in ingredient_groups:
            level = ig.level
            if level > last_level:
                for i in range(last_level, level):
                    html += "<ul>"
            elif level < last_level:
                for i in range(level, last_level):
                    html += "</ul>"

            html_ig, has_ingr = CIngredientGroup.build_html_for_ig(ig)
            html += html_ig

            # Update last_level:
            if ig.title is not None and len(ig.title) > 0 and has_ingr:  # If ingredient group has title and has
                # ingredients (so contains a <ul> but not a </ul>
                level += 1
            last_level = level

        if last_level > 0:
            for i in range(0, last_level):
                html += "</ul>"

        return html
