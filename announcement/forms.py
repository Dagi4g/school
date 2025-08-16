from django import forms

class SectionLookupForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    grade = forms.IntegerField()