from django.shortcuts import render

from django.views.generic.list import ListView
from django.views.generic import DetailView, TemplateView

from django.db import connection
from django.contrib.auth import authenticate, login
from .forms import UserForm, NameForm

class LoginView(TemplateView):
    template_name = "registration/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UserForm()
        
        return context

def log_log_user(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return render(request, 'registration/login.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()

    return render(request, 'registration/login.html', {'form': form})