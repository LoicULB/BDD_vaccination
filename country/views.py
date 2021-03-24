from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView, TemplateView
from country.models import Country, Climat

# Create your views here.
class CountryListView(ListView):
    model = Country
    context_object_name= "countrys"
    queryset = Country.objects.raw("SELECT * FROM Country;")

class CountryDetailView(DetailView):
    model = Country
    context_object_name= "country"
    #queryset = Country.objects.raw("SELECT * FROM Country WHERE iso=%s;", [request.GET.get("iso")])

class CountryDetailView2(TemplateView):
    
    template_name= "country/country_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("Param : " +kwargs["iso"] )
        raw_sql = Country.objects.raw("SELECT * FROM Country WHERE iso=%s;", [kwargs["iso"]])
        context["country"] = raw_sql[0]
        return context

class ClimatListView(ListView):
    print("Whar happen")
    model = Climat
    context_object_name= "climats"
    queryset = Climat.objects.raw("SELECT * FROM Climat;")

    

