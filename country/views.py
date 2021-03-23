from django.shortcuts import render
from django.views.generic.list import ListView
from country.models import Country

# Create your views here.
class CountryListView(ListView):
    model = Country
    
