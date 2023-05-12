from django.shortcuts import render
from products.models import Product
from orders.models import Ordine
from django.contrib.auth.models import User
from authentication.models import Client
import operator
import json

#Metodo per ottenere la quantità acquistata per ogni oggetto in ordine di quantità
def mostpopular(popular,request):

    if request.user.is_authenticated:
        user=User.objects.get(username=request.user) #acquisisco user
        client=Client.objects.get(user=user) #Dallo user acquisisco il client
    
        ordini= Ordine.objects.filter() #Acquisisco tutti gli ordini 
        ordini_utente=Ordine.objects.filter(client=client)

        #Acquisisco prodotti acquistati dall'utente
        prod_utente=[]
        for o in ordini_utente:
            for p in o.prodotti.all():
                prod_utente.append(p.item)
        prod_utente=list(set(prod_utente)) #Rimuovo duplicati


        #Metto in un dizionario la coppia prodotto-quantità acquistata
        for ordine in ordini:
            for p in ordine.prodotti.all():
                if p.item in popular:
                    popular[p.item]+=p.quantity
                else:
                    popular[p.item]=p.quantity

        popular_ord = dict(sorted(popular.items(), key=operator.itemgetter(1), reverse=True)) #Ordino elementi sulla base della quantità acquistata

        #Rimuovo dal dizionario prodotti già acquistati dall'utente
        for p in prod_utente:
            del popular_ord[p]

        popular_ord= dict(list(popular_ord.items())[:9]) #Massimo 6 elementi
        return popular_ord

    else:
        ordini= Ordine.objects.filter() #Acquisisco tutti gli ordini (di tutti gli utenti)

        #Metto in un dizionario la coppia prodotto-quantità acquistata
        for ordine in ordini:
            for p in ordine.prodotti.all():
                if p.item in popular:
                    popular[p.item]+=p.quantity
                else:
                    popular[p.item]=p.quantity

        popular_ord = dict(sorted(popular.items(), key=operator.itemgetter(1), reverse=True)) #Ordino elementi sulla base della quantità acquistata
        popular_ord= dict(list(popular_ord.items())[:9]) #Massimo 6 elementi
        return popular_ord


def recommend(client):
    
    ordini_utente=Ordine.objects.filter(client=client) #Acquisisco ordini fatti dall'utente loggato

    prod_utente=[] #lista con prodotti acquistati dall'utente
    for ord in ordini_utente:
        for p in ord.prodotti.all():
            prod_utente.append(p.item) #Acquisisco prodotti acquistati utente

    #rimuovo duplicati dalla lista:
    prod_utente_nd= list(set(prod_utente)) #nuova lista contenete i prodotti acquistati senza duplicati

    ordini= Ordine.objects.exclude(client=client) #Acquisisco tutti gli ordini degli altri clienti
    
    recommend=[]
    for ordine in ordini:
        if ordine.prodotti.count() > 1: #Se ordine con più di un prodotto
            for p in ordine.prodotti.all():
                    #Se l'ordine di un altro utente contiene prodotto acquistato dall'utente
                    if p.item in prod_utente_nd:
                        recommend.append(ordine) #Mi salvo l'ordine

    #Rimuovo dalla lista i prodotti che ho acquistato
    recommend_new=[]
    for o in recommend:
        for p in o.prodotti.all():
            if p.item not in prod_utente_nd:
                recommend_new.append(p.item)

    recommend_new= list(set(recommend_new)) #Rimuovo duplicati dalla lista
    
    # recommend_new=recommend_new[:6] Riduco elementi (max 6)
    return recommend_new

def all_products():

    products=Product.objects.filter() #Acquisisco tutti i prodotti

    return products

