from django import forms

class UserForm(forms.Form):
    username = forms.CharField(label='Your name', max_length=200)
    password = forms.CharField(label="Password", max_length=200)


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)