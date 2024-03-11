from django.urls import path
from . import views

urlpatterns = [  
    path('attack.py', views.attack, name='attack'), 
]
