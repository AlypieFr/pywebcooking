from django.views.generic import View
from django.http import JsonResponse, Http404
from main.models import Recipe


class RecipesChangeView(View):

    def get(self, request):
        raise Http404

    def post(self, request):
        # Check data:
        print(request.POST)
        allowed_actions = ['1', '2', '3', '4', '5', 'empty_trash']
        if "action" not in request.POST or ("action" in request.POST and request.POST["action"] not in allowed_actions)\
                or ("selection[]" not in request.POST and request.POST["action"] != "empty_trash"):
            return JsonResponse({
                "success": False,
                "message": "Incorrect data!"
            })

        # Get recipes:
        action = request.POST["action"]
        recipes_id = list(map(int, request.POST.getlist("selection[]")))

        # Check data (2):
        if action != "empty_trash":
            if len(recipes_id) == 0:
                return JsonResponse({
                    "success": False,
                    "message": "No recipe provided!"
                })

            recipes = Recipe.objects.filter(pk__in=recipes_id)

            # Check rights:
            allowed = True
            if not request.user.is_staff:
                for recipe in recipes:
                    if recipe.author.user != request.user:
                        allowed = False
            if not allowed:
                return JsonResponse({
                    "success": False,
                    "message": "Not allowed!"
                })

            # Do action:
            if len(recipes) == len(recipes_id):
                if action == "1":  # Publish
                    recipes.update(published=True)
                elif action == "2":  # unpublish
                    recipes.update(published=False)
                elif action == "3":  # Trash
                    recipes.update(trash=True)
                elif action == "4":  # Restore
                    recipes.update(trash=False)
                elif action == "5":  # Delete definitively
                    recipes.delete()
                else:
                    return JsonResponse({
                        "success": False,
                        "message": "Unknown action!"
                    })
                return JsonResponse({
                    "success": True
                })
            else:
                return JsonResponse({
                    "success": False,
                    "message": "Unable to get all recipes selected. Please contact us to report the bug."
                })
        else:
            recipes_trash = Recipe.objects.filter(trash=True)
            if request.user.is_staff:
                recipes_trash.delete()
            else:
                for recipe in recipes_trash:
                    if recipe.author.user == request.user:
                        recipe.delete()
            return JsonResponse({
                "success": True
            })
