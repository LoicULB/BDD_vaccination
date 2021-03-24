from django.urls import path
from . import views
app_name='country'
urlpatterns = [
    path('', views.CountryListView.as_view(), name="country-list"),
    path('detail/<str:iso>', views.CountryDetailView2.as_view(), name="country-detail"),
    path('climats', views.ClimatListView.as_view() , name="climat-list"),
   
]