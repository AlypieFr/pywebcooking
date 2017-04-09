#!/usr/bin/env python3

import argparse
import os
import re
import django

from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pywebcooking.settings')

django.setup()

from main.controllers import CRecipe
from main.models import Recipe

parser = argparse.ArgumentParser(description='Rebuild html for all recipes or for some recipes.')
parser.add_argument("--id", help="Id of the recipe to rebuild", type=int)
parser.add_argument("--slug", help="Slug of the recipe to rebuild")
parser.add_argument("--from-date", help="Rebuild html for recipes from the date specified.\nDate format: YYYY+MM-DD")
parser.add_argument("--to-date", help="Rebuild html for recipes to the date specified.\nDate format: YYYY+MM-DD")

args = parser.parse_args()

if args.id is not None and args.slug is not None:
    print("ERROR: Parameters \"id\" and \"slug\" are mutually exclusive.")
    exit(1)

recipes = Recipe.objects.all()

if args.id is not None:
    recipes = recipes.filter(id=args.id)
elif args.slug is not None:
    recipes = recipes.filter(slug=args.slug)

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

if len(recipes) == 0:
    print("ERROR: No recipe match to your query. Exciting...")

for recipe in recipes:
    print("Processing recipe {0} ({1})...".format(recipe.title, recipe.id))
    CRecipe.build_html_recipe(recipe)

print("")
print("DONE!")
