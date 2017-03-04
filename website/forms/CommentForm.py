from django import forms
from django.utils.translation import ugettext as _
from captcha.fields import CaptchaField


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for bound_field in self:
            if hasattr(bound_field, "field") and bound_field.field.required:
                bound_field.field.widget.attrs["required"] = "required"


class CommentForm(BaseForm):

    name = forms.CharField(label=_('Name'), max_length=100, required=True)
    email = forms.EmailField(label=_("Email"), required=True)
    website = forms.CharField(label=_("Website"), max_length=255, required=False)
    text = forms.CharField(label=_("Comment"), widget=forms.Textarea)
    captcha = CaptchaField()


class CommentFormAuthenticated(BaseForm):

    text = forms.CharField(label="Comment", widget=forms.Textarea)