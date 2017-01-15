from main.models import Equipment, Recipe, EquipmentInRecipe
from main.functions.exceptions import RequiredParameterException, MissingKeyException, UnknownKeyException


class CEquipment:
    @staticmethod
    def add_new_to_recipe(name: str, quantity: int, nb: int, is_comment: bool, recipe: Recipe) -> EquipmentInRecipe:
        # Check parameters:
        if name is not None and (not isinstance(name, str)):
            raise TypeError("name must be a string")
        if name is None or len(name) == 0:
            raise RequiredParameterException("name is required and must be not empty")
        if quantity is not None and (not isinstance(quantity, int)):
            raise TypeError("quantity must be an integer")
        if nb is not None and (not isinstance(nb, int)):
            raise TypeError("nb must be an integer")
        if nb is None:
            raise RequiredParameterException("nb is required")
        if is_comment is not None and (not isinstance(is_comment, bool)):
            raise TypeError("isComment must be a boolean")
        if is_comment is None:
            is_comment = False
        if recipe is not None and (not isinstance(recipe, Recipe)):
            raise TypeError("recipe must be an instance of the Recipe class")
        if recipe is None:
            raise RequiredParameterException("recipe is required")

        # Do the add:
        e = Equipment.objects.get_or_create(name=name)[0]
        eir = EquipmentInRecipe(equipment=e, recipe=recipe, nb=nb, quantity=quantity if int(quantity) > 0 else None,
                                is_comment=is_comment)
        eir.save()

        return eir

    @staticmethod
    def add_new_list_to_recipe(equipments: list, recipe: Recipe) -> "list of EquipmentInRecipe":
        # Check parameters:
        if equipments is not None and (not isinstance(equipments, list)):
            raise TypeError("equipments must be a list")
        if equipments is None or len(equipments) == 0:
            raise RequiredParameterException("equipments is required and must be not empty")
        else:
            for equipment in equipments:
                req_keys = {
                    "name": False,
                    "quantity": False,
                    "nb": False,
                    "isComment": False
                }
                for key, value in equipment.items():
                    if key in req_keys:
                        req_keys[key] = True
                        if key == "name":
                            if value is not None and (not isinstance(value, str)):
                                raise TypeError("equipment: name must be a string")
                            if value is None or len(value) == 0:
                                raise RequiredParameterException("equipment: name must be not none or empty")
                        elif key == "quantity":
                            if value is not None and (not isinstance(value, int)):
                                raise TypeError("equipment: quantity must be an integer")
                            if value is None or value == 0:
                                raise RequiredParameterException("equipment: quantity must be not none and must be "
                                                                 "strictly higher than 0")
                        elif key == "nb":
                            if value is not None and (not isinstance(value, int)):
                                raise TypeError("equipment: nb must be an integer")
                            if value is None:
                                raise RequiredParameterException("equipment: nb must not be none")
                    else:
                        raise UnknownKeyException("equipment: unknown key: " + key)
                for key in req_keys:
                    if not req_keys[key]:
                        raise MissingKeyException("equipment: missing key: " + key)
        if recipe is not None and (not isinstance(recipe, Recipe)):
            raise TypeError("recipe must be an instance of the Recipe class")
        if recipe is None:
            raise RequiredParameterException("recipe is required")

        # Do the add:
        eir_list = []
        for equipment in equipments:
            # noinspection PyTypeChecker
            eir_list.append(CEquipment.add_new_to_recipe(equipment['name'], equipment["quantity"], equipment["nb"],
                                                         equipment['isComment'], recipe))

        return eir_list

    @staticmethod
    def build_html_for_equipments(recipe: Recipe) -> str:
        # Check parameters:
        if recipe is not None and (not isinstance(recipe, Recipe)):
            raise TypeError("recipe must be an instance of the Recipe class")
        if recipe is None:
            raise RequiredParameterException("recipe is required")

        equipments_query = recipe.equipmentinrecipe_set.iterator()
        equipments = []
        for eq in equipments_query:
            equipments.append(eq)
        equipments.sort(key=lambda k: k.nb)

        html = ""
        list_begin = False
        for eq in equipments:
            if not eq.is_comment:
                if not list_begin:
                    list_begin = True
                    html += "<ul>"
                html += "<li>" + str(eq.quantity) + " " + eq.equipment.name + "</li>"
            else:
                if list_begin:
                    list_begin = False
                    html += "</ul>"
                html += "<p>" + eq.equipment.name + "</p>"

        if list_begin:
            html += "</ul>"

        return html