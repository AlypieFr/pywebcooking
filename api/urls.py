from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include

from .views.RecipeList import RecipeList
from .views.RecipeById import RecipeById
from .views.RecipeBySlug import RecipeBySlug
from .views.Categories import Categories

urlpatterns = [
    url(r'^$', RecipeList.as_view()),
    url(r'^recipe/by-id/([0-9]+)$', RecipeById.as_view()),
    url(r'^recipe/by-slug/([\w_]+)$', RecipeBySlug.as_view()),
    url(r'^categories/', Categories.as_view()),
    url(r'^auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
