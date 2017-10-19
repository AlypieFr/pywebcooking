from django.views.generic import View
from django.shortcuts import render, redirect
from pywebcooking import settings
from django.utils.translation import ugettext as _
from pywebcooking.settings import MEDIA_ROOT
from main.models import Recipe, Comment
from django.contrib.auth.models import User


class IndexView(View):

    def get(self, request):
        print(request)
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        nb_recipes = Recipe.objects.all().count()
        nb_recipes_user = Recipe.objects.filter(author__user=self.request.user).count()
        nb_comments = Comment.objects.filter(published=True).count()
        nb_users = User.objects.all().count()
        context = {
            "title": _("User panel") + " - " + settings.SITE_NAME,
            "nb_recipes": nb_recipes,
            "nb_recipes_user": nb_recipes_user,
            "nb_comments": nb_comments,
            "nb_pages": 0,  # TODO: update this when page will be implemented
            "nb_users": nb_users if request.user.is_staff else 0
        }
        return render(request, 'panel/index.html', context)
