from django import forms

class searchForm(forms.Form):
    name = forms.CharField(label='Search Recipe Name', max_length=100)
