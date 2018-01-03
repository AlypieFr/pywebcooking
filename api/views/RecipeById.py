from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from django.core.exceptions import ObjectDoesNotExist
from api.exceptions import RecipeNotFound

from api.functions import Functions

from main.controllers.C_Recipe import CRecipe
from main.models.Recipe import Recipe
from main.models.UserProfile import UserProfile

from django.utils.translation import ugettext as _


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

    def put(self, request, id_recipe):
        data = Functions.get_data_dict(request.POST.dict())
        try:
            recipe = Recipe.objects.get(id=id_recipe)
        except ObjectDoesNotExist:
            raise RecipeNotFound
        user_profile = UserProfile.objects.get(user__username=request.user.username)
        r_id, message = Functions.update_recipe(recipe, data, request.FILES, user_profile.url)
        response = {
            "status": "0",
            "message": "",
            "url": "",
            "id": str(r_id)
        }
        if r_id < 0:
            response["status"] = str(-r_id)
            response["message"] = message
            if r_id != -1:
                response["message"] = _("Unexpected error: ") + message
        else:
            response["url"] = request.META['HTTP_HOST'] + "/" + _("recipe") + "/" + message
        return Response(response)

