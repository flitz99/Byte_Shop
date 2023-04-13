from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User

def home(request):
    return redirect('../')

def carrello(request):
    
    templ="cart/carrello.html"

    user=User.objects.get(username=request.user) #acquisisco user
    client=Client.objects.get(user=user) #acquisisco client
    carrello=Carrello.objects.get(user=client) #Acquisisco carrello relativo all'utente loggato
    
    #Acquisisco prezzo totale carrello
    prezzo_totale=0
    for c in carrello.prodotti.all():
        prezzo_totale= prezzo_totale+c.price

    ctx= {"listacarrello":carrello.prodotti,"totale":round(prezzo_totale,2)}

    if request.method == "POST":
        
        quantities=request.POST.getlist('list')

        cont=0
        prezzo_totale=0
        for c in carrello.prodotti.all():
            c.quantity=int(quantities[cont])
            c.price=round(c.item.final_price*c.quantity,2)
            c.save()
            prezzo_totale= prezzo_totale+c.price
            cont=cont+1
        
        ctx= {"listacarrello":carrello.prodotti,"totale":round(prezzo_totale,2)}

    
            

    return render(request, template_name=templ, context=ctx) #restituisco il template

def delete_item(request,prod_code):

    user=User.objects.get(username=request.user) #acquisisco user
    client=Client.objects.get(user=user) #acquisisco client
    carrello=Carrello.objects.get(user=client) #Acquisisco carrello relativo all'utente loggato

    for c in carrello.prodotti.all():
        if c.item.product_code == prod_code:
            c.delete() #elimino oggetto dal carrello

    return redirect("../carrello")






