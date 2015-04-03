from django import forms


class CitizenForm(forms.Form):
    name = forms.CharField()
    lastname = forms.CharField()
    photo = forms.ImageField()
    social = forms.CharField()