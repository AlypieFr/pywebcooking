from django.conf.urls import url
from django.utils.translation import ugettext as _
from django.utils.translation import pgettext
from django.views.generic.base import RedirectView

from .views.IndexView import IndexView
from .views.RecipesView import RecipesView
from .views.RecipesChangeView import RecipesChangeView
from .views.RecipeView import RecipeView
from .views.RecipeEditView import RecipeEditView


favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='panel_index'),

    #####################
    # Recipes view URLs #
    #####################

    # Main recipes URL:
    url(r'^' + _("recipes") + '/$', RecipesView.as_view(), name='panel_recipes'),
    url(r'^' + _("recipes") + '/' + _("page") + '/(?P<page>\d+)$', RecipesView.as_view(), name='panel_recipes_page'),

    # Trash:
    url(r'^' + _("recipes") + '/' + _("trash") + '/$', RecipesView.as_view(), name='panel_recipes_trash',
        kwargs={"trash": True}),
    url(r'^' + _("recipes") + '/' + _("trash") + '/' + _("page") + '/(?P<page>\d+)$', RecipesView.as_view(),
        name='panel_recipes_trash_page', kwargs={"trash": True}),

    # Mine:
    url(r'^' + _("recipes") + '/' + pgettext("url", "mine") + '/$', RecipesView.as_view(), name='panel_recipes_mine',
        kwargs={"mine": True}),
    url(r'^' + _("recipes") + '/' + pgettext("url", "mine") + '/' + _("page") + '/(?P<page>\d+)$', RecipesView.as_view(),
        name='panel_recipes_mine_page', kwargs={"mine": True}),

    # Published
    url(r'^' + _("recipes") + '/' + pgettext("url", "published") + '/$', RecipesView.as_view(),
        name='panel_recipes_published', kwargs={"published": True}),
    url(r'^' + _("recipes") + '/' + pgettext("url", "published") + '/' + _("page") + '/(?P<page>\d+)$', RecipesView.as_view(),
        name='panel_recipes_published_page', kwargs={"published": True}),

    # Change:
    url(r'^' + _("recipes") + '/change/', RecipesChangeView.as_view(), name='panel_recipes_change'),

    ########################
    # One Recipe view URLs #
    ########################

    # Main recipe URL:
    url(r'^' + _("recipe") + "/(?P<slug>\w+)$", RecipeView.as_view(), name='panel_recipe'),

    # Submit form:
    url(r'^' + _("recipe") + "/(?P<slug>\w+)/submit/$", RecipeEditView.as_view(), name='panel_recipe_edit'),
]
