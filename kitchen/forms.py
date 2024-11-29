from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory

from kitchen.models import Cook, Dish, DishType, Ingredient


class SearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(),
        label="",
    )

    def __init__(self, *args, **kwargs):
        placeholder = kwargs.pop("placeholder", "Search...")
        super().__init__(*args, **kwargs)
        self.fields["search"].widget.attrs["placeholder"] = placeholder


def validate_experience_years(years_of_experience):
    if years_of_experience is not None and years_of_experience < 2:
        raise forms.ValidationError(
            {
                "years_of_experience": "Cook must "
                "have at least 2 years of experience."
            }
        )

    return years_of_experience


class CookCreationForm(UserCreationForm):
    years_of_experience = forms.IntegerField(
        required=True,
        min_value=0,
        label="Years of Experience",
        help_text="Enter the number of years of experience.",
    )

    class Meta:
        model = Cook
        fields = [
            "username",
            "first_name",
            "last_name",
            "years_of_experience",
            "password1",
            "password2",
        ]


class CookExperienceUpdateForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = ["years_of_experience"]

    def validate_experience_years(self):
        return validate_experience_years(
            self.cleaned_data["years_of_experience"]
        )


class DishCreationForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=Cook.objects,
        required=True,
        widget=forms.CheckboxSelectMultiple,
        label="Assign cook(s)",
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Ingredients",
    )

    class Meta:
        model = Dish
        fields = [
            "name",
            "description",
            "price",
            "dish_type",
            "cooks",
            "ingredients",
        ]


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name"]


IngredientFormSet = modelformset_factory(
    Ingredient,
    form=IngredientForm,
    extra=1,
)


class DishTypeForm(forms.ModelForm):
    class Meta:
        model = DishType
        fields = ["name"]


DishTypeFormSet = modelformset_factory(DishType, form=DishTypeForm, extra=1)
