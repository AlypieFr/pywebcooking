from django.views.generic import View
from django.shortcuts import render, redirect
from pywebcooking import settings
from django.utils.translation import ugettext as _
from pywebcooking.settings import MEDIA_ROOT
from main.models import Recipe, Comment
from django.contrib.auth.models import User
from django_gravatar.helpers import get_gravatar_url


class IndexView(View):

    def get(self, request):
        print(request)
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        recipes = Recipe.objects.all()
        nb_recipes = recipes.count()
        recipes_user = Recipe.objects.filter(author__user=self.request.user)
        last_recipes = recipes_user.order_by("pub_date").reverse()[:5]
        nb_recipes_user = recipes_user.count()
        comments = Comment.objects.filter(published=True)
        latest_comments = comments.filter(recipe__in=recipes_user).order_by("pub_date").reverse()[:5]
        last_comments = []
        for comment in latest_comments:
            last_comments.append({
                "pseudo": comment.pseudo if comment.pseudo is not None else comment.author.user.username,
                "comment": comment.content,
                "pub_date": comment.pub_date,
                "recipe": comment.recipe
            })
        nb_comments = comments.count()
        nb_users = User.objects.all().count()
        context = {
            "title": _("User panel") + " - " + settings.SITE_NAME,
            "nb_recipes": nb_recipes,
            "nb_recipes_user": nb_recipes_user,
            "nb_comments": nb_comments,
            "nb_pages": 0,  # TODO: update this when page will be implemented
            "nb_users": nb_users if request.user.is_staff else 0,
            "last_recipes": last_recipes,
            "last_comments": last_comments,
            "staff": request.user.is_staff,
            "user_name": request.user.first_name + " " + request.user.last_name,
            "user": request.user,
            "avatar": get_gravatar_url(request.user.email, size=160)
        }
        return render(request, 'panel/index.html', context)