def home(request):  #View per la Homepage

    ctx= {} 
    
    #--- Se utente loggato
    if request.user.is_authenticated:

        #---- Se utente loggato amministratore
        if request.user.is_staff:
            user=User.objects.get(username=request.user) #acquisisco user
            
            #Se amministratore ha dei prodotti caricati
            if  Product.objects.filter(supplier=user):
                prodotti= Product.objects.filter(supplier=user) #acquisisco prodotti inseriti dall'utente amministratore
                products={}

                for prodotto in prodotti:
                    products[prodotto.name]=0

                ordini= Ordine.objects.filter()
                for ordine in ordini:
                    for p in ordine.prodotti.all():
                        if p.item.supplier==user: #Se quel prodotto è stato inserito dall'utente
                            products[p.item.name]+=p.quantity

                ctx={'products':json.dumps(products),'check':True,'title':"Vendite dei prodotti inseriti:"}

            #Se amministratore non ha dei prodotti caricati
            else:
                ctx={'check':False} #passo lista vuota

        #---- Se utente loggato è un cliente
        if not request.user.is_staff:

            user=User.objects.get(username=request.user) #acquisisco user
            client=Client.objects.get(user=user) #Dallo user acquisisco il client

            #Se cliente ha fatto acquisti
            if Ordine.objects.filter(client=client).exists():
                
                recommended = recommend(client) #Acquisisco prodotti consigliati per l'utente
                
                if len(recommended) > 0: #Se ho almeno un prodotto raccomandato
                    ctx= {"listaprodotti": recommended,'title':"Prodotti consigliati in base ai tuoi acquisti:"} #listaprodotti contiene i prodotti raccomandati
                
                else: #Se non ho prodotti da consigliare

                    #Se esistono acquisti fatti da altri utenti
                    if Ordine.objects.exclude(client=client).exists():
                        popular={}
                        popular_ord= mostpopular(popular,request) #Acquisisco oggetti più popolari in ordine di quantità acquistata
                        
                        #Se ho prodotti popolari non acquistati dall'utente
                        if len(popular_ord) > 0:
                            ctx= {"listaprodotti": popular_ord,'title':"Prodotti popolari:"} #listaprodotti contiene i prodotti più popolari

                        #Se non ho prodotti popolari non acquistati dall'utente
                        else:
                            products=all_products() #Acquisisco tutti i prodotti
                            ctx= {"listaprodotti": products,'title':"Tutti i prodotti:"} #listaprodotti contiene tutti i prodotti
                    
                    #Se non esistono acquisti fatti da altri utenti
                    else:
                        products=all_products() #Acquisisco tutti i prodotti
                        ctx= {"listaprodotti": products,'title':"Tutti i prodotti:"} #listaprodotti contiene tutti i prodotti 
            
            #Se cliente non ha fatto acquisti
            else:
                #Se esistono degli ordini di altri utenti
                if Ordine.objects.filter().exists():
                    popular={}
                    popular_ord= mostpopular(popular,request) #Acquisisco oggetti più popolari in ordine di quantità acquistata
                    ctx= {"listaprodotti": popular_ord,'title':"Prodotti popolari:"} #listaprodotti contiene i prodotti più popolari
                
                #Se non esistono ordini di altri utenti
                else:
                    products=all_products() #Acquisisco tutti i prodotti
                    ctx= {"listaprodotti": products,'title':"Tutti i prodotti:"} #listaprodotti contiene tutti i prodotti 

    #--- Se utente non è  loggato
    else:
        #Se esistono degli ordini degli utenti
        if Ordine.objects.filter().exists():
            popular={}
            popular_ord= mostpopular(popular,request) #Acquisisco oggetti più popolari in ordine di quantità acquistata
            ctx= {"listaprodotti": popular_ord,'title':"Prodotti popolari:"} #listaprodotti contiene i prodotti più popolari
        
        #Se non esistono ordini degli utenti
        else:
            products=all_products() #Acquisisco tutti i prodotti
            ctx= {"listaprodotti": products,'title':"Tutti i prodotti:"} #listaprodotti contiene tutti i prodotti 

    return render(request, template_name="home.html", context=ctx) #restituisco il template


