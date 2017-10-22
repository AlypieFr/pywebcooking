from django.conf.urls import url
from django.utils.translation import ugettext as _
from django.utils.translation import pgettext
from django.views.generic.base import RedirectView

from .views import IndexView, RecipesView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^recipes/$', RecipesView.as_view(), name='recipes'),
]
