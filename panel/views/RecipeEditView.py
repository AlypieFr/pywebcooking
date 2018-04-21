from django.views.generic import View
from django.http import JsonResponse, Http404, HttpResponseRedirect
from main.models.Recipe import Recipe


class RecipeEditView(View):

    def get(self, request):
        raise Http404

    def post(self, request, slug):

        print(request.POST)
        print(slug)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

        # return JsonResponse({
        #     "success": True
        # })
