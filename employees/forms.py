from django import forms
from django.forms import inlineformset_factory
from .models import Employee, Skills


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']
        widgets = {
            'join_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'emp_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'emp_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = ['skills_name']


SkillFormSet = inlineformset_factory(
    Employee,
    Skills,
    form=SkillForm,
    fields=['skills_name'],
    extra=1,
    can_delete=True
)
