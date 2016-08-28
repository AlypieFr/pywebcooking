from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from django.conf.urls import include

urlpatterns = [
    url(r'^$', views.RecipeList.as_view()),
    url(r'^auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
