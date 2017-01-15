import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.translation import ugettext as _

from api.functions import Functions

from main.controllers import CRecipe
from main.models import UserProfile


class RecipeList(APIView):
    """
    List all recipes of the user, or create a new one
    """
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        return Response(CRecipe.get_author_recipes_data(request.user))

    def post(self, request):
        data = Functions.get_data_dict(request.POST.dict())
        user_profile = UserProfile.objects.get(user__username=request.user.username)
        r_id, message = Functions.add_recipe(data, request.FILES, user_profile.url)
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
                response["message"] = "Unexpected error: " + message
        else:
            response["url"] = request.META['HTTP_HOST'] + "/" + _("recipe") + "/" + message
        return Response(response)
