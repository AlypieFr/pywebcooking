from django import forms
from django.utils.translation import ugettext as _


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for bound_field in self:
            if hasattr(bound_field, "field") and bound_field.field.required:
                bound_field.field.widget.attrs["required"] = "required"


class RecipeForm(BaseForm):

    title = forms.CharField(label=_('Title'), max_length=255, required=True)
    permalink = forms.CharField(label=_("Permalink"), max_length=255, required=True)