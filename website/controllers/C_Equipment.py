from website.models import Equipment, Recipe, EquipmentInRecipe
from website.functions.exceptions import RequiredParameterException


class CEquipment:
    @staticmethod
    def add_new_to_recipe(name: str, quantity: int, nb: int, recipe: Recipe) -> EquipmentInRecipe:
        # Check parameters:
        if name is not None and (not isinstance(name, str)):
            raise TypeError("name must be a string")
        if name is None or len(name) == 0:
            raise RequiredParameterException("name is required and must be not empty")
        if quantity is not None and (not isinstance(quantity, int)):
            raise TypeError("quantity must be an integer")
        if quantity is None or quantity == 0:
            raise RequiredParameterException("quantity is required and must be strictly higher than 0")
        if nb is not None and (not isinstance(nb, int)):
            raise TypeError("nb must be an integer")
        if nb is None:
            raise RequiredParameterException("nb is required")
        if recipe is not None and (not isinstance(recipe, Recipe)):
            raise TypeError("recipe must be an instance of the Recipe class")
        if recipe is None:
            raise RequiredParameterException("recipe is required")

        # Do the add:
        e = Equipment.objects.get_or_create(name=name)[0]
        eir = EquipmentInRecipe(equipment=e, recipe=recipe, nb=nb, quantity=quantity)
        eir.save()

        return eir
