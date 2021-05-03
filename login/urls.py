from django.urls import path
from . import views
app_name='login'
urlpatterns = [
    
    path('login', views.LoginView.as_view(), name="login"),
    path('login2', views.log_log_user, name="login2"),
   
]