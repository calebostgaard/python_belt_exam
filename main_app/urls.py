from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('log_in', views.log_in),
    path('dashboard', views.dashboard),
    path('trips/new', views.new_trip),
    path('create_trip', views.create_trip),
    path('delete/<int:num>', views.delete_trip),
    path('trips/edit/<int:num>', views.edit_trip),
    path('edit_trip_execute/<int:num>', views.edit_trip_execute),
    path('trips/<int:num>', views.view_trip),
    path('join/<int:num>', views.join_trip),
    path('cancel/<int:num>', views.cancel_trip),
    path('log_out', views.log_out),
]
