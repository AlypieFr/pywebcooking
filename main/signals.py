import os
import glob

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings

from main.models import Recipe, MediaInRecipe


@receiver(pre_delete, sender=Recipe)
def delete_recipe(**kwargs):
    recipe = kwargs["instance"]
    medias = MediaInRecipe.objects.filter(recipe=recipe)
    for media in medias:
        if MediaInRecipe.objects.filter(media=media).count() == 0:
            pict_file = settings.BASE_DIR + settings.MEDIA_URL + recipe.author.url + "/" + media.media
            if os.path.isfile(pict_file):
                os.remove(pict_file)
            if media.type == "main":
                thumb_files = os.path.splitext(settings.BASE_DIR + settings.MEDIA_URL + recipe.author.url +
                                               "/" + media.media)[0] + "_thumb_*"
                for thumb_file in glob.glob(thumb_files):
                    os.remove(thumb_file)
