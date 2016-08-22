from main.models import Category
from website.config import MainConfig


class GenericView:

    @staticmethod
    def categories():
        cats = []
        cats_get = Category.objects.order_by('order')
        for cat in cats_get:
            cats.append({"name": cat.name, "url": cat.url})
        return cats

    config = {
        "title": MainConfig.title_website
    }
