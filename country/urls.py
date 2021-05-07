from django.urls import path
from . import views
app_name='country'
urlpatterns = [
    path('', views.CountryListView.as_view(), name="country-list"),
    path('form_prepared_query', views.FormPreparedQuery.as_view() , name="form-prepared-query"),
    path('receive_form_prepared_query', views.handle_form_prepared_query , name="receive-form-prepared-query"),
    path('requete_sql', views.Sql_query.as_view() , name="requete-sql"),
    path('writed_query_validation/', views.writed_query_form_validation, name='writed_query_validation'),

   
]