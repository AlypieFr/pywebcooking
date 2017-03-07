from .GenericView import GenericView
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from pywebcooking.settings import MEDIA_ROOT

from main.models import Recipe


class IndexView(TemplateView):
    categories = GenericView.categories()
    config = GenericView.config

    template_name = "website/index.html"

    def data(self):
        dat = {}
        page = 1
        if "nb" in self.kwargs:
            page = self.kwargs["nb"]
        recipes = Recipe.objects.all().order_by("-pub_date")
        paginator = Paginator(recipes, 5)
        try:
            page_recipe = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            page_recipe = paginator.page(1)
        dat["recipes"] = page_recipe
        dat["page"] = page
        dat["media_root"] = MEDIA_ROOT #+ recipe.author.user.username
        return dat
