from django.urls import path
from . import views
app_name='country'
urlpatterns = [
    path('', views.CountryListView.as_view(), name="country-list"),
    path('detail/<str:iso>', views.CountryDetailView2.as_view(), name="country-detail"),
    path('climats', views.ClimatListView.as_view() , name="climat-list"),
    path('form_prepared_query', views.FormPreparedQuery.as_view() , name="form-prepared-query"),
    path('receive_form_prepared_query', views.handle_form_prepared_query , name="receive-form-prepared-query"),
    path('login', views.LoginView.as_view(), name="login"),
   
]