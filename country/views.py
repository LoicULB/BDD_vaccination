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
from django.db import Error, IntegrityError
from .forms import CreateUserForm
from django.views.generic.edit import FormView
import uuid



# Create your views here.

def dictGetColumn(cursor):
    "Return all columns of select statement"
    columns = [col[0] for col in cursor.description]
    return columns
def get_sql_type(query):
    splited_query=query.split(" ")
    return splited_query[0].lower()
def is_dsl(query):
    
    return get_sql_type(query) == "select"

def is_user_epidemiologist(user):
    with connection.cursor() as cursor:
            cursor.execute("""SELECT e.uuid 
                            FROM utilisateur u join epidemiologiste e ON u.uuid=e.uuid
                            WHERE u.id=%s""", [user.id])
            
            row = cursor.fetchone()
    return row is not None
def is_user_id_epidemiologist(user_id):
    with connection.cursor() as cursor:
            cursor.execute("""SELECT e.uuid 
                            FROM utilisateur u join epidemiologiste e ON u.uuid=e.uuid
                            WHERE u.id=%s""", [user_id])
            
            row = cursor.fetchone()
    return row is not None
def execute_sql(sql, param=None):
    response = {}
    with connection.cursor() as cursor:
        cursor.execute(sql, param)
            
        row = cursor.fetchall()
        response["result"]  = row
        response["columns"] = dictGetColumn(cursor) 
    return response
def execute_sql_one(sql, param=None):
    response = {}
    with connection.cursor() as cursor:
        cursor.execute(sql, param)
            
        row = cursor.fetchone()
        response["result"]  = row
        response["columns"] = dictGetColumn(cursor) 
    return response
def create_user_dict(data_form):
    user_dict = {}
    print("Les keys")
    for key in data_form.keys():
        if data_form[key] and key != 'csrfmiddlewaretoken':
            user_dict[key]= data_form[key]
            print(data_form[key])
    if not data_form['uuid']:
        user_dict["uuid"] = uuid.uuid4()
    return user_dict
def create_user(form):
    user_dict = create_user_dict(form.data)
    query_columns = ""
    index_key=1
    for key in user_dict.keys():

        query_columns += key
        if(index_key<len(user_dict.keys())):
            query_columns+=","
        index_key+=1   
    query_values = ""
    index_key=1
    for value in user_dict.values():

        query_values += f"$${value}$$"
        if index_key<len(user_dict):
            query_values+=","
        index_key+=1   
    
    print( query_columns)
    print(query_values)
    query = f"INSERT INTO utilisateur({query_columns}) VALUES ({query_values}) RETURNING id;"
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
        return row[0]
class QueryView(LoginRequiredMixin,TemplateView):
    query = None
    query_context_name = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        response_sql = execute_sql(self.query)
        context[self.query_context_name] = response_sql["result"] 
        context["columns"] = response_sql["columns"]
           
        return context
    def get_query(self):
        return self.query
    def get_query_context_name(self):
        return self.get_query_context_name


class CountryListView(QueryView):
    
    template_name= "country/pays_list.html"
    query = "SELECT * FROM pays;"
    query_context_name= "countrys"


class FormPreparedQuery(TemplateView, LoginRequiredMixin):
    template_name= "country/form_prepared_query.html"

@login_required
def writed_query_form_validation(request):
    if request.is_ajax():
        query = request.POST.get('query', None) # getting data from first_name input 
        
        if (not is_dsl(query)):
        
            if( not is_user_epidemiologist(request.user)):
                msg = "MDR t'es pas un epi mon coco lapin"
            
                response = {
                    
                    'msg': msg # response message
                }
                return HttpResponse(msg, status=403)
            else :
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(query)
                    response = {
                        'type' : get_sql_type(query),
                        'msg': "L'instruction " +get_sql_type(query) + " s'est bien déroulée" # response message
                    }
                    return JsonResponse(response) 
                    # code that produces error
                except Error as e:
                        
                    return HttpResponse(str(e), status=500)
                
                
                
        response = {
            'type' : get_sql_type(query),   
            'msg': "success", # response message
            'url' : reverse('country:receive-form-prepared-query') +"?query=" + query,

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
                return render(request, 'country/requete_sql.html', {'success' : "Success" })
    else:
          
        response_sql = execute_sql(query)
        
    return render(request, 'country/select_results.html', {'results': response_sql["result"] , 'columns' : response_sql["columns"] })
    
class Sql_query(TemplateView):
    template_name= "country/requete_sql.html"

class UserProfile(TemplateView):
    template_name= "country/user_profile.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("Le param est : " +str(kwargs["id"]))
        response_sql = execute_sql_one("SELECT u.id, u.uuid, u.nom, u.prenom, u.pseudo, u.rue_adresse, u.code_postal_adresse, u.numero_adresse, u.ville_adresse, e.centre, e.telephone_service FROM utilisateur u LEFT JOIN epidemiologiste e ON u.uuid=e.uuid  WHERE id=%s", [kwargs["id"]])
        print("La réponse est = " +str(response_sql["result"]))
        print("Les colonnes sont : " +str(response_sql["columns"]))
        user_data = {}
        for key in range(len(response_sql["columns"])):
            user_data[response_sql["columns"][key]]=response_sql["result"][key]
             
        user_data["is_epidemiologist"] = is_user_id_epidemiologist(kwargs["id"] )
        print(user_data)
        context["user"] = user_data
        
           
        return context
class CreateUserFormView(FormView):
    template_name = 'country/create_user.html'
    form_class = CreateUserForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print("Form is : ")
        print(form.data)
        id_user = create_user(form)
        self.success_url = reverse('country:user-profile',  kwargs={'id':id_user})
        return super().form_valid(form)