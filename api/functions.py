import os, errno, re, json

from django.utils.translation import ugettext as _

from pywebcooking import settings
from main.controllers import CRecipe, CIngredientGroup, CInstruction, CEquipment, CProposal
from main.models import UserProfile, Category, Recipe


class Functions:

    @staticmethod
    def add_recipe(data, files, user_url):
        """
        Add a new recipe
        :param data: data of the recipe, full JSON loaded {dict}
        :param files: list of uploaded files
        :param user_url:
        :return:
        """
        try:
            cats = Functions.__get_categories_objects(data["categories"])
        except Category.DoesNotExist:
            return -1, _("Category does not exists")
        try:
            author = UserProfile.objects.get(user__username=user_url)
        except UserProfile.DoesNotExist:
            return -1, _("User not found. Please contact an administrator")

        # Save uploaded files:
        files_saved = Functions.__save_files(files, user_url)
        try:
            recipe = CRecipe.add_new(title=data["title"], description=data["description"], tps_prep=int(data["tps_prep"]),
                            tps_cuis=int(data["tps_cuis"]) if "tps_cuis" in data and int(data["tps_cuis"]) > 0 else None,
                            tps_rep=int(data["tps_rep"]) if "tps_rep" in data and int(data["tps_rep"]) > 0 else None,
                            picture_file=files_saved["main_picture"], nb_people=int(data["nb_people"]),
                            nb_people_max=int(data["nb_people_max"]) if "nb_people_max" in data and
                                                                        int(data["nb_people_max"]) > 0 else None,
                            author=author,
                            categories=cats, precision=data["precision"] if "precision" in data else "",
                            published=data["published"]=="1")
        except Exception as e:
            # TODO: remove files saved
            return -2, str(e)

        # Complete recipe:
        try:
            # Add ingredients:
            Functions.__save_ingredients(recipe, data["ingredients"], data["ingredients_groups"],
                                         data["ingredients_in_groups"])
            # Add equipments:
            if "equipments" in data and len(data["equipments"]) > 0:
                CEquipment.add_new_list_to_recipe(equipments=data["equipments"], recipe=recipe)
            # Add instructions:
            CInstruction.add_new_list(instructions=data["instructions"], recipe=recipe)
            # Add proposals:
            if "proposals" in data and len(data["proposals"]) > 0:
                CProposal.add_new_list_to_recipe(proposals=data["proposals"], recipe=recipe)
        except Exception as e:
            recipe.delete()
            return -2, str(e)
            # TODO: remove files saved
        return recipe.pk, None

    @staticmethod
    def __save_ingredients(recipe: Recipe, ingredients: dict, ingredients_groups: dict, ingredients_in_groups: dict):
        iig = {}
        for ig, ingrs in ingredients_in_groups.items():
            ingr_list = []
            for ingr in ingrs:
                ingr_list.append(ingredients[ingr])
            iig[ig] = ingr_list
        for ig_id, ig in ingredients_groups.items():
            CIngredientGroup.add_new(recipe=recipe, title=ig["title"], nb=int(ig["nb"]), level=int(ig["level"]),
                                     ingredients=iig[ig_id] if ig_id in iig else None)

    @staticmethod
    def __get_categories_objects(cats:list):
        categories = []
        for cat in cats:
            categories.append(Category.objects.get(name=cat))
        return categories

    @staticmethod
    def __save_files(files, user_url):
        files_saved = {}
        for f in files:
            save_dir = settings.BASE_DIR + settings.MEDIA_ROOT + user_url + "/"
            filename = files[f].name
            ext = re.search(r"\.\w+$", filename).group(0)
            base_name = filename[:-len(ext)]
            if not os.path.isdir(save_dir):
                Functions.mkdir_p(save_dir)
            add = 2
            while os.path.isfile(save_dir + filename):
                filename = base_name + "_" + str(add) + ext
                add += 1
            with open(save_dir + filename, "wb") as my_file:
                my_file.write(files[f].read())
            files_saved[f] = filename
        return files_saved

    @staticmethod
    def get_data_dict(data: dict):
        new_data = {}
        for key, value in data.items():
            if type(value) == str and len(value) > 0 and (value[0] == "{" or value[0] == "["):
                new_data[key] = json.loads(value)
                if value[0] == "[" and len(new_data[key]) > 0 and type(new_data[key][0]) == str \
                        and len(new_data[key][0]) > 0 and (new_data[key][0][0] == "{"
                                                           or new_data[key][0][0] == "["):
                    for it in range(0, len(new_data[key])):
                        new_data[key][it] = json.loads(new_data[key][it])
                elif value[0] == "{" and len(new_data[key]) > 0:
                    first_item = list(new_data[key].keys())[0]
                    if type(new_data[key][first_item]) == str \
                        and len(new_data[key][first_item]) > 0 and (new_data[key][first_item][0] == "{" \
                                                                    or new_data[key][first_item][0] == "["):
                        for k, v in new_data[key].items():
                            new_data[key][k] = json.loads(v)

            else:
                new_data[key] = value
        return new_data

    @staticmethod
    def mkdir_p(path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise