#!/usr/bin/python3
"""
This file create recipes for debug only.
Used for test the application
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pywebcooking.settings')

import django

django.setup()

from main.controllers import *
from main.models import Category, UserProfile

title = input("Title: ")
description = input("Description: ")
tps_prep = int(input("Prep time: "))
tps_rep = int(input("Break time: "))
tps_cuis = int(input("Cook time: "))
picture_file = input("Picture file: ")
nb_people = int(input("Nb people: "))
nb_people_max = int(input("Nb people max: "))
precision = input("Precision: ")

category = Category.objects.get_or_create(name="Dessert", url="dessert", order=0)[0]
author = UserProfile.objects.get(user__username=input("Author username: "))

recipe = CRecipe.add_new(title=title, description=description, tps_prep=tps_prep, tps_rep=tps_rep, tps_cuis=tps_cuis,
                picture_file=picture_file, nb_people=nb_people, nb_people_max=nb_people_max, precision=precision,
                author=author, categories=[category])

print("Recipe added")

nb_igGroup = 0
nb_equipment = 0
nb_instruction = 0
nb_proposal = 0

def what_to_do_next():
    print("What to do next?")
    print("1 - Add an ingredient group")
    print("2 - Add an equipment")
    print("3 - Add an instruction")
    print("4 - Add a proposal")
    print("5 - Exit")


def add_ig_to_group(nb):
    quantity = int(input("Quantity: "))
    unit = input("Unit: ")
    name = input("Name: ")
    return {"name": name, "quantity": quantity, "unit": unit, "nb": nb}


def add_ig_group():
    global nb_igGroup, recipe
    nb_igGroup += 1
    name = input("Group name:")
    level = int(input("Level: "))
    nb = 0
    ingredients = []

    def what_to_do_next_ingr():
        print("What to do next?")
        print("1 - Add an ingredient to the group")
        print("2 - Exit")

    what_to_do_next_ingr()
    choice_ingr = int(input("Choice: "))
    while choice_ingr != 2:
        ingredients.append(add_ig_to_group(nb))
        what_to_do_next_ingr()
        choice_ingr = int(input("Choice: "))
        nb += 1
    CIngredientGroup.add_new(name, nb_igGroup, recipe, level, ingredients)


def add_equipment():
    global nb_equipment, recipe
    nb_equipment += 1
    name = input("Name: ")
    quantity = int(input("Quantity: "))
    CEquipment.add_new_to_recipe(name, quantity, nb_equipment, recipe)


def add_instruction():
    global nb_instruction, recipe
    nb_instruction += 1
    text_inst = input("Text: ")
    level = int(input("Level: "))
    CInstruction.add_new(text_inst, nb_instruction, recipe, level)


def add_proposal():
    global nb_proposal, recipe
    nb_proposal += 1
    text_prop = input("Text: ")
    CProposal.add_new_to_recipe(text_prop, nb_proposal, recipe)

what_to_do_next()
choice = int(input("Choice: "))
while choice != 5:
    if choice == 1:
        add_ig_group()
    elif choice == 2:
        add_equipment()
    elif choice == 3:
        add_instruction()
    elif choice == 4:
        add_proposal()
    what_to_do_next()
    choice = int(input("Choice: "))
