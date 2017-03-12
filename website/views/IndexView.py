from .GenericView import GenericView
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext as _

from pywebcooking.settings import MEDIA_ROOT, POSTS_PER_PAGE

from main.models import Recipe, Category, UserProfile


class IndexView(TemplateView):
    categories = GenericView.categories()
    config = GenericView.config

    template_name = "website/index.html"

    def data(self):
        dat = {"in_archive": False, "page_view_name": "index_page", "additional_kwargs": {}}
        page = 1
        if "page" in self.kwargs:
            page = self.kwargs["page"]
        if "cat" in self.kwargs:
            dat["in_archive"] = True
            dat["page_view_name"] = "category_page"
            dat["archive_header"] = Category.objects.get(url=self.kwargs["cat"]).name
            dat["additional_kwargs"] = {"cat": self.kwargs["cat"]}
            recipes = Recipe.objects.filter(category__url=self.kwargs["cat"]).order_by("-pub_date")
        elif "author" in self.kwargs:
            dat["in_archive"] = True
            dat["page_view_name"] = "author_page"
            dat["archive_header"] = _("Author:") + " " + \
                UserProfile.objects.get(url=self.kwargs["author"]).user.first_name
            dat["additional_kwargs"] = {"author": self.kwargs["author"]}
            recipes = Recipe.objects.filter(author__url=self.kwargs["author"])
        else:
            recipes = Recipe.objects.all().order_by("-pub_date")

        paginator = Paginator(recipes, POSTS_PER_PAGE)
        try:
            page_recipe = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            page_recipe = paginator.page(1)
        dat["recipes"] = page_recipe
        dat["page"] = page
        dat["media_root"] = MEDIA_ROOT #+ recipe.author.user.username

        dat["times"] = {}
        for recipe in page_recipe:
            dat["times"][recipe.id] = {}
            # Preparation time:
            if recipe.tps_prep is not None and recipe.tps_prep != 0:
                tps_prep_h = int(recipe.tps_prep / 60)
                tps_prep_min = recipe.tps_prep % 60
                tps_prep = []
                if tps_prep_h > 0:
                    tps_prep.append(str(tps_prep_h) + " h")
                if tps_prep_min > 0:
                    tps_prep.append(str(tps_prep_min) + " min")
                recipe.tps_prep = " ".join(tps_prep)

            # Break time:
            if recipe.tps_rep is not None and recipe.tps_rep > 0:
                tps_rep_j = int(recipe.tps_rep / 1440)
                tps_rep_h = int((recipe.tps_rep % 1440) / 60)
                tps_rep_min = recipe.tps_rep % 60
                tps_rep = []
                if tps_rep_j > 0:
                    tps_rep.append(str(tps_rep_j) + " j")
                if tps_rep_h > 0:
                    tps_rep.append(str(tps_rep_h) + " h")
                if tps_rep_min > 0:
                    tps_rep.append(str(tps_rep_min) + " min")
                recipe.tps_rep = " ".join(tps_rep)

            # Cook time:
            if recipe.tps_cuis is not None and recipe.tps_cuis > 0:
                tps_cuis_h = int(recipe.tps_cuis / 60)
                tps_cuis_min = recipe.tps_cuis % 60
                tps_cuis = []
                if tps_cuis_h > 0:
                    tps_cuis.append(str(tps_cuis_h) + " h")
                if tps_cuis_min > 0:
                    tps_cuis.append(str(tps_cuis_min) + " min")
                recipe.tps_cuis = " ".join(tps_cuis)

            cats = []
            print(recipe.category.all().order_by("order"))
            for cat in recipe.category.all().order_by("order"):
                cats.append(cat.name)
            recipe.cats = ", ".join(cats)

        return dat
