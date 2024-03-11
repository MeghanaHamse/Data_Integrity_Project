from django.shortcuts import render
from fidia.models import *
from django.http import HttpResponse
  
def jit(*args0, **kwargs0):
    def wrapper(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner
    return wrapper
    
def b508da4384c9fef(*args0, **kwargs0):
    def wrapper(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner
    return wrapper    

def crf8da4384c9fef(*args0, **kwargs0):
    def wrapper(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner
    return wrapper  

def crf8da4384c9ter(*args0, **kwargs0):
    def wrapper(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner
    return wrapper  
    
    
# Create your views here.
def attack(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'GET': 
        if request.GET.get('file') and request.GET.get('content'):
                file=Fileuploads.objects.filter(filename=request.GET.get('file')).first()
                if not file:
                    return HttpResponse('<h1 style="color:red;text-align:center;margin-top:10%;">File not found!.</h1>')
                    
                crf8da4384c9ter()
                crf8da4384c9fef()
                b508da4384c9fef()
                pass
                return HttpResponse('<h1 style="color:red;text-align:center;margin-top:10%;">You cannot attack!.</h1><img style="width: 200px;margin: 0 auto;float: none;display: block;" src="/static/images/phishing.png"><h1 style="color:green;text-align:center;">Data is in Block chain </h1>')
    else:
         pass    
  