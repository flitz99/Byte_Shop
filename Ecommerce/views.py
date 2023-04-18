from cmath import e
from django.http import HttpResponse
from datetime import datetime 
from django.shortcuts import render
from products.models import Product, Smartphone, Computer


def home(request):  #View per la Homepage

    ctx= {"ciao": "ciao"}
    
    
    
    return render(request, template_name="home.html", context=ctx) #restituisco il template

