from django import forms

class QueryForm(forms.Form):
    query = forms.TextField(label='Your name', max_length=100)