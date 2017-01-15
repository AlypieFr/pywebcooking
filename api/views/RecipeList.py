from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from api.functions import Functions

from api.serializers import RecipeSerializer

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
        # serializer = RecipeSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = Functions.get_data_dict(request.POST.dict())
        user_profile = UserProfile.objects.get(user__username=request.user.username)
        r_id, error = Functions.add_recipe(data, request.FILES, user_profile.url)
        if r_id < 0:
            if r_id == -1:
                return Response(error)
            else:
                return Response("Unexpected error: " + error)
        else:
            return Response("ok " + str(r_id))
