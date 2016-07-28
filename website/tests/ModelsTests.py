from django.test import TestCase

from website.models import User, Category, Recipe, IngredientGroup, IngredientInGroup, Instruction

from website.controllers import CRecipe, CIngredientGroup, CInstruction

from datetime import datetime


class ModelsTests(TestCase):
    def recipe_test(self, title: str, description: str, tps_prep: int, picture_file: str, nb_people: int, author: User,
                    categories: "list of Category" = None, pub_date: datetime = datetime.now(), tps_rep: int = None,
                    tps_cuis: int = None, nb_people_max: int = None):
        r = CRecipe.add_new(title=title, description=description, tps_prep=tps_prep, picture_file=picture_file,
                            nb_people=nb_people, author=author, categories=categories, pub_date=pub_date,
                            tps_rep=tps_rep, tps_cuis=tps_cuis, nb_people_max=nb_people_max)
        self.assertIs(r.id is None, False)
        rget = Recipe.objects.get(pk=r.pk)
        vars_orig = vars(r)
        vars_get = vars(rget)
        for key in vars_orig:
            if not key.startswith("_"):
                self.assertIs(key in vars_get, True)
                self.assertEqual(vars_orig[key], vars_get[key])
        return r

    def add_new_recipe_minimalist(self):
        title = "Title of the recipe"
        description = "My description"
        tps_prep = 20
        picture_file = "myFile.jpg"
        nb_people = 4
        author = User(first_name="Floréal", last_name="Cabanettes", email="test@gmail.com")
        author.save()
        cat = Category(name="Category1", url="category1")
        cat.save()
        categories = [cat]
        r = self.recipe_test(title, description, tps_prep, picture_file, nb_people, author, categories)
        return r

    def test_add_new_ingredientGroup(self):
        ingr1 = {"name": "Carotte", "quantity": 2, "nb": 1, "unit": ""}
        ingr2 = {"nb": 2, "name": "Pommes de terre", "quantity": 400, "unit": "g"}
        ingrs = [ingr1, ingr2]
        r = self.add_new_recipe_minimalist()
        ig = CIngredientGroup.add_new("Pour la pâte:", 1, r, 0, ingrs)
        self.assertIs(ig.id is None, False)
        ig_get = IngredientGroup.objects.get(pk=ig.pk)
        self.assertEqual(ig_get.title, ig.title)
        self.assertEqual(ig_get.nb, ig.nb)
        self.assertEqual(ig_get.level, ig.level)
        iig_gets = IngredientInGroup.objects.filter(ingredientGroup=ig_get)
        for iigGet in iig_gets:
            if iigGet.ingredient.name == ingr1["name"]:
                ingr = ingr1
            else:
                ingr = ingr2
            self.assertEqual(iigGet.ingredient.name, ingr["name"])
            self.assertEqual(iigGet.quantity, ingr["quantity"])
            self.assertEqual(iigGet.nb, ingr["nb"])
            self.assertEqual(iigGet.unit, ingr["unit"])

    def test_add_new_instruction(self):
        r = self.add_new_recipe_minimalist()
        inst = CInstruction.add_new("A new instruction", 0, r)
        self.assertIs(inst.id is None, False)
        inst_get = Instruction.objects.get(pk=inst.id)
        vars_orig = vars(inst)
        vars_get = vars(inst_get)
        for key in vars_orig:
            if not key.startswith("_"):
                self.assertIs(key in vars_get, True)
                self.assertEqual(vars_orig[key], vars_get[key])

    def test_add_new_instruction_list(self):
        inst_list = [{
            "nb": 0,
            "level": 2,
            "text_inst": "My instruction 1"
        }, {
            "nb": 1,
            "text_inst": "My instruction 2"
        }]
        r = self.add_new_recipe_minimalist()
        CInstruction.add_new_list(inst_list, r)
        instr1 = Instruction.objects.get(text_inst="My instruction 1")
        self.assertEqual(instr1.nb, 0)
        self.assertEqual(instr1.level, 2)
        instr2 = Instruction.objects.get(text_inst="My instruction 2")
        self.assertEqual(instr2.nb, 1)
        self.assertEqual(instr2.level, 0)
