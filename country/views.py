from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView, TemplateView
from .models import Pays, Climat
from django.db import connection
# Create your views here.

def dictGetColumn(cursor):
    "Return all columns of select statement"
    columns = [col[0] for col in cursor.description]
    return columns

class QueryView(TemplateView):
    query = None
    query_context_name = None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with connection.cursor() as cursor:
            cursor.execute(self.query)
            
            row = cursor.fetchall()
            context[self.query_context_name] = list((row))
            context["columns"] = dictGetColumn(cursor)
            
        return context
    def get_query(self):
        return self.query
    def get_query_context_name(self):
        return self.get_query_context_name


class CountryListView(QueryView):
    
    template_name= "country/pays_list.html"
    query = "SELECT * FROM Pays;"
    query_context_name= "countrys"


class CountryDetailView(DetailView):
    model = Pays
    context_object_name= "country"
    #queryset = Pays.objects.raw("SELECT * FROM Pays WHERE iso=%s;", [request.GET.get("iso")])

class CountryDetailView2(TemplateView):
    
    template_name= "country/country_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("Param : " +kwargs["iso"] )
        raw_sql = Pays.objects.raw("SELECT * FROM Country WHERE iso=%s;", [kwargs["iso"]])
        context["country"] = raw_sql[0]
        return context

class ClimatListView(ListView):
    model = Climat
    context_object_name= "climats"
    queryset = Climat.objects.raw("SELECT * FROM Climat;")

    

