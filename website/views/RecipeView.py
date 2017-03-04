from .GenericView import GenericView
from django.views.generic import TemplateView
from django.http import Http404
from django.utils.translation import pgettext
from django.shortcuts import redirect
from django.contrib.auth.models import User

from website.forms import CommentForm, CommentFormAuthenticated

from main.controllers import CRecipe, CComment
from main.models import UserProfile

import urllib.parse


class RecipeView(TemplateView):
    categories = GenericView.categories()
    config = GenericView.config

    template_name = "website/recipe.html"

    def post(self, request, *args, **kwargs):
        recipe = CRecipe.get_recipe_from_slug(kwargs["slug"])
        is_auth = False
        if self.request.user.is_authenticated():
            is_auth = True
            form = CommentFormAuthenticated(data=request.POST)
        else:
            form = CommentForm(data=request.POST)
        base_url = request.META['HTTP_REFERER'].split("?")[0].split("#")[0]
        if form.is_valid():
            if is_auth:
                user = UserProfile.objects.get(user__username=self.request.user)
                comment = CComment.add_new(content=form.data.get("text"), recipe=recipe, author=user)
            else:
                comment = CComment.add_new(content=form.data.get("text"), recipe=recipe, pseudo=form.data.get("name"),
                                 mail=form.data.get("email"), website=form.data.get("website"))
            return redirect(base_url + "?success#comm" + str(comment.id))
        else:
            if form.has_error("captcha"):
                return redirect(base_url + "?captcha-error&" + urllib.parse.urlencode(form.data) + "#post-comment")
            return redirect(base_url + "?error#post-comment", args=form.data)

    def recipe(self):
        data = {"authenticated": False}
        if self.request.user.is_authenticated():
            if "text" in self.request.GET.keys():
                data["comment_form"] = CommentFormAuthenticated(data=self.request.GET)
            else:
                data["comment_form"] = CommentFormAuthenticated()
            data["authenticated"] = True
            data["username"] = User.objects.get(username=self.request.user).first_name
        else:
            if "text" in self.request.GET.keys():
                data["comment_form"] = CommentForm(data=self.request.GET)
            else:
                data["comment_form"] = CommentForm()
        data["error"] = "error" in self.request.GET or "captcha-error" in self.request.GET
        data["captcha_error"] = "captcha-error" in self.request.GET
        recipe = CRecipe.get_recipe_from_slug(self.kwargs["slug"])
        if recipe is None:
            raise Http404("This recipe does not exists")
        data["html"] = CRecipe.get_recipe_html(recipe)
        data["recipe"] = recipe
        data["date_published"] = recipe.pub_date.date()
        data["categories"] = []
        for cat in recipe.category.all().order_by("order"):
            # Translators: category url
            data["categories"].append("<a href='/" + pgettext("category url", "category") + "/" + cat.url + "'>" + cat.name + "</a>")
        data["categories"] = " - ".join(data["categories"])
        data["comments"] = CComment.get_recipe_comments(recipe)
        return data
