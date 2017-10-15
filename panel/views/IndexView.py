from django.views.generic import View
from django.shortcuts import render, redirect
from pywebcooking import settings
from pywebcooking.settings import MEDIA_ROOT


class IndexView(View):

    def get(self, request):
        print(request)
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return render(request, 'panel/index.html', {})
