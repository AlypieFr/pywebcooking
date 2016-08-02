from website.models import Proposal, Recipe
from website.functions.exceptions import RequiredParameterException, MissingKeyException, UnknownKeyException


class CProposal:
    @staticmethod
    def add_new_to_recipe(text_cons: str, nb: int, recipe: Recipe) -> Proposal:
        # Test parameters:
        if text_cons is not None and (not isinstance(text_cons, str)):
            raise TypeError("text_cons must be a string")
        if text_cons is None or len(text_cons) == 0:
            raise RequiredParameterException("text_cons is required and must be not empty")
        if nb is not None and (not isinstance(nb, int)):
            raise TypeError("nb must be an integer")
        if nb is None:
            raise RequiredParameterException("nb is required")
        if recipe is not None and (not isinstance(recipe, Recipe)):
            raise TypeError("recipe must be an instance of the Recipe class")
        if recipe is None:
            raise RequiredParameterException("recipe is required")

        # Do the add:
        p = Proposal(text_cons=text_cons, nb=nb, recipe=recipe)
        p.save()

        return p

    @staticmethod
    def add_new_list_to_recipe(proposals: list, recipe: Recipe):
        # Check parameters:
        if proposals is not None and (not isinstance(proposals, list)):
            raise TypeError("proposals must be a list")
        if proposals is None or len(proposals) == 0:
            raise RequiredParameterException("proposals is required and must be not empty")
        else:
            for proposal in proposals:
                req_keys = {
                    "text_cons": False,
                    "nb": False
                }
                for key, value in proposal.items():
                    if key in req_keys:
                        req_keys[key] = True
                        if key == "text_cons":
                            if value is not None and (not isinstance(value, str)):
                                raise TypeError("proposal: text_cons must be a string")
                            if value is None or len(value) == 0:
                                raise RequiredParameterException("proposal: text_cons must be not none or empty")
                        elif key == "nb":
                            if value is not None and (not isinstance(value, int)):
                                raise TypeError("proposal: nb must be an integer")
                            if value is None:
                                raise RequiredParameterException("proposal: nb is required")
                    else:
                        raise UnknownKeyException("proposal: unknown key: " + key)
                for key in req_keys:
                    if not req_keys[key]:
                        raise MissingKeyException("proposal: missing key: " + key)
        if recipe is not None and (not isinstance(recipe, Recipe)):
            raise TypeError("recipe must be an instance of the Recipe class")
        if recipe is None:
            raise RequiredParameterException("recipe is required")

        # Do the add:
        p_list = []
        for proposal in proposals:
            p_list.append(CProposal.add_new_to_recipe(proposal["text_cons"], proposal["nb"], recipe))

        return p_list

    @staticmethod
    def build_html_for_proposals(recipe: Recipe) -> str:
        # Check parameters:
        if recipe is not None and (not isinstance(recipe, Recipe)):
            raise TypeError("recipe must be an instance of the Recipe class")
        if recipe is None:
            raise RequiredParameterException("recipe is required")

        proposals_query = recipe.proposal_set.iterator()
        proposals = []
        for p in proposals_query:
            proposals.append(p)
        proposals.sort(key=lambda k: k.nb)

        html = "<ul>"
        for p in proposals:
            html += "<li>" + p.text_cons + "</li>"
        html += "</ul>"

        return html
