import os, errno, re, json

from django.utils.translation import ugettext as _

from pywebcooking import settings
from main.controllers import CRecipe, CIngredientGroup, CInstruction, CEquipment, CProposal
from main.models import UserProfile, Category, Recipe, IngredientGroup, EquipmentInRecipe, Instruction, Proposal, \
    MediaInRecipe


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
        except Category.DoesNotExist as e:
            return -1, _("Category does not exists: " + str(e))
        try:
            author = UserProfile.objects.get(user__username=user_url)
        except UserProfile.DoesNotExist:
            return -1, _("User not found. Please contact an administrator")

        # Save uploaded files:
        files_saved, files_renamed = Functions.__save_files(files, user_url)
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
            for group, files in files_saved.items():
                if type(files) == str:
                    os.remove(files)
                else:
                    for file in files:
                        os.remove(file)
            return -2, str(e)

        Functions.__add_media_files(recipe, files_saved)

        # Complete recipe:
        try:
            # Add ingredients:
            Functions.__save_ingredients(recipe, data["ingredients"], data["ingredients_groups"],
                                         data["ingredients_in_groups"])
            # Add equipments:
            if "equipments" in data and len(data["equipments"]) > 0:
                CEquipment.add_new_list_to_recipe(equipments=data["equipments"], recipe=recipe)
            # Add instructions:
            CInstruction.add_new_list(instructions=data["instructions"], recipe=recipe, files_replaces=files_renamed)
            # Add proposals:
            if "proposals" in data and len(data["proposals"]) > 0:
                CProposal.add_new_list_to_recipe(proposals=data["proposals"], recipe=recipe,
                                                 files_replaces=files_renamed)
        except Exception as e:
            recipe.delete()
            return -2, str(e)
        return recipe.pk, recipe.slug

    @staticmethod
    def __add_media_files(recipe: Recipe, medias: dict):
        CRecipe.add_media_file(recipe, medias["main_picture"], "main")
        if "other_pictures" in medias and len(medias["other_pictures"]) > 0:
            if type(medias["other_pictures"]) == list:
                for media in medias["other_pictures"]:
                    CRecipe.add_media_file(recipe, media, "other")
            else:
                CRecipe.add_media_file(recipe, medias["other_pictures"], "other")

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
            try:
                categories.append(Category.objects.get(name=cat))
            except Category.DoesNotExist:
                raise Category.DoesNotExist(cat)
        return categories

    @staticmethod
    def __save_file(file, user_url):
        save_dir = settings.BASE_DIR + settings.MEDIA_ROOT + user_url + "/"
        filename = file.name
        ext = re.search(r"\.\w+$", filename).group(0)
        base_name = filename[:-len(ext)]
        if not os.path.isdir(save_dir):
            Functions.mkdir_p(save_dir)
        add = 2
        while os.path.isfile(save_dir + filename):
            filename = base_name + "_" + str(add) + ext
            add += 1
        file_path = save_dir + filename
        with open(file_path, "wb") as my_file:
            my_file.write(file.read())
        if file_path.lower().endswith(".jpg") or file_path.lower().endswith(".jpeg"):
            jpegoptim = Functions.which("jpegoptim")
            print("jpegoptim", jpegoptim)
            if jpegoptim is not None:
                os.system(jpegoptim + " -s " + file_path)
        return filename

    @staticmethod
    def __save_files(files, user_url):
        files_saved = {}
        files_renamed = {}
        for f in files:
            files_list = files.getlist(f)
            if len(files_list) > 1:
                files_saved[f] = []
                for file in files_list:
                    filename = Functions.__save_file(file, user_url)
                    files_saved[f].append(filename)
                    if file.name != filename:
                        files_renamed[file.name] = filename
            else :
                filename = Functions.__save_file(files_list[0], user_url)
                files_saved[f] = filename
                if files_list[0].name != filename:
                    files_renamed[files_list[0].name] = filename

        return files_saved, files_renamed

    @staticmethod
    def get_data_dict(data: dict):
        is_obj = ["categories", "ingredients", "ingredients_groups", "ingredients_in_groups", "equipments",
                  "instructions", "proposals"]
        new_data = {}
        for key, value in data.items():
            if key in is_obj and type(value) == str:
                new_data[key] = json.loads(value)
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

    @staticmethod
    def which(program):
        import os

        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file

        return None
