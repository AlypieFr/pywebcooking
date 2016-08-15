from django.test import TestCase

from website.models import User, Category, Recipe, IngredientGroup, IngredientInGroup, Instruction, Equipment, \
    EquipmentInRecipe, Proposal, Comment

from website.controllers import CRecipe, CIngredientGroup, CInstruction, CEquipment, CProposal, CComment

from website.functions.exceptions import *

from datetime import datetime


class TModels(TestCase):
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

    def test_add_new_equipment_to_recipe(self):
        equip_name = "My equipment 1"
        r = self.add_new_recipe_minimalist()
        eir = CEquipment.add_new_to_recipe(name=equip_name, quantity=1, nb=0, recipe=r)
        self.assertIs(eir.id is None, False)
        self.assertEqual(eir.equipment.name, equip_name)
        self.assertEqual(eir.quantity, 1)
        self.assertEqual(eir.nb, 0)
        self.assertEqual(eir.recipe.id, r.id)
        e_get = Equipment.objects.get(name="My equipment 1")
        eir_get = EquipmentInRecipe.objects.get(equipment=e_get)
        self.assertEqual(eir_get.equipment.name, equip_name)
        self.assertEqual(eir_get.quantity, eir.quantity)
        self.assertEqual(eir_get.nb, eir.nb)
        self.assertEqual(eir_get.recipe.id, r.id)

    def test_add_new_equipment_list_to_recipe(self):
        equipments = [{
            "name": "My equipment 2",
            "quantity": 1,
            "nb": 0
        }, {
            "name": "My equipment 3",
            "quantity": 2,
            "nb": 1
        }]
        r = self.add_new_recipe_minimalist()
        eir_list = CEquipment.add_new_list_to_recipe(equipments, r)
        for eir in eir_list:
            equip_name = eir.equipment.name
            e_get = Equipment.objects.get(name=equip_name)
            eir_get = EquipmentInRecipe.objects.get(equipment=e_get)
            self.assertEqual(eir_get.equipment.name, equip_name)
            self.assertEqual(eir_get.quantity, eir.quantity)
            self.assertEqual(eir_get.nb, eir.nb)
            self.assertEqual(eir_get.recipe.id, r.id)

    def test_add_new_proposal(self):
        r = self.add_new_recipe_minimalist()
        p = CProposal.add_new_to_recipe("My proposal 1", 0, r)
        p_get = Proposal.objects.get(text_cons="My proposal 1")
        self.assertIs(p_get.id is None, False)
        vars_orig = vars(p)
        vars_get = vars(p_get)
        for key in vars_orig:
            if not key.startswith("_"):
                self.assertIs(key in vars_get, True)
                self.assertEqual(vars_orig[key], vars_get[key])

    def test_ann_new_proposal_list_to_recipe(self):
        proposals = [{
            "text_cons": "My proposal 2",
            "nb": 1
        }, {
            "text_cons": "My proposal 3",
            "nb": 2
        }]
        r = self.add_new_recipe_minimalist()
        p_list = CProposal.add_new_list_to_recipe(proposals, r)
        for p in p_list:
            p_get = Proposal.objects.get(text_cons=p.text_cons)
            self.assertIs(p_get.id is None, False)
            vars_orig = vars(p)
            vars_get = vars(p_get)
            for key in vars_orig:
                if not key.startswith("_"):
                    self.assertIs(key in vars_get, True)
                    self.assertEqual(vars_orig[key], vars_get[key])

    def test_add_comment(self):
        r = self.add_new_recipe_minimalist()

        CComment.add_new(content="My comment 1", recipe=r, pseudo="Alyssia", mail="alyssia@gmail.com",
                         website="http://www.alyssia.fr")
        c_get = Comment.objects.get(content="My comment 1")
        self.assertEqual(c_get.id is None, False)
        self.assertEqual(c_get.recipe.id, r.id)
        self.assertEqual(c_get.pseudo, "Alyssia")
        self.assertEqual(c_get.mail, "alyssia@gmail.com")
        self.assertEqual(c_get.website, "http://www.alyssia.fr")
        self.assertIs(c_get.author, None)

        CComment.add_new(content="My comment 2", recipe=r, pseudo="Elaura", mail="elaura@gmail.com")
        c_get = Comment.objects.get(content="My comment 2")
        self.assertEqual(c_get.id is None, False)
        self.assertEqual(c_get.recipe.id, r.id)
        self.assertEqual(c_get.pseudo, "Elaura")
        self.assertEqual(c_get.mail, "elaura@gmail.com")
        self.assertIs(c_get.website, None)
        self.assertIs(c_get.author, None)
        author = User(first_name="Alyssia", last_name="Frênaie", email="alyssia.frenaie@gmail.com")
        author.save()

        CComment.add_new(content="My comment 3", recipe=r, author=author)
        c_get = Comment.objects.get(content="My comment 3")
        self.assertEqual(c_get.id is None, False)
        self.assertEqual(c_get.recipe.id, r.id)
        self.assertIs(c_get.pseudo, None)
        self.assertIs(c_get.mail, None)
        self.assertEqual(c_get.author.first_name, "Alyssia")
        self.assertEqual(c_get.author.last_name, "Frênaie")
        self.assertEqual(c_get.author.email, "alyssia.frenaie@gmail.com")

        try:
            CComment.add_new(content="My comment 4", recipe=r, pseudo="Martin")
            self.fail("This test is expected to fail")
        except RequiredParameterException as e:
            if str(e) != "if you do not give an author, mail is required":
                self.fail("RequiredParameterException: " + str(e))

        try:
            CComment.add_new(content="My comment 5", recipe=r, mail="martin@gmail.com")
            self.fail("This test is expected to fail")
        except RequiredParameterException as e:
            if str(e) != "if you do not give an author, pseudo is required":
                self.fail("RequiredParameterException: " + str(e))

        try:
            CComment.add_new(content="My comment 6", recipe=r, author=author, pseudo="Houbi")
            self.fail("This test is expected to fail")
        except RequiredParameterException as e:
            if str(e) != "if you give author, you cannot give pseudo, mail or website":
                self.fail("RequiredParameterException: " + str(e))

    def test_build_html_for_ig(self):
        ingr1 = {"name": "Carottes", "quantity": 2, "nb": 1, "unit": ""}
        ingr2 = {"nb": 2, "name": "Pommes de terre", "quantity": 400, "unit": "g de"}
        ingrs = [ingr2, ingr1]
        r = self.add_new_recipe_minimalist()
        ig = CIngredientGroup.add_new("Pour la pâte à tarte:", 1, r, 1, ingrs)
        html, has_ingr = CIngredientGroup.build_html_for_ig(ig)
        html_expected = "<li>Pour la pâte à tarte:</li><ul><li>2 Carottes</li><li>400 g de Pommes de terre</li>"
        self.assertEqual(html_expected, html)

    def test_build_recipe_ingredients(self):
        r = self.add_new_recipe_minimalist()
        # Group 1
        CIngredientGroup.add_new("group 1 :", 0, r, 1, [{"name": "carottes", "quantity": 2, "unit": "", "nb": 0}])
        # Group 2
        CIngredientGroup.add_new("Pour les oeufs :", 1, r, 2, [{"name": "chocolat", "quantity": 100, "unit":
                                 "g de", "nb": 0}, {"name": "sucre", "quantity": 25, "unit": "g de", "nb": 1}])
        # Group 3
        CIngredientGroup.add_new("", 2, r, 2, [{"name": "poires", "quantity": 3, "unit": "", "nb": 0}, {"name": "eau",
                                               "quantity": 5, "unit": "cl d'", "nb": 1}])
        # Group 4
        CIngredientGroup.add_new("", 3, r, 1, [{"name": "pommes", "quantity": 4, "unit": "kg de", "nb": 0}, {"name":
                                               "sel", "quantity": 5, "unit": "g de", "nb": 1}])
        html = CIngredientGroup.build_html_for_ingredients(r)
        html_expected = "<ul><li>group 1 :</li><ul><li>2 carottes</li><li>Pour les oeufs :</li><ul><li>100 g de " \
                        "chocolat</li><li>25 g de sucre</li></ul><li>3 poires</li><li>5 cl d'eau</li></ul><li>4 kg de" \
                        " pommes</li><li>5 g de sel</li></ul>"
        self.assertEqual(html_expected, html)

    def test_build_recipe_ingredients_2(self):
        r = self.add_new_recipe_minimalist()
        # Group 1
        CIngredientGroup.add_new("group 1 :", 0, r, 1, [{"name": "carottes", "quantity": 2, "unit": "", "nb": 0}])
        # Group 2
        CIngredientGroup.add_new("Pour les oeufs :", 1, r, 2, [{"name": "chocolat", "quantity": 100, "unit":
            "g de", "nb": 0}, {"name": "sucre", "quantity": 25, "unit": "g de", "nb": 1}])
        # Group 3
        CIngredientGroup.add_new("", 2, r, 2, [{"name": "poires", "quantity": 3, "unit": "", "nb": 0}, {"name": "eau",
                                                                                                        "quantity": 5,
                                                                                                        "unit": "cl d'",
                                                                                                        "nb": 1}])
        # Group 4
        CIngredientGroup.add_new("Un commentaire pour finir", 3, r, 0)
        html = CIngredientGroup.build_html_for_ingredients(r)
        html_expected = "<ul><li>group 1 :</li><ul><li>2 carottes</li><li>Pour les oeufs :</li><ul><li>100 g de " \
                        "chocolat</li><li>25 g de sucre</li></ul><li>3 poires</li><li>5 cl d'eau</li></ul></ul>Un " \
                        "commentaire pour finir"
        self.assertEqual(html_expected, html)

    def test_build_recipe_instructions(self):
        r = self.add_new_recipe_minimalist()
        CInstruction.add_new("instr 1", 0, r, 1)
        CInstruction.add_new("instr 3", 2, r, 2)
        CInstruction.add_new("instr 4 :", 3, r, 2)
        CInstruction.add_new("instr 9", 8, r, 1)
        CInstruction.add_new("instr 5", 4, r, 3)
        CInstruction.add_new("instr 6", 5, r, 3)
        CInstruction.add_new("instr 7", 6, r, 2)
        CInstruction.add_new("instr 8", 7, r, 1)
        CInstruction.add_new("instr 2 :", 1, r, 1)

        html = CInstruction.build_html_for_instructions(r)
        html_expected = "<ol><li>instr 1</li><li>instr 2 :</li><ol><li>instr 3</li><li>instr 4 :</li><ol><li>instr 5" \
                        "</li><li>instr 6</li></ol><li>instr 7</li></ol><li>instr 8</li><li>instr 9</li></ol>"
        self.assertEqual(html_expected, html)

    def test_build_recipe_proposals(self):
        r = self.add_new_recipe_minimalist()
        CProposal.add_new_to_recipe("cons 1", 0, r)
        CProposal.add_new_to_recipe("cons 3", 2, r)
        CProposal.add_new_to_recipe("cons 2", 1, r)

        html = CProposal.build_html_for_proposals(r)
        html_expected = "<ul><li>cons 1</li><li>cons 2</li><li>cons 3</li></ul>"
        self.assertEqual(html_expected, html)

    def test_build_recipe_equipments(self):
        r = self.add_new_recipe_minimalist()
        CEquipment.add_new_to_recipe("equipment 3", 3, 2, r)
        CEquipment.add_new_to_recipe("equipment 1", 1, 0, r)
        CEquipment.add_new_to_recipe("equipment 2", 2, 1, r)

        html = CEquipment.build_html_for_equipments(r)
        html_expected = "<ul><li>1 equipment 1</li><li>2 equipment 2</li><li>3 equipment 3</li></ul>"
        self.assertEqual(html_expected, html)

    def add_new_recipe_full(self):
        title = "Title of the recipe"
        description = "My description"
        tps_prep = 20
        tps_rep = 140
        tps_cuis = 65
        picture_file = "myFile.jpg"
        nb_people = 4
        nb_people_max = None
        pub_date = datetime.now()
        author = User(first_name="Floréal", last_name="Cabanettes", email="test@gmail.com")
        author.save()
        cat = Category(name="Category1", url="category1")
        cat.save()
        categories = [cat]
        precision = "ne vous loupez pas"
        r = CRecipe.add_new(title=title, description=description, tps_prep=tps_prep, picture_file=picture_file,
                            nb_people=nb_people, author=author, categories=categories, pub_date=pub_date,
                            tps_rep=tps_rep, tps_cuis=tps_cuis, nb_people_max=nb_people_max, precision=precision)
        # Group 1
        CIngredientGroup.add_new("group 1 :", 0, r, 1, [{"name": "carottes", "quantity": 2, "unit": "", "nb": 0}])
        # Group 2
        CIngredientGroup.add_new("Pour les oeufs :", 1, r, 2, [{"name": "chocolat", "quantity": 100, "unit":
                                 "g de", "nb": 0}, {"name": "sucre", "quantity": 25, "unit": "g de", "nb": 1}])
        # Group 3
        CIngredientGroup.add_new("", 2, r, 2, [{"name": "poires", "quantity": 3, "unit": "", "nb": 0}, {"name": "eau",
                                 "quantity": 5, "unit": "cl d'", "nb": 1}])
        # Group 4
        CIngredientGroup.add_new("", 3, r, 1, [{"name": "pommes", "quantity": 4, "unit": "kg de", "nb": 0}, {"name":
                                 "sel", "quantity": 5, "unit": "g de", "nb": 1}])
        CEquipment.add_new_to_recipe("equipment 3", 3, 2, r)
        CEquipment.add_new_to_recipe("equipment 1", 1, 0, r)
        CEquipment.add_new_to_recipe("equipment 2", 2, 1, r)
        CInstruction.add_new("instr 1", 0, r, 1)
        CInstruction.add_new("instr 3", 2, r, 2)
        CInstruction.add_new("instr 4 :", 3, r, 2)
        CInstruction.add_new("instr 9", 8, r, 1)
        CInstruction.add_new("instr 5", 4, r, 3)
        CInstruction.add_new("instr 6", 5, r, 3)
        CInstruction.add_new("instr 7", 6, r, 2)
        CInstruction.add_new("instr 8", 7, r, 1)
        CInstruction.add_new("instr 2 :", 1, r, 1)
        CProposal.add_new_to_recipe("cons 1", 0, r)
        CProposal.add_new_to_recipe("cons 3", 2, r)
        CProposal.add_new_to_recipe("cons 2", 1, r)
        return r

    def test_full_recipe(self):
        r = self.add_new_recipe_full()
        html = CRecipe.get_recipe_html(r)
        html_expected = "<div id='masquer'><div><a href='/Photos/myFile.jpg'><img class='shadow' style='float: left; " \
                        "margin-right: 6px;' title='Title of the recipe' src='/Photos/myFile.jpg' alt='illustration' " \
                        "width='254px' /></a></div>My description</div>"
        html_expected += "<div id='timesDetail'><strong>Temps de préparation&#8239;: 20 min<br/>Temps de repos&#8239;" \
                         ": 2 h 20 min<br/>Temps de cuisson&#8239;: 1 h 5 min</strong></div>"
        html_expected += "<div id='ingredientsAndEquipments'><div id='ingredients'><p id='ingredientsHeader'><strong>" \
                         "Ingrédients (pour 4 personnes (ne vous loupez pas))&#8239;:</strong></p>"
        html_expected += "<ul><li>group 1 :</li><ul><li>2 carottes</li><li>Pour les oeufs :</li><ul><li>100 g de " \
                         "chocolat</li><li>25 g de sucre</li></ul><li>3 poires</li><li>5 cl d'eau</li></ul><li>4 kg " \
                         "de pommes</li><li>5 g de sel</li></ul>"
        html_expected += "</div><div class='equipment'><p id='equipmentHeader'><strong>Matériel nécessaire&#8239;:" \
                         "</strong></p><ul><li>1 equipment 1</li><li>2 equipment 2</li><li>3 equipment 3</li></ul>" \
                         "</div></div>"
        html_expected += "<div id='instructions'><p id='instructionsHeader'><strong>Préparation&#8239;:</strong></p>" \
                         "<ol><li>instr 1</li><li>instr 2 :</li><ol><li>instr 3</li><li>instr 4 :</li><ol><li>instr 5" \
                         "</li><li>instr 6</li></ol><li>instr 7</li></ol><li>instr 8</li><li>instr 9</li></ol></div>"
        html_expected += "<div id='proposals'><p id='proposalsHeader'><strong>Conseils&#8239;:</strong></p><ul><li>" \
                         "cons 1</li><li>cons 2</li><li>cons 3</li></ul></div>"
        self.assertEqual(html_expected, html)
