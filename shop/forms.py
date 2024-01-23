from django import forms


class UserForm(forms.Form):
    count = forms.IntegerField()
