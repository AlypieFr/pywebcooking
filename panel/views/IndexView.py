from django.views.generic import TemplateView
from pywebcooking.settings import MEDIA_ROOT


class IndexView(TemplateView):
    template_name = "panel/index.html"

    media_root = MEDIA_ROOT