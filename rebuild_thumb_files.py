#!/usr/bin/env python3

import argparse
import os
import re
import django
import glob

from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pywebcooking.settings')

django.setup()

from pywebcooking import settings

from main.models import Recipe
from main.models import MediaInRecipe
from main.functions import Functions

parser = argparse.ArgumentParser(description='Rebuild thumbnail files for all recipes or for some recipes.')
parser.add_argument("--id", help="Id of the recipe to rebuild", type=int)
parser.add_argument("--slug", help="Slug of the recipe to rebuild")
parser.add_argument("--from-date", help="Rebuild html for recipes from the date specified.\nDate format: YYYY+MM-DD")
parser.add_argument("--to-date", help="Rebuild html for recipes to the date specified.\nDate format: YYYY+MM-DD")

args = parser.parse_args()

if args.id is not None and args.slug is not None:
    print("ERROR: Parameters \"id\" and \"slug\" are mutually exclusive.")
    exit(1)

recipes = Recipe.objects.all()
all_r = True

if args.id is not None:
    recipes = recipes.filter(id=args.id)
    all_r = False
elif args.slug is not None:
    recipes = recipes.filter(slug=args.slug)
    all_r = False

match_string = r"(\d{4})-(\d{2})-(\d{2})"
if args.from_date:
    match = re.match(match_string, args.from_date)
    if match:
        recipes = recipes.filter(pub_date__gte=timezone.datetime(int(match.group(1)), int(match.group(2)),
                                                                 int(match.group(3)),
                                                                 tzinfo=timezone.get_current_timezone()))

if args.to_date:
    match = re.match(match_string, args.to_date)
    if match:
        recipes = recipes.filter(pub_date__lte=timezone.datetime(int(match.group(1)), int(match.group(2)),
                                                                 int(match.group(3)), 23, 59, 59,
                                                                 tzinfo=timezone.get_current_timezone()))

if all_r:
    main_files = MediaInRecipe.objects.filter(type="main")
else:
    main_files = MediaInRecipe.objects.filter(type="main", recipe__in=recipes)

for main_file in main_files:
    file_path = settings.BASE_DIR + settings.MEDIA_ROOT + main_file.recipe.author.url + "/" + main_file.media

    print("Processing file {0}...".format(file_path))

    # Remove old thumb files:
    thumb_files = os.path.splitext(file_path)[0] + "_thumb_*"
    for thumb_file in glob.glob(thumb_files):
        os.remove(thumb_file)

    # Create new ones:
    Functions.add_illustration_thumbnails(file_path)

print("")
print("DONE!")
