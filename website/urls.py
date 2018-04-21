from django.conf.urls import url
from django.utils.translation import ugettext as _
from django.utils.translation import pgettext
from django.views.generic.base import RedirectView

from .views.IndexView import IndexView
from .views.RecipeView import RecipeView
from .views.LoginView import LoginView
from .views.LogoutView import LogoutView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='website_index'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^' + _("page") + '/(?P<page>\d+)$', IndexView.as_view(), name='website_index_page'),
    url(r'^' + pgettext("category url", "category") + "/(?P<cat>[\w-]+)$", IndexView.as_view(), name='website_category'),
    url(r'^' + pgettext("category url", "category") + "/(?P<cat>[\w-]+)/" + _("page") + '/(?P<page>\d+)$',
        IndexView.as_view(), name='website_category_page'),
    url(r'^' + pgettext("author url", "author") + "/(?P<author>[\w-]+)$", IndexView.as_view(), name='website_author'),
    url(r'^' + pgettext("author url", "author") + "/(?P<author>[\w-]+)/" + _("page") + '/(?P<page>\d+)$',
        IndexView.as_view(), name='website_author_page'),
    # Translators: recipe is the parent tag of a recipe
    url(r'^' + _("recipe") + '/(?P<slug>\w+)$', RecipeView.as_view(), name='website_recipe'),
    url(r'^favicon\.ico$', favicon_view),
]
