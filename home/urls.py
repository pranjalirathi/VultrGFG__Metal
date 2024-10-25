from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('begins', views.forms, name='forms'),
    path("exercise/<slug>", views.exercise, name='exercise'),
    path("prepare", views.prepare, name="prepare"),
    path("calculate", views.calculate, name="calculate"),
]