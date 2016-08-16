from django.conf.urls import url
from website.config import UrlConfig

from .views import IndexView, RecipeView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^' + UrlConfig.recipe + '/(?P<slug>\w+)$', RecipeView.as_view(), name='recipe'),
]
