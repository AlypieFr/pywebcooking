from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from api.serializers import RecipeSerializer

from main.controllers import CRecipe


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
        print(request.FILES)
        return Response("ok")
