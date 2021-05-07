from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView, TemplateView
from .models import Pays, Climat
from django.db import connection
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
class LoginView(TemplateView):
    template_name = "registration/login.html"
def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...
# Create your views here.

def dictGetColumn(cursor):
    "Return all columns of select statement"
    columns = [col[0] for col in cursor.description]
    return columns
def is_dsl(query):
    splited_query=query.split(" ")
    return splited_query[0].lower() == "select"

def is_user_epidemiologist(user):
    with connection.cursor() as cursor:
            cursor.execute("""SELECT e.uuid 
                            FROM utilisateur u join epidemiologiste e ON u.uuid=e.uuid
                            WHERE u.id=%s""", [user.id])
            
            row = cursor.fetchone()
    return row is not None
class QueryView(LoginRequiredMixin,TemplateView):
    query = None
    query_context_name = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(make_password("Pikachu"))
        print(check_password("Pikachu", "pbkdf2_sha256$216000$NRinKHRX2HRS$cTc6kK/J9gBDSSCrfMCOkPObJZMwCD+dX4jpLrNtqfM="))
        print(self.request.user)
        print(is_user_epidemiologist(self.request.user))
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
    query = "SELECT * FROM pays;"
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

class FormPreparedQuery(TemplateView, LoginRequiredMixin):
    template_name= "country/form_prepared_query.html"

# ajax_posting function
@login_required
def ajax_posting(request):
    if request.is_ajax():
        query = request.POST.get('query', None) # getting data from first_name input 
        
        if (not is_dsl(query)):
        
            if( not is_user_epidemiologist(request.user)):
                msg = "MDR t'es pas un epi mon coco lapin"
            
        
                response = {
                    
                    'msg': msg # response message
                }
                return HttpResponse(msg, status=403)
                #return JsonResponse(response, status=400) # return response as JSON
        response = {
                    
            'msg': "success", # response message
            'url' : reverse('country:country-list'),

        }
        return JsonResponse(response)  

@login_required
def handle_form_prepared_query(request):
    print(request.GET["query"])
    query = request.GET["query"]
    error= None
    
    if (not is_dsl(query)):
        print("C'est pas du DSL")
        if( not is_user_epidemiologist(request.user)):
            print("MDR t'es pas un epi mon coco lapin")
            error = "MDR faut être un épidemiologiste pour pouvoir faire du DDL mon coco"
            return render(request, 'country/requete_sql.html', {'errors' : error })
        else :
            print("Tu es un épi mon coco")

            with connection.cursor() as cursor:
                cursor.execute(query)
            
               
                result  = ""
                col = ""
                return render(request, 'country/requete_sql.html', {'errors' : "Success" })
    else:
        print("C'est du DSL")     
        with connection.cursor() as cursor:
            cursor.execute(query)
            
            row = cursor.fetchall()
            result  = list((row))
            col = dictGetColumn(cursor)       
    return render(request, 'country/pays_list.html', {'countrys': result , 'columns' : col })
    
class Sql_query(TemplateView):
    template_name= "country/requete_sql.html"


