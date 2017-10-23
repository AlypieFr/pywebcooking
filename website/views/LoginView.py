from django.views.generic import FormView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from pywebcooking.settings import SITE_NAME
from website.forms import LoginForm


class LoginView(FormView):

    def get(self, request, **kwargs):
        return render(request, 'website/login.html', {"site_name": SITE_NAME,
                                                      "next": request.GET['next'] if "next" in request.GET else "/"})

    def post(self, request, **kwargs):
        form = LoginForm(request.POST or None)
        if request.POST and form.is_valid():
            user = form.login()
            if user is not None:
                login(request, user)
                return redirect(request.POST["next"] if request.POST["next"] != "" else "/")
        else:
            return render(request, 'website/login.html', {'form': form, "site_name": SITE_NAME,
                                                          "next": request.POST['next']
                                                          if "next" in request.POST else "/"})
