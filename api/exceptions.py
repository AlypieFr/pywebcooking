from rest_framework.exceptions import APIException


class RecipeNotFound(APIException):
    status_code = 404
    default_detail = 'Recipe not found, or you have not access to it.'
    default_code = 'recipe not found'
