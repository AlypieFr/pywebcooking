from website.models import IngredientGroup, IngredientInGroup, Ingredient, Recipe

from website.functions.exceptions import RequiredParameterException, MissingKeyException


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

    @staticmethod
    def __sort_by_nb__(a):
        return a.nb

    @staticmethod
    def build_html_for_ig(ingredient_group: IngredientGroup) -> str:
        html = ""
        has_title = ingredient_group.title is not None and len(ingredient_group.title) > 0
        level = ingredient_group.level

        if has_title and level > 0:
            html += "<li>" + ingredient_group.title + "</li>"
        elif has_title:
            html += ingredient_group.title

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

        if len(ingredients) > 0:
            html += "<ul>"
            for ingr in ingredients:
                qte = round(ingr.quantity, 2)
                quantity = str(ingr.quantity)
                if qte in quantity_transform:
                    quantity = quantity_transform[qte]
                elif quantity[-2:] == ".0":  # Remove .0 if any
                    quantity = quantity[:-2]
                unit = ""
                if len(ingr.unit) > 0:
                    unit = ingr.unit + " "
                html += "<li>" + quantity + " " + unit + ingr.ingredient.name + "</li>"
            html += "</ul>"

        return html
