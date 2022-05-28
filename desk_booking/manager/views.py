from django.shortcuts import render, redirect

from .decorators import manager_user
from .models import *
from .forms import FloorForm
# Create your views here.

@manager_user
def manager_home_view(request):
    location_list = Location.objects.all()
    context = {
        "location_list": location_list,
    }
    return render(request, "manager_home.html", context)

@manager_user
def add_location_view(request):
    
    if(request.method == "POST"):
        name    = request.POST.get("location_name")
        city    = request.POST.get("location_city")
        country = request.POST.get("location_country")

        Location.objects.create(name = name, city = city, country = country)
        return redirect("manager_home") 

    context = {

    }
    return render(request, "add_location.html", context)

@manager_user
def location_view(request, location_id):    
    location = Location.objects.get(id = location_id)
    floors = Floor.objects.filter(parent_location = location)

    context = {
        "location": location,
        "floors": floors,
    }
    return render(request, "location.html", context)

@manager_user
def edit_floor_view(request, floor_id):
    if(request.method == 'POST'):
        desks = request.body
        print(desks)
    
    floor = Floor.objects.get(id = floor_id)
    
    context = {
        "floor": floor,
    }
    return render(request, "edit_floor.html", context)

@manager_user
def add_floor_view(request, location_id):
    if(request.method == 'POST'):
        print(request.FILES)
        map = None
        if "floor_map" in request.FILES:
            map = request.FILES['floor_map']
        name = request.POST.get("floor_name")
        location = Location.objects.get(id = location_id)

        if(len(name) > 0 and map != None):
            new_floor = Floor(name = name, map = map, parent_location = location)
            new_floor.save()
    form = FloorForm()
    context = {
        "form": form
    }
    return render(request, "add_floor.html", context)
