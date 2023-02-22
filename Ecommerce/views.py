from cmath import e
from django.http import HttpResponse
from datetime import datetime 
from django.shortcuts import render
from products.models import Product, Smartphone, Computer


def home(request):  #View per la Homepage
    products= Product.objects.all() #prendo tutti i prodotti
    ctx= {"listaprodotti": products}
    
    
    if request.user.is_authenticated and request.user.is_staff: # Se utente è autenticato ed è amministratore

        user= request.user # acquisisco utente registrato
        products= Product.objects.filter(supplier=user.id) #prendo prodotti che hanno tale supplier

        ctx = { "listaprodotti": products

        }
    if not request.user.is_authenticated: #Se utente non autenticato
        
        products= Product.objects.all() #prendo tutti i prodotti
        ctx= {"listaprodotti": products}

    
    
    return render(request, template_name="home.html", context=ctx) #restituisco il template

