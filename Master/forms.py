from django import forms
from .models import Department, Designation, Location

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name', 'dept_description']

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['loc_name', 'loc_description']

class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['department', 'des_name', 'des_description']