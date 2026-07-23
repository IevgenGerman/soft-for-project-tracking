from django import forms
from django.contrib.auth.forms import UserCreationForm

from monitor.models import Project, TeamMember


class TeamMemberCreationForm(UserCreationForm):
    languages = forms.ModelMultipleChoiceField(
        queryset=TeamMember.languages.field.related_model.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta(UserCreationForm.Meta):
        model = TeamMember
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
            "role",
            "license_number",
            "team",
            "languages",
        )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ("slug",)
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
