from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction

from website.tests import TModels

from website.controllers import CIngredientGroup, CInstruction, CProposal, CEquipment


class TDuplicates(TestCase):
    def test_duplicate_exceptions(self):
        m = TModels()
        r = m.add_new_recipe_minimalist()

        # Test 1: for IngredientGroup in Recipe:
        with transaction.atomic():
            CIngredientGroup.add_new("group 1 :", 0, r, 1, [{"name": "carottes", "quantity": 2, "unit": "", "nb": 0}])
        try:
            with transaction.atomic():
                CIngredientGroup.add_new("group 2 :", 0, r, 2, [{"name": "salades", "quantity": 2, "unit": "", "nb": 0}])
            self.fail("This test is expected to fail")
        except IntegrityError as e:
            if "Duplicate entry" not in str(e):
                self.fail("django.db.utils.IntegrityError: " + str(e))

        # Test 2: for Ingredient in IngredientInGroup:
        try:
            with transaction.atomic():
                CIngredientGroup.add_new("group 1 :", 1, r, 1, [{"name": "carottes", "quantity": 2, "unit": "", "nb": 0},
                                                                {"name": "sel", "quantity": 3, "unit": "g", "nb": 1}])
        except IntegrityError as e:
            if "Duplicate entry" not in str(e):
                self.fail("django.db.utils.IntegrityError: " + str(e))

        # Test 3: for Instruction in Recipe:
        with transaction.atomic():
            CInstruction.add_new("inst 1", 0, r, 0)
        try:
            with transaction.atomic():
                CInstruction.add_new("inst 2", 0, r, 1)
            self.fail("This test is expected to fail")
        except IntegrityError as e:
            if "Duplicate entry" not in str(e):
                self.fail("django.db.utils.IntegrityError: " + str(e))

        # Test 4: for Proposal in Recipe:
        with transaction.atomic():
            CProposal.add_new_to_recipe("cons 1", 0, r)
        try:
            with transaction.atomic():
                CProposal.add_new_to_recipe("cons 2", 0, r)
            self.fail("This test is expected to fail")
        except IntegrityError as e:
            if "Duplicate entry" not in str(e):
                self.fail("django.db.utils.IntegrityError: " + str(e))

        # Test 5: for Equipment in Recipe:
        with transaction.atomic():
            CEquipment.add_new_to_recipe("eq 1", 1, 0, r)
        try:
            with transaction.atomic():
                CEquipment.add_new_to_recipe("eq 2", 2, 0, r)
            self.fail("This test is expected to fail")
        except IntegrityError as e:
            if "Duplicate entry" not in str(e):
                self.fail("django.db.utils.IntegrityError: " + str(e))
