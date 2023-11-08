# suricata_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("stats/", views.view_stats, name="view_stats"),
    path("events/", views.view_events, name="view_events"),
    path("fast/", views.view_fast, name="view_fast"),
    path("", views.index, name="index"),
    path('service-control/', views.service_control, name='service_control'),
]
