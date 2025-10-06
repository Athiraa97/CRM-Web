from django import forms
from django.forms import ModelForm, modelformset_factory
from .models import Employee, Skills

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        exclude = ['created_at', 'created_by', 'updated_at', 'updated_by']


SkillFormSet = modelformset_factory(
    Skills,
    fields=('skills_name',),
    extra=1,
    can_delete=True
)
