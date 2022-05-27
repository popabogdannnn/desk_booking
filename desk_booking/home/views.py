from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .decorators import *
from .forms import CreateUserForm

# Create your views here. 

@unauthenticated_user
def home_view(request):
    if(request.user.is_superuser):
        return redirect("manager_home")
    else:
        return render(request, "employee_home.html", {})

@authenticated_user
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Username sau Parola incorecta")
    context = {

    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    return redirect("home")

@authenticated_user
def register_view(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")

    context = {
        "form" : form,
    }
    return render(request, "register.html", context)