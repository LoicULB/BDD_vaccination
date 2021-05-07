from django import forms

class QueryForm(forms.Form):
    query = forms.CharField(label='Your name', max_length=100, required=True)