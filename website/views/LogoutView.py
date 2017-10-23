from django.views.generic import View
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.middleware import csrf


class LogoutView(View):

    def get(self, request):
        logout(request)
        csrf.rotate_token(request)
        if request.META["HTTP_REFERER"].find("/panel/") > -1 or request.META["HTTP_REFERER"].find("/admin/") > -1 or \
                request.META["HTTP_REFERER"].find("/api/") > -1:
            return redirect("/")
        return redirect(request.META["HTTP_REFERER"])
