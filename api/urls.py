"""APPTBT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
""" 
from django.urls import path,include
from . import views

urlpatterns = [  
         path('blockchain/add_block/', views.add_block), 
         path('blockchain/get_block/<int:index>', views.get_block), 
         path('blockchain/get_chain/', views.get_chain), 
         path('blockchain/validate_block/', views.validate_block),          
         path('blockchain/is_chain_valid/', views.is_chain_valid),         
]
