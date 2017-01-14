from main.models import Comment, Recipe, UserProfile
from main.functions.exceptions import RequiredParameterException


class CComment:
    @staticmethod
    def add_new(content: str, recipe: Recipe, pseudo: str = None, mail: str = None, website: str = None,
                author: UserProfile = None, published: bool = True) -> Comment:
        # Check parameters:
        if content is not None and (not isinstance(content, str)):
            raise TypeError("content must be a string")
        if content is None or len(content) == 0:
            raise RequiredParameterException("content is required")
        if recipe is not None and (not isinstance(recipe, Recipe)):
            raise TypeError("recipe must be an instance of the Recipe class")
        if recipe is None:
            raise RequiredParameterException("recipe is required")
        if pseudo is not None and (not isinstance(pseudo, str)):
            raise TypeError("pseudo must be a string, or None")
        if mail is not None and (not isinstance(mail, str)):
            raise TypeError("mail must be a string, or None")
        if website is not None and (not isinstance(website, str)):
            raise TypeError("main must be a string, or None")
        if author is not None and (not isinstance(author, UserProfile)):
            raise TypeError("author must be an instance of the UserProfile class, or None")
        if author is None and pseudo is None:
            raise RequiredParameterException("if you do not give an author, pseudo is required")
        if author is None and mail is None:
            raise RequiredParameterException("if you do not give an author, mail is required")
        if author is not None and (pseudo is not None or mail is not None or website is not None):
            raise RequiredParameterException("if you give author, you cannot give pseudo, mail or main")
        if not isinstance(published, bool):
            raise TypeError("published must be a boolean")

        # Do the add:
        c = Comment(content=content, recipe=recipe, pseudo=pseudo, website=website, mail=mail, author=author,
                    published=published)
        c.save()

        return c
