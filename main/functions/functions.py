import os
import re
import unicodedata

from PIL import Image
from main.config import RecipeConfig

# import the logging library
import logging


class Functions:

    # Get an instance of a logger
    logger = logging.getLogger(__name__)

    @staticmethod
    def remove_accents(input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

    @staticmethod
    def insert_picture(item: str, author_url: str):
        pict_iter = re.finditer(r"\[PICT:(\w+):(\d+):(\d+)(:center)?:([^]]+)]", item)
        for pict in pict_iter:
            bal_img = pict.group(0)
            printable = pict.group(1)
            width = pict.group(2)
            height = pict.group(3)
            center = pict.group(4) is not None
            img = pict.group(5)
            url = "/media/" + author_url + "/" + img
            img_html = "<a href=\"" + url + "\" data-lightbox='illustration'><img src=\"" + url + "\" width=\"" + width + \
                       "\" alt=\"Illustration\" class=\""
            if printable == "print-only":
                img_html += "print-only "
            if printable == "no-print":
                img_html += "no-print "
            if center:
                img_html += "center "
            img_html += "autoresize\"/></a>"
            item = item.replace(bal_img, img_html)
        return item

    @staticmethod
    def replace_files(text: str, files_replace: dict):
        pict_iter = re.finditer(r"\[PICT:(\w+):(\d+):(\d+)(:center)?:([^]]+)]", text)
        for pict in pict_iter:
            img = pict.group(5)
            if img in files_replace:
                old_pict_bal = pict.group(0)
                new_pict_bal = old_pict_bal.replace(img, files_replace[img])
                text = text.replace(old_pict_bal, new_pict_bal)
        return text

    @staticmethod
    def add_illustration_thumbnails(file):
        """
        Build thumbnails pictures
        :param file: full path of the illustration file
        """
        if os.path.isfile(file):
            try:
                im = Image.open(file)
                size = (int(RecipeConfig.photo_in_recipe_width), 1000000)
                im.thumbnail(size, Image.ANTIALIAS)
                file_parts = os.path.splitext(file)
                out_file = file_parts[0] + "_thumb_" + RecipeConfig.photo_in_recipe_width + file_parts[1]
                im.save(out_file, "JPEG" if file_parts[1].lower() in (".jpg", ".jpeg") else "PNG")
                if RecipeConfig.photo_in_index_width != RecipeConfig.photo_in_recipe_width:
                    im = Image.open(file)
                    size = (int(RecipeConfig.photo_in_index_width), 1000000)
                    im.thumbnail(size, Image.ANTIALIAS)
                    file_parts = os.path.splitext(file)
                    out_file = file_parts[0] + "_thumb_" + RecipeConfig.photo_in_index_width + file_parts[1]
                    im.save(out_file, "JPEG" if file_parts[1].lower() in (".jpg", ".jpeg") else "PNG")
            except IOError:
                Functions.logger.error("Unable to build thumbnails for the picture {0}: IO error".format(file))
        else:
            Functions.logger.error("Unable to build thumbnails for the picture {0}: file not found".format(file))