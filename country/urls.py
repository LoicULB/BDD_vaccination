from django.urls import path
from . import views
app_name='country'
urlpatterns = [
    path('', views.CountryListView.as_view(), name="country-list"),
   
]