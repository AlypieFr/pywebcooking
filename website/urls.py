from django.conf.urls import url

from .views import IndexView, RecipeView

from django.utils.translation import ugettext as _

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    # Translators: recipe is the parent tag of a recipe
    url(r'^' + _("recipe") + '/(?P<slug>\w+)$', RecipeView.as_view(), name='recipe'),
]
