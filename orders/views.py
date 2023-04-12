from django.shortcuts import render
from .models import Ordine, Recensione
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def my_orders(request):

    templ="orders/my_orders.html"
    ctx={}

    #lista_ordini=Ordine.objects.filter(client_id=client_id) #Acquisisco lista ordini per dato cliente


    return render(request,template_name=templ,context=ctx)

def create_order(request):
    print("creo ordine")

    return redirect("orders")
