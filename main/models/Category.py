from django.db import models
from django.utils.translation import ugettext as _


class Category(models.Model):
    # Translators: categories fields
    name = models.CharField(max_length=100, verbose_name=_("name"))
    url = models.CharField(max_length=100, verbose_name=_("url"))
    order = models.IntegerField(unique=True, verbose_name=_("order"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
