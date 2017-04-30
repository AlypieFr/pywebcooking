#!/usr/bin/env python3

import argparse
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pywebcooking.settings')

django.setup()

from pywebcooking import settings

from api.functions import Functions
from main.models import MediaInRecipe

parser = argparse.ArgumentParser(description='Tinify pictures for all recipes or for some files.')
parser.add_argument("--file", help="Tinify only given file")

args = parser.parse_args()

if args.file is not None:
    Functions.tinify_pict(os.path.abspath(args.file))
else:
    for media in MediaInRecipe.objects.all():
        file_path = settings.BASE_DIR + settings.MEDIA_ROOT + media.recipe.author.url + "/" + media.media

        print("Processing file {0}...".format(file_path))

        Functions.tinify_pict(file_path)

print("")
print("Done!")
