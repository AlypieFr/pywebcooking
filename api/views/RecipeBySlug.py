from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from django.core.exceptions import ObjectDoesNotExist
from api.exceptions import RecipeNotFound

from main.controllers import CRecipe


class RecipeBySlug(APIView):
    """
    Get a specific recipe
    """
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, slug):
        try:
            return Response(CRecipe.get_recipe_data_from_slug(slug, request.user, True))
        except ObjectDoesNotExist:
            raise RecipeNotFound
