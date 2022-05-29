from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .decorators import manager_user
from .models import *
from .forms import FloorForm
import json
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
        desks = desks.decode()
        desks = json.loads(desks)
        curr_floor = Floor.objects.get(id = floor_id)
        prev_desks = Desk.objects.filter(parent_floor = curr_floor)
        
        prev_desk_list = [
            [x.left_up_x, x.left_up_y, x.right_down_x, x.right_down_y]
            for x in prev_desks
        ]

        for i in range(len(prev_desk_list)):
            if(prev_desk_list[i] not in desks):
                prev_desks[i].delete()
        
        desks_to_be_added = [desk for desk in desks if desk not in prev_desk_list]

        for desk in desks_to_be_added:
            add_desk = Desk(
                left_up_x = desk[0],
                left_up_y = desk[1],
                right_down_x = desk[2],
                right_down_y = desk[3],
                parent_floor = curr_floor
            )
            add_desk.save()
        
        return HttpResponse("E bine fra")

    
    floor = Floor.objects.get(id = floor_id)
    desks = Desk.objects.filter(parent_floor = floor)

    desk_list = [
        [x.left_up_x, x.left_up_y, x.right_down_x, x.right_down_y]
        for x in desks
    ]
    context = {
        "floor": floor,
        "desk_list": desk_list
    }
    return render(request, "edit_floor.html", context)

@manager_user
def add_floor_view(request, location_id):
    if(request.method == 'POST'):
        #print(request.FILES)
        map = None
        if "floor_map" in request.FILES:
            map = request.FILES['floor_map']
        name = request.POST.get("floor_name")
        location = Location.objects.get(id = location_id)

        if(len(name) > 0 and map != None):
            new_floor = Floor(name = name, map = map, parent_location = location)
            new_floor.save()
        return redirect("location", location_id)
    form = FloorForm()
    context = {
        "form": form
    }
    return render(request, "add_floor.html", context)

@manager_user
def statistics_view(request):
    if(request.method == 'FETCH'):

        all_bookings = Booking.objects.all().order_by("end_booking")

        location_distribution = {

        }

        floor_distribution = {

        }

        user_ids = set()

        for booking in all_bookings:
            location_distribution[booking.parent_desk.parent_floor.parent_location.name] = 0
        for booking in all_bookings:
            location_distribution[booking.parent_desk.parent_floor.parent_location.name] += 1

        for booking in all_bookings:
            floor_distribution["Floor " + booking.parent_desk.parent_floor.name] = 0
            now = datetime.now().date()
            end_booking = booking.end_booking
            start_booking = booking.start_booking
            if ((end_booking < now and (now - end_booking).days < 7) or (start_booking < now and (now - start_booking).days < 7)):
                user_ids.add(booking.booked_by.id)
        for booking in all_bookings:
            floor_distribution["Floor " + booking.parent_desk.parent_floor.name] += 1

        percentage_last_week = len(user_ids) / User.objects.all().count()


        return JsonResponse(json.dumps({
            "location_distribution": location_distribution,
            "floor_distribution": floor_distribution,
            "percentage_last_week": percentage_last_week
        }), safe=False)
        

    return render(request, "statistics.html", {})