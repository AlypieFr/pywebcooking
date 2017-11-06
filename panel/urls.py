from django.conf.urls import url
from django.utils.translation import ugettext as _
from django.utils.translation import pgettext
from django.views.generic.base import RedirectView

from .views import IndexView, RecipesView, RecipesChangeView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),

    #####################
    # Recipes view URLs #
    #####################

    # Main recipes URL:
    url(r'^recipes/$', RecipesView.as_view(), name='recipes'),
    url(r'^recipes/' + _("page") + '/(?P<page>\d+)$', RecipesView.as_view(), name='recipes_page'),

    # Trash:
    url(r'^recipes/' + _("trash") + '/$', RecipesView.as_view(), name='recipes_trash', kwargs={"trash": True}),
    url(r'^recipes/' + _("trash") + '/' + _("page") + '/(?P<page>\d+)$', RecipesView.as_view(),
        name='recipes_trash_page', kwargs={"trash": True}),

    # Mine:
    url(r'^recipes/' + pgettext("url", "mine") + '/$', RecipesView.as_view(), name='recipes_mine',
        kwargs={"mine": True}),
    url(r'^recipes/' + pgettext("url", "mine") + '/' + _("page") + '/(?P<page>\d+)$', RecipesView.as_view(),
        name='recipes_mine_page', kwargs={"mine": True}),

    # Published
    url(r'^recipes/' + pgettext("url", "published") + '/$', RecipesView.as_view(), name='recipes_published',
        kwargs={"published": True}),
    url(r'^recipes/' + pgettext("url", "published") + '/' + _("page") + '/(?P<page>\d+)$', RecipesView.as_view(),
        name='recipes_published_page', kwargs={"published": True}),

    # Change:
    url(r'^recipes/change/', RecipesChangeView.as_view(), name='recipes_change')
]
