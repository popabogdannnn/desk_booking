from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.employee_home_view, name = "employee_home"),
    path("book/", views.book_desk_view, name = "book_desk")

]