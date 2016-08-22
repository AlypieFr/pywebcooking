from django.contrib import admin

# Register your models here.

from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    ordering = ("order",)


class RecipeAdmin(admin.ModelAdmin):
    fields = ["title", "author", "category", "published", "enable_comments"]

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
