from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from main.models import Category


class Categories(APIView):
    """
    Get available categories
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        cats = []
        for cat in Category.objects.all():
            cat_dict = {
                "name": cat.name,
                "url": cat.url
            }
            cats.append(cat_dict)
        return Response(cats)
