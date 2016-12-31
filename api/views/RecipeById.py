from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from django.core.exceptions import ObjectDoesNotExist
from api.exceptions import RecipeNotFound

from main.controllers import CRecipe


class RecipeById(APIView):
    """
    Get a specific recipe
    """
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, id_recipe):
        try:
            return Response(CRecipe.get_recipe_data_from_id(int(id_recipe), request.user, True))
        except ObjectDoesNotExist:
            raise RecipeNotFound
