from django import forms
from django.utils.translation import ugettext as _, pgettext as __
from main.models.Category import Category


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for bound_field in self:
            if hasattr(bound_field, "field") and bound_field.field.required:
                bound_field.field.widget.attrs["required"] = "required"
            if isinstance(bound_field.field, forms.CharField) or isinstance(bound_field.field, forms.IntegerField) or \
                    isinstance(bound_field.field.widget, forms.Select):
                bound_field.field.widget.attrs["class"] = ((bound_field.field.widget.attrs["class"] + " ")
                                                           if "class" in bound_field.field.widget.attrs else "") + \
                                                          "form-control"


class RecipeForm(BaseForm):
    title = forms.CharField(label=_('Title'), max_length=255, required=True)
    slug = forms.CharField(label=_("Slug"), max_length=255, required=True)
    categories = forms.MultipleChoiceField(
        label=_('Categories'),
        choices=[(cat.id, cat.name) for cat in Category.objects.order_by('order')],
        widget=forms.CheckboxSelectMultiple
    )
    tps_prep_hr = forms.IntegerField(label=_("hours"), min_value=0)
    tps_prep_min = forms.IntegerField(label=_("minutes"), min_value=0, max_value=59, required=True)
    tps_break_j = forms.IntegerField(label=_("days"), min_value=0)
    tps_break_hr = forms.IntegerField(label=_("hours"), min_value=0, max_value=23)
    tps_break_min = forms.IntegerField(label=_("minutes"), min_value=0, max_value=59)
    tps_cook_hr = forms.IntegerField(label=_("hours"), min_value=0)
    tps_cook_min = forms.IntegerField(label=_("minutes"), min_value=0, max_value=59, required=True)
    description = forms.CharField(label=_("Description"), widget=forms.Textarea())
    pub_date = forms.CharField(label=_("Publication date"),
                               widget=forms.TextInput(attrs={"class": "datemask datepicker"}))
    status = forms.MultipleChoiceField(
        label=_('Status'),
        choices=[(1, __("singular", "Published")), (0, _("Draft"))],
        widget=forms.Select
    )
