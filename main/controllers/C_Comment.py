from main.models.Comment import Comment
from main.models.Recipe import Recipe
from main.models.UserProfile import UserProfile
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

    @staticmethod
    def get_recipe_comments(recipe: Recipe) -> "list of dict":
        if recipe is not None and (not isinstance(recipe, Recipe)):
            raise TypeError("recipe must be an instance of the Recipe class")
        if recipe is None:
            raise RequiredParameterException("recipe is required")

        comments_o = Comment.objects.filter(recipe=recipe).order_by("pub_date")
        comments = []
        for comment_o in comments_o:
            comment = {"content": comment_o.content, "id": comment_o.id, "date": comment_o.pub_date}
            if comment_o.author is not None:
                comment["authenticated"] = True
                comment["pseudo"] = comment_o.author.user.first_name
                comment["email"] = comment_o.author.user.email
                comment["author_url"] = comment_o.author.url
            else:
                comment["authenticated"] = False
                comment["pseudo"] = comment_o.pseudo
                comment["email"] = comment_o.mail
                comment["website"] = comment_o.website
            comments.append(comment)

        return comments
