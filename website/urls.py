from django.conf.urls import url
from django.utils.translation import ugettext as _
from django.utils.translation import pgettext
from django.views.generic.base import RedirectView

from .views import IndexView, RecipeView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^' + _("page") + '/(?P<page>\d+)$', IndexView.as_view(), name='index_page'),
    url(r'^' + pgettext("category url", "category") + "/(?P<cat>[\w-]+)$", IndexView.as_view(), name='category'),
    url(r'^' + pgettext("category url", "category") + "/(?P<cat>[\w-]+)/" + _("page") + '/(?P<page>\d+)$',
        IndexView.as_view(), name='category_page'),
    url(r'^' + pgettext("author url", "author") + "/(?P<author>[\w-]+)$", IndexView.as_view(), name='author'),
    url(r'^' + pgettext("author url", "author") + "/(?P<author>[\w-]+)/" + _("page") + '/(?P<page>\d+)$',
        IndexView.as_view(), name='author_page'),
    # Translators: recipe is the parent tag of a recipe
    url(r'^' + _("recipe") + '/(?P<slug>\w+)$', RecipeView.as_view(), name='recipe'),
    url(r'^favicon\.ico$', favicon_view),
]
