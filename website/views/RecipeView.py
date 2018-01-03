from .GenericView import GenericView
from django.views.generic import TemplateView
from django.http import Http404
from django.utils.translation import pgettext
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django_gravatar.helpers import get_gravatar_url

from website.forms import CommentForm, CommentFormAuthenticated

from main.controllers.C_Recipe import CRecipe
from main.controllers.C_Comment import CComment

from main.models.UserProfile import UserProfile

from pywebcooking.settings import SITE_NAME


class RecipeView(TemplateView):
    template_name = "website/recipe.html"
    site_name = SITE_NAME

    user = None

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        c = super(RecipeView, self).get_context_data(**kwargs)
        self.user = self.request.user
        return c

    def data(self):
        categories = GenericView.categories()
        config = GenericView.config
        dat = {"categories": categories, "config": config, "user": self.user if self.user.is_authenticated else None}
        if self.user.is_authenticated:
            dat["avatar"] = get_gravatar_url(self.user.email, size=160)
            dat["user_name"] = self.user.first_name
        return dat

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
            data["username"] = self.user.first_name
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
