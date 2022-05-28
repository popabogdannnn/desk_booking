from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.employee_home_view, name = "employee_home"),
    path("book/", views.book_desk_view, name = "book_desk"),
    path("book/send/", views.book_desk_handler),
    path("my_bookings/", views.my_bookings_view, name="my_bookings")
]