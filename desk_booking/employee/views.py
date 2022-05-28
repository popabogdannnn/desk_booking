from django.forms import all_valid
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

import json
from datetime import datetime
from .decorators import unauthenticated_user
from manager.models import Desk, Booking, Floor

# Create your views here.

@unauthenticated_user
def employee_home_view(request):
    
    context = {

    }
    return render(request, "employee_home.html", context)

@unauthenticated_user
def book_desk_view(request):
    context = {

    }
    if request.method == 'FETCH':
        dates = json.loads(request.body.decode())
        
        if(dates['first_day'] == "" or dates['last_day'] == ""):
            return JsonResponse(json.dumps({}), safe=False)

        dates = {
            'first_day': datetime.strptime(dates['first_day'], '%Y-%m-%d'),
            'last_day': datetime.strptime(dates['last_day'], '%Y-%m-%d')
        }

        bookings_overlapping = Booking.objects.exclude(start_booking__gt = dates['last_day']).exclude(end_booking__lt = dates['first_day'])

        desks_id = [x.parent_desk.id for x in bookings_overlapping]

        available_desks = Desk.objects.exclude(id__in = desks_id).values()
        available_desks = [desk for desk in available_desks]
        
        floors_with_available_desks = {}
        for x in available_desks:
            floor = Floor.objects.get(id = x["parent_floor_id"])
            floors_with_available_desks[x["parent_floor_id"]] = {
                "name": str(floor),
                "image_url": floor.map.url,
                "available_desks": []
            }
        
        for x in available_desks:
            floors_with_available_desks[x["parent_floor_id"]]['available_desks'].append([
                x["left_up_x"],
                x["left_up_y"],
                x["right_down_x"],
                x["right_down_y"],
                x["id"]
            ])
        


        return JsonResponse(json.dumps(floors_with_available_desks), safe=False)
        
    
    return render(request, "book_desk.html", context)

@unauthenticated_user
def book_desk_handler(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        
        parent_desk = Desk.objects.get(id = data["desk_id"])
        first_day = data["first_day"]
        last_day = data["last_day"]
        booked_by = request.user
        booking = Booking(booked_by = booked_by, start_booking = first_day, end_booking = last_day, parent_desk = parent_desk)
        booking.save()
        return HttpResponse("E bine")


@unauthenticated_user
def my_bookings_view(request):
    if request.method == 'POST':
        booking_id = request.body.decode()
        Booking.objects.get(id = booking_id).delete()
        return HttpResponse("E bine")


    bookings = Booking.objects.filter(booked_by = request.user)
    context = {
        "bookings": bookings
    }
    return render(request, "my_bookings.html", context)