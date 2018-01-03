from main.models.Category import Category


class GenericView:

    @staticmethod
    def categories():
        cats = []
        cats_get = Category.objects.order_by('order')
        for cat in cats_get:
            cats.append({"name": cat.name, "url": cat.url})
        return cats
