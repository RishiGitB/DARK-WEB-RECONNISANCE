from django.contrib import admin
from django.urls import path
from home import views


urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('check/', views.check_suspicious, name='check_suspicious'),
]
