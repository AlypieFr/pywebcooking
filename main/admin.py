from django.contrib import admin

# Register your models here.

from .models.Category import Category
from .models.Recipe import Recipe
from .models.UserProfile import UserProfile


class CategoryAdmin(admin.ModelAdmin):
    ordering = ("order",)


class RecipeAdmin(admin.ModelAdmin):
    fields = ["title", "author", "category", "published", "enable_comments"]

    def has_add_permission(self, request, obj=None):
        return False


class UserProfileAdmin(admin.ModelAdmin):
    fields = ["user", "url"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
