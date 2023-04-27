from django.shortcuts import render
from .models import Ordine, Recensione, Ordine_Item
from authentication.models import Client
from cart.models import *
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import datetime, random, string

#View con gli ordini del cliente registrato
def my_orders(request):

    templ="orders/my_orders.html"

    user=User.objects.get(username=request.user) #acquisisco user
    client=Client.objects.get(user=user) #acquisisco client

    ordini= Ordine.objects.filter(client=client).order_by('-date') #Acquisisco ordini del cliente ordinati col più recente

    ctx={"listaordini":ordini}

    #lista_ordini=Ordine.objects.filter(client_id=client_id) #Acquisisco lista ordini per dato cliente


    return render(request,template_name=templ,context=ctx)

#Creazione nuovo ordine, modifica quantità del prodotto e cancellazione oggetti nel carrello
def create_order(request):
    
    #Acquisisco il carrello dell'utente
    user=User.objects.get(username=request.user) #acquisisco user
    client=Client.objects.get(user=user) #acquisisco client
    carrello=Carrello.objects.get(user=client) #Acquisisco carrello relativo all'utente loggato

    #Creo nuovo ordine
    new_order=Ordine()
    new_order.date= datetime.date.today()
    new_order.client=client

    #Genero codice ordine
    length_of_string = 8
    order_code=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
    new_order.id_ordine=order_code
    new_order.save()

    total_price=0
    #Acquisisco prodotti carrello e creo prodotti dell'ordine
    for c in carrello.prodotti.all():
        new_order_item= Ordine_Item()
        new_order_item.item=c.item
        new_order_item.quantity=c.quantity
        new_order_item.price=c.price
        new_order_item.save() #Salvo nuovo oggetto dell'ordine

        total_price+=c.price
        new_order.prodotti.add(new_order_item)

    new_order.total_price=round(total_price,2)
    new_order.save()
    
    #Modifico quantità disponibile prodotti acquistati
    modifica_quantità(carrello)

    #Svuoto il carrello
    svuota_carrello(carrello)

    return redirect("./my_orders")

#Elimina tutti gli oggetti dal carrello
def svuota_carrello(carrello):
    for c in carrello.prodotti.all():
        c.delete() #elimino oggetti dal carrello

#Modifica le quantità dei prodotti dopo che è stato effettuato un ordine
def modifica_quantità(carrello):
    for c in carrello.prodotti.all():
        prodotto= Product.objects.get(product_code=c.item.product_code)
        prodotto.quantity=prodotto.quantity-c.quantity
        prodotto.save()

