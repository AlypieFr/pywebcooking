from pywebcooking.settings import MEDIA_ROOT

from main.models import Recipe, Category, IngredientInGroup, UserProfile, MediaInRecipe
from django.contrib.auth.models import User

from main.functions.exceptions import RequiredParameterException, BadParameterException

from main.controllers.C_IngredientGroup import CIngredientGroup
from main.controllers.C_Equipment import CEquipment
from main.controllers.C_Instruction import CInstruction
from main.controllers.C_Proposal import CProposal

from main.config import RecipeConfig

import datetime
import unicodedata
import re


class CRecipe:

    @staticmethod
    def add_new(title: str, description: str, tps_prep: int, picture_file: str, nb_people: int, author: UserProfile,
                categories: "list of Category" = None, pub_date: datetime = datetime.datetime.now(),
                tps_rep: int = None, tps_cuis: int = None, nb_people_max: int = None, precision: str = None, excerpt: str = None,
                enable_comments: bool = True, published: bool = True, coup_de_coeur: int = 0) -> Recipe:
        """
        Add new recipe
        :param title: title of the recipe {string} [REQ]
        :param description: description of the recipe {string} [REQ]
        :param tps_prep: time needed to prepare the recipe, without "cuisson" time - in minutes {int} [REQ]
        :param picture_file: the illustration filename of the recipe {string} [REQ]
        :param nb_people: the number of people for this recipe {int} [REQ]
        :param author: the author of this recipe {User} [REQ]
        :param categories: the list of categories for this recipe {list<Category>} [REQ]
        :param pub_date: the publication date - if not sent, use current date {datetime} [OPT]
        :param tps_rep: the break ("repos") time {int} [OPT]
        :param tps_cuis: the cooking ("cuisson") time {int} [OPT]
        :param nb_people_max: the number of people for this recipe (max value, if filled, the min value is nb_people)
        :param precision: the precision to add to the ingredients header just after nb people
        :param excerpt: the excerpt of the recipe (shown in index pages)
        :param enable_comments: enable comments for this recipe
        :param published: is the recipe publicly published
        [OPT]
        :return: the recipe created {Recipe}
        """

        # Check parameters:
        if title is not None and (not isinstance(title, str)):
            raise TypeError("title must be a string")
        if title is None or len(title) == 0:
            raise RequiredParameterException("title is required and must be not empty")
        if description is not None and (not isinstance(description, str)):
            raise TypeError("description must be a string")
        if description is None or len(description) == 0:
            raise RequiredParameterException("description is required and must be not empty")
        if tps_prep is not None and (not isinstance(tps_prep, int)):
            raise TypeError("tps_prep must be an integer")
        if tps_prep is None or tps_prep == 0:
            raise RequiredParameterException("tps_prep is required and must be greater than 0")
        if tps_rep is not None and (not isinstance(tps_rep, int)):
            raise TypeError("tps_rep must be an integer")
        if tps_rep is not None and tps_rep == 0:
            raise BadParameterException("tps_rep is given but is equal to 0")
        if tps_cuis is not None and (not isinstance(tps_cuis, int)):
            raise TypeError("tps_cuis must be an integer")
        if tps_cuis is not None and tps_cuis == 0:
            raise BadParameterException("tps_cuis is given but is equal to 0")
        if picture_file is not None and (not isinstance(picture_file, str)):
            raise TypeError("picture_file must be a string")
        if picture_file is None or len(picture_file) == 0:
            raise RequiredParameterException("picture_file is required and must be not empty")
        if nb_people is not None and (not isinstance(nb_people, int)):
            raise TypeError("nb_people must be an integer")
        if nb_people is None or nb_people == 0:
            raise RequiredParameterException("nb_people is required and must be greater than 0")
        if author is not None and (not isinstance(author, UserProfile)):
            raise TypeError("author must be an instance of UserProfile object")
        if author is None:
            raise RequiredParameterException("author is required")
        if nb_people_max is not None and (not isinstance(nb_people_max, int)):
            raise TypeError("nb_people_max must be an integer (or None)")
        if precision is not None and (not isinstance(precision, str)):
            raise TypeError("precision must be a string (or None)")
        if categories is None:
            raise RequiredParameterException("categories is required")
        else:
            if not isinstance(categories, list):
                raise TypeError("categories must be a list")
            for cat in categories:
                if not isinstance(cat, Category):
                    raise TypeError("categories must be a list of Category object")
        if coup_de_coeur is None:
            coup_de_coeur = 0
        elif not isinstance(coup_de_coeur, int):
            raise TypeError("coup_de_coeur must be an int (or None)")
        elif coup_de_coeur not in (0, 1, 2, 3):
            raise BadParameterException("coup_de_coeur must be between 0 and 3")

        if excerpt is None:
            desc_words = description.split(" ")
            excerpt_words = desc_words[0:max(len(desc_words), 50)]  # TODO: set the true number of words
            excerpt = " ".join(excerpt_words)

        # Make slug:
        slug = CRecipe.build_recipe_slug(title)

        # Create recipe:
        r = Recipe(title=title, description=description, tps_prep=tps_prep, tps_rep=tps_rep, tps_cuis=tps_cuis,
                   picture_file=picture_file, nb_people=nb_people, nb_people_max=nb_people_max, precision=precision,
                   author=author, pub_date=pub_date, enable_comments=enable_comments, excerpt=excerpt,
                   published=published, slug=slug, coup_de_coeur=coup_de_coeur)
        r.save()

        # Add categories:
        CRecipe.add_categories(r, categories)

        return r

    @staticmethod
    def update(recipe: Recipe, title: str = None, description: str = None, tps_prep: int = None,
               picture_file: str = None, nb_people: int = None, author: UserProfile = None,
               categories: "list of Category" = None, pub_date: datetime = datetime.datetime.now(),
               tps_rep: int = None, tps_cuis: int = None, nb_people_max: int = None, precision: str = None,
               excerpt: str = None, enable_comments: bool = True, published: bool = True) -> Recipe:
        """
                Add new recipe
                :param title: title of the recipe {string} [REQ]
                :param description: description of the recipe {string} [REQ]
                :param tps_prep: time needed to prepare the recipe, without "cuisson" time - in minutes {int} [REQ]
                :param picture_file: the illustration filename of the recipe {string} [REQ]
                :param nb_people: the number of people for this recipe {int} [REQ]
                :param author: the author of this recipe {User} [REQ]
                :param categories: the list of categories for this recipe {list<Category>} [REQ]
                :param pub_date: the publication date - if not sent, use current date {datetime} [OPT]
                :param tps_rep: the break ("repos") time {int} [OPT]
                :param tps_cuis: the cooking ("cuisson") time {int} [OPT]
                :param nb_people_max: the number of people for this recipe (max value, if filled, the min value is nb_people)
                :param precision: the precision to add to the ingredients header just after nb people
                :param excerpt: the excerpt of the recipe (shown in index pages)
                :param enable_comments: enable comments for this recipe
                :param published: is the recipe publicly published
                [OPT]
                :return: the recipe created {Recipe}
                """

        # Check parameters:
        if recipe is None:
            raise RequiredParameterException("recipe parameter is required")
        if recipe is not None and (not isinstance(recipe, Recipe)):
            raise TypeError("recipe must be an instance of the Recipe object")
        if title is not None and (not isinstance(title, str)):
            raise TypeError("title must be a string")
        if description is not None and (not isinstance(description, str)):
            raise TypeError("description must be a string")
        if tps_prep is not None and (not isinstance(tps_prep, int)):
            raise TypeError("tps_prep must be an integer")
        if tps_prep is not None and tps_prep == 0:
            raise BadParameterException("tps_prep is given but is equal to 0")
        if tps_rep is not None and (not isinstance(tps_rep, int)):
            raise TypeError("tps_rep must be an integer")
        if tps_cuis is not None and (not isinstance(tps_cuis, int)):
            raise TypeError("tps_cuis must be an integer")
        if picture_file is not None and (not isinstance(picture_file, str)):
            raise TypeError("picture_file must be a string")
        if nb_people is not None and (not isinstance(nb_people, int)):
            raise TypeError("nb_people must be an integer")
        if author is not None and (not isinstance(author, UserProfile)):
            raise TypeError("author must be an instance of UserProfile object")
        if nb_people_max is not None and (not isinstance(nb_people_max, int)):
            raise TypeError("nb_people_max must be an integer (or None)")
        if precision is not None and (not isinstance(precision, str)):
            raise TypeError("precision must be a string (or None)")
        if categories is not None:
            if not isinstance(categories, list):
                raise TypeError("categories must be a list")
            for cat in categories:
                if not isinstance(cat, Category):
                    raise TypeError("categories must be a list of Category object")

        if title is not None:
            recipe.title = title
        if description is not None:
            recipe.description = description
            if excerpt is None:
                desc_words = description.split(" ")
                excerpt_words = desc_words[0:max(len(desc_words), 50)]  # TODO: set the true number of words
                excerpt = " ".join(excerpt_words)
                recipe.excerpt = excerpt
        if tps_prep is not None:
            recipe.tps_prep = tps_prep
        if tps_cuis is not None:
            recipe.tps_cuis = tps_cuis if tps_cuis > 0 else None
        if tps_rep is not None:
            recipe.tps_rep = tps_rep if tps_rep > 0 else None
        if picture_file is not None:
            recipe.picture_file = picture_file
        if nb_people is not None:
            recipe.nb_people = nb_people
        if nb_people_max is not None:
            recipe.nb_people_max = nb_people_max if nb_people_max > 0 else None
        if precision is not None:
            recipe.precision = precision if len(precision) > 0 else None
        if author is not None:
            recipe.author = author
        if pub_date is not None:
            recipe.pub_date = pub_date
        recipe.enable_comments = enable_comments
        recipe.published = published
        recipe.last_modif = datetime.datetime.now()
        recipe.save()

        if categories is not None:
            CRecipe.set_categories(recipe, categories)

        return recipe

    @staticmethod
    def get_author_recipes_data(author: User) -> list:
        recipes = Recipe.objects.filter(author__user=author)
        recipes_data = []
        for recipe in recipes:
            recipes_data.append(CRecipe.get_recipe_data(recipe))
        return recipes_data

    @staticmethod
    def get_recipe_data_from_id(id_recipe: int, author: str=None, details: bool=False) -> dict:
        if author is None:
            return CRecipe.get_recipe_data(Recipe.objects.get(id=id_recipe), details)
        else:
            recipe = Recipe.objects.get(id=id_recipe, author__user=author)
            return CRecipe.get_recipe_data(recipe, details)

    @staticmethod
    def get_recipe_data_from_slug(slug: str, author: str=None, details: bool=False) -> dict:
        if author is None:
            return CRecipe.get_recipe_data(Recipe.objects.get(slug=slug), details)
        else:
            recipe = Recipe.objects.get(slug=slug, author__user=author)
            return CRecipe.get_recipe_data(recipe, details)

    @staticmethod
    def get_recipe_data(recipe: Recipe, details=False) -> dict:
        """
        get data of a recipe
        :param recipe: the recipe to get the data
        :return: data of the recipe
        """
        data = {"author": recipe.author.user.username}
        vars_recipe = vars(recipe)
        for key in vars_recipe:
            if not key.startswith("_") and key != "author_id":
                data[key] = vars_recipe[key]
        data["picture_url"] = "/media/" + recipe.author.user.username + "/" + recipe.picture_file
        categories = []
        for cat in recipe.category.all():
            categories.append(cat.name)
        data["categories"] = categories
        if details:
            ingredients = []
            ingredients_groups = recipe.ingredientgroup_set
            for ingredients_group in ingredients_groups.all().order_by("nb"):
                ig = {
                    "title": ingredients_group.title,
                    "nb": ingredients_group.nb,
                    "level": ingredients_group.level,
                    "ingredients": []
                }
                ingredients_in_group = IngredientInGroup.objects.filter(ingredientGroup=ingredients_group)\
                    .order_by("nb")
                for iig in ingredients_in_group:
                    ig["ingredients"].append({
                        "name": iig.ingredient.name,
                        "quantity": iig.quantity,
                        "unit": iig.unit,
                        "nb": iig.nb
                    })
                ingredients.append(ig)
            data["ingredients"] = ingredients
            equipments = []
            for eq in recipe.equipmentinrecipe_set.all().order_by("nb"):
                equipment = {
                    "name": eq.equipment.name,
                    "quantity": eq.quantity,
                    "nb": eq.nb,
                    "is_comment": eq.is_comment
                }
                equipments.append(equipment)
            data["equipments"] = equipments
            instructions = []
            for instr in recipe.instruction_set.all().order_by("nb"):
                instruction = {
                    "text_inst": instr.text_inst,
                    "nb": instr.nb,
                    "level": instr.level
                }
                instructions.append(instruction)
            data["instructions"] = instructions
            proposals = []
            for prop in recipe.proposal_set.all().order_by("nb"):
                proposal = {
                    "text_prop": prop.text_prop,
                    "nb": prop.nb,
                    "is_comment": prop.is_comment
                }
                proposals.append(proposal)
            data["proposals"] = proposals
        return data

    @staticmethod
    def add_categories(recipe: Recipe, categories: "list of Categories"):
        # Check parameters:
        if not isinstance(categories, list):
            raise TypeError("categories must be a list")
        for cat in categories:
            if not isinstance(cat, Category):
                raise TypeError("categories must be a list of Category object")

        # Do the staff:
        for cat in categories:
            recipe.category.add(cat)

    @staticmethod
    def set_categories(recipe: Recipe, categories: "list of Categories"):
        # Check parameters:
        if not isinstance(categories, list):
            raise TypeError("categories must be a list")
        for cat in categories:
            if not isinstance(cat, Category):
                raise TypeError("categories must be a list of Category object")

        # Do the staff:
        Recipe.category.through.objects.filter(recipe=recipe).delete() # Delete all categories from the recipe
        for cat in categories:
            recipe.category.add(cat)

    @staticmethod
    def build_recipe_slug(title: str):
        slug = title.lower()
        slug = slug.replace(" ", "_")
        slug = str(unicodedata.normalize('NFKD', slug).encode('ASCII', 'ignore'), 'utf-8')  # Remove accents
        slug = re.sub(r'\W', "", slug)
        slug = re.compile(r'[a-z].*[a-z]').search(slug).group(0)
        slug_orig = slug
        i = 2
        while Recipe.objects.filter(slug=slug).count() > 0:
            slug = slug_orig + "_" + str(i)
            i += 1
        return slug

    @staticmethod
    def __get_times_details_html(recipe: Recipe):
        """
        Get html of the times of the recipe
        :param recipe: the recipe to build times
        :return: the html of the times
        """
        html = "<div id='timesDetail'>"
        # Preparation time:
        if recipe.tps_prep is None or recipe.tps_prep == 0:
            raise BadParameterException("tps_prep is required and must be higher than 0")
        tps_prep_h = int(recipe.tps_prep / 60)
        tps_prep_min = recipe.tps_prep % 60
        html += "<strong>" + RecipeConfig.timePreparation
        if tps_prep_h > 0:
            html += " " + str(tps_prep_h) + " h"
        if tps_prep_min > 0:
            html += " " + str(tps_prep_min) + " min"

        # Break time:
        if recipe.tps_rep is not None and recipe.tps_rep > 0:
            tps_rep_j = int(recipe.tps_rep / 1440)
            tps_rep_h = int((recipe.tps_rep % 1440) / 60)
            tps_rep_min = recipe.tps_rep % 60
            html += "<br/>" + RecipeConfig.timeRep
            if tps_rep_j > 0:
                html += " " + str(tps_rep_j) + " j"
            if tps_rep_h > 0:
                html += " " + str(tps_rep_h) + " h"
            if tps_rep_min > 0:
                html += " " + str(tps_rep_min) + " min"

        # Cook time:
        if recipe.tps_cuis is not None and recipe.tps_cuis > 0:
            tps_cuis_h = int(recipe.tps_cuis / 60)
            tps_cuis_min = recipe.tps_cuis % 60
            html += "<br/>" + RecipeConfig.timeCuis
            if tps_cuis_h > 0:
                html += " " + str(tps_cuis_h) + " h"
            if tps_cuis_min > 0:
                html += " " + str(tps_cuis_min) + " min"

        # End times:
        html += "</strong></div>"
        return html

    @staticmethod
    def get_recipe_from_slug(slug: str) -> Recipe:
        try:
            recipe = Recipe.objects.get(slug=slug)
        except Recipe.DoesNotExist:
            return None
        return recipe

    @staticmethod
    def get_recipe_html_from_slug(slug: str) -> str:
        try:
            recipe = Recipe.objects.get(slug=slug)
        except Recipe.DoesNotExist:
            return None
        return CRecipe.get_recipe_html(recipe)

    @staticmethod
    def build_html_recipe(recipe: Recipe) -> str:
        if recipe is None:
            raise RequiredParameterException("recipe is required")
        if not isinstance(recipe, Recipe):
            raise TypeError("recipe must be an instance of the Recipe class")

        # Start html:
        html = "<div id='illustration_desc'>"

        # Add picture:
        html += "<div id='illustration'><a href='" + MEDIA_ROOT + recipe.author.user.username + "/" + recipe.picture_file + "'><img " \
                                                                                                                            "class='shadow' title='" + recipe.title + "' src='" + MEDIA_ROOT + recipe.author.user.username + "/" + \
                recipe.picture_file + "' alt='illustration' width='" + RecipeConfig.photo_in_recipe_width + \
                "' /></a></div>"

        # Add description:
        html += "<div id='description'><p>" + recipe.description + "</p></div>"

        # End masquer div:
        html += "</div>"

        # time details:
        html += CRecipe.__get_times_details_html(recipe)

        # Ingredients headers:
        html += "<div id='ingredientsAndEquipments'><div id='ingredients'>"
        html += "<p id='ingredientsHeader'><strong>"
        if recipe.nb_people_max is not None and recipe.nb_people_max > 0:
            if recipe.precision is not None and len(recipe.precision) > 0:
                html += RecipeConfig.ingredients_range_long % (recipe.nb_people, recipe.nb_people_max, recipe.precision)
            else:
                html += RecipeConfig.ingredients_range_short % (recipe.nb_people, recipe.nb_people_max)
        else:
            if recipe.precision is not None and len(recipe.precision) > 0:
                if recipe.nb_people > 1:
                    html += RecipeConfig.ingredients_long % (recipe.nb_people, recipe.precision)
                else:
                    html += RecipeConfig.ingredients_long_1p(recipe.nb_people, recipe.precision)
            else:
                if recipe.nb_people > 1:
                    html += RecipeConfig.ingredients_short % recipe.nb_people
                else:
                    html += RecipeConfig.ingredients_short_1p % recipe.nb_people
        html += "</strong></p>"

        # Ingredients:
        html += CIngredientGroup.build_html_for_ingredients(recipe)

        html += "</div>"  # Close ingredients div

        # Equipment:
        if recipe.equipmentinrecipe_set.count() > 0:
            html += "<div id='equipments'>"
            html += "<p id='equipmentHeader'><strong>" + RecipeConfig.equipment + "</strong></p>"
            html += CEquipment.build_html_for_equipments(recipe)
            html += "</div>"

        html += "</div>"  # Close Ingredients and equipments div

        # Instructions:
        html += "<div id='instructions'>"
        html += "<p id='instructionsHeader'><strong>" + RecipeConfig.instructions + "</strong></p>"
        html += CInstruction.build_html_for_instructions(recipe)
        html += "</div>"

        # Proposals:
        if recipe.proposal_set.count() > 0:
            html += "<div id='proposals'>"
            html += "<p id='proposalsHeader'><strong>" + RecipeConfig.proposals + "</strong></p>"
            html += CProposal.build_html_for_proposals(recipe)
            html += "</div>"

        recipe.html = html
        recipe.save()

        return html

    @staticmethod
    def get_recipe_html(recipe: Recipe) -> str:
        """
        Get the html of the full recipe
        :param recipe:
        :return:
        """
        if recipe is None:
            raise RequiredParameterException("recipe is required")
        if not isinstance(recipe, Recipe):
            raise TypeError("recipe must be an instance of the Recipe class")

        if recipe.html is not None:
            return recipe.html

        html = CRecipe.build_html_recipe(recipe)

        return html

    @staticmethod
    def add_media_file(recipe: Recipe, media: str, type: str):
        if type == "main":
            MediaInRecipe.objects.filter(recipe=recipe, type="main").delete()
            MediaInRecipe.objects.create(recipe=recipe, media=media, type=type)
        else:
            MediaInRecipe.objects.get_or_create(recipe=recipe, media=media, type=type)