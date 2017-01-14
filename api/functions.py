import os, errno, re

from django.core.files import File
from pywebcooking import settings
from main.controllers import CRecipe, CIngredientGroup, CInstruction, CEquipment, CProposal


class Functions:

    @staticmethod
    def add_recipe(data, files, user_url):
        main_picture = None
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
            if f == "main_picture":
                main_picture = filename
        print("MAIN PICTURE", main_picture)
        return -1  # TODO: the id of the recipe

    @staticmethod
    def mkdir_p(path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise