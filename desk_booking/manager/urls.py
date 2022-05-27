from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.manager_home_view, name = "manager_home"),
    path("add/", views.add_location_view, name = "add_location"),
    path("location/<int:location_id>", views.location_view, name = "location"),
    path("edit_floor/<int:floor_id>", views.edit_floor_view, name = "edit_floor"),
    path("location/<int:location_id>/add", views.add_floor_view, name="add_floor"),
]