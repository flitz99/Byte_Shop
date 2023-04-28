from django.shortcuts import render, redirect
from .models import Smartphone, Computer, Product, Recensione, Televisore, Cuffie, Cover
from django.shortcuts import get_object_or_404
from django.contrib import messages
from cart.models import *
from django.views.generic.list import ListView
from django.db.models import Q
from django.contrib.auth.models import User
from orders.models import Ordine
from django.utils.timezone import datetime 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def home(request):
    return redirect('../')

def all_products(request):
        products= Product.objects.all() #prendo tutti i prodotti

        templ="products/allproducts.html"
        ctx= {"listaprodotti": products}
    
        if request.user.is_authenticated and request.user.is_staff: # Se utente è autenticato ed è amministratore
                user= request.user # acquisisco utente registrato
                products= Product.objects.filter(supplier=user.id) #prendo prodotti che hanno tale supplier
                ctx = { "listaprodotti": products}

        if not request.user.is_authenticated: #Se utente non autenticato
                products= Product.objects.all() #prendo tutti i prodotti
                ctx= {"listaprodotti": products}

        return render(request,template_name=templ,context=ctx)  

def prodotto(request,prod_code):

        if Product.objects.filter(product_code=prod_code).exists():
                templ="products/prodotto.html"
                ctx={}
                prodotto=Product.objects.get(product_code=prod_code) #Acquisisco prodotto dal product code

                #Se utente autenticato controllo se ha acquistato il prodotto in questione
                #Se il prodotto è stato acquistato, allora l'utente può lasciare una recensione
                check=False
                if request.user.is_authenticated:
                        user=User.objects.get(username=request.user) #acquisisco user

                        #Se è un cliente
                        if not request.user.is_staff:
                                client=Client.objects.get(user=user) #Dallo user acquisisco il client
                                
                                if Ordine.objects.filter(client=client).exists(): #Se utente ha effettuato ordini
                                        ordini=Ordine.objects.filter(client=client) #Prendo gli ordini fatti dall'utente
                                        for ordine in ordini:
                                            for o in ordine.prodotti.all():
                                                if o.item==prodotto: #Se utente ha acquistato questo prodotto
                                                        check=True
                                
                                #Se utente ha già recensito il prodotto (non può recensirlo più volte)
                                if Recensione.objects.filter().exists():
                                   for r in prodotto.recensioni.all():
                                      if r.client==client: 
                                          check=False
                                
                if prodotto.type=="computer": #Se è un computer
                    computer=Computer.objects.get(product_code=prod_code) #Acquisisco computer dal product code
                    ctx={"prodotto":computer,"check":check}
        
                if prodotto.type=="smartphone": # Se è uno smartphone
                    smartphone=Smartphone.objects.get(product_code=prod_code) #Acquisisco smartphone dal product code
                    ctx={"prodotto":smartphone,"check":check}
                
                if prodotto.type=="televisore": #Se è un televisore
                   televisore=Televisore.objects.get(product_code=prod_code)
                   ctx={"prodotto":televisore,"check":check}

                if prodotto.type=="cover": #Se è una cover
                    cover=Cover.objects.get(product_code=prod_code)
                    ctx={"prodotto":cover,"check":check}

                if prodotto.type=="cuffie": #Se è un paio di cuffie
                    cuffie=Cuffie.objects.get(product_code=prod_code)
                    ctx={"prodotto":cuffie,"check":check}

                
                #Quando premo pulsante "acquista" inserendo quantità
                if request.method == "POST":
                        quantity=request.POST['quantity']
                        if quantity != '':

                                q= int(quantity) #Acquisisco quantità

                                #Aggiorno carrello 
                                user=User.objects.get(username=request.user) #acquisisco user
                                client=Client.objects.get(user=user) #Dallo user acquisisco il client
                                carrello=Carrello.objects.get(user=client) #Acquisisco carrello relativo all'utente loggato

                                exists=False
                                cart_item= Carrello_Item()
                                for c in carrello.prodotti.all(): #Controllo prodotti nel carrello dell'utente loggato
                                   if c.item == prodotto: #Se prodotto in questione esiste
                                        exists=True
                                        cart_item=c #Acquisisco il prodotto nel carrello
                                
                                if exists: #Se esiste prodotto nel carrello
                                        
                                        if cart_item.quantity + q > prodotto.quantity:
                                                messages.error(request,"Raggiunta la quantità massima disponibile per questo prodotto! ")
                                        else:
                                                cart_item.quantity+=q
                                                cart_item.price=round(prodotto.final_price*cart_item.quantity,2)
                                                cart_item.save()
                                                messages.success(request, "Modificata correttamente quantità nel carrello!")

                                else:       #Se prodotto non esiste nel carrello

                                        new_cart_item=Carrello_Item()
                                        new_cart_item.item= prodotto
                                        new_cart_item.quantity=q
                                        new_cart_item.price=round(prodotto.final_price*new_cart_item.quantity,2)
                                        new_cart_item.save()
                                        
                                        carrello.prodotti.add(new_cart_item)
                                        

                                        messages.success(request, "Prodotto inserito correttamente nel carrello!")

                        else:
                                messages.error(request,"selezionare una quantità per inserire il prodotto nel carrello!")
                        

                return render(request,template_name=templ,context=ctx)
        else:
               return HttpResponse("ERROR: product_code non valido")

@login_required
def create_review(request,prod_code):
        
        if Product.objects.filter(product_code=prod_code).exists():
                templ="products/create_review.html"

                prodotto=prodotto=Product.objects.get(product_code=prod_code) #Acquisisco prodotto dal product cod
                
                user=User.objects.get(username=request.user) #acquisisco user
                client=Client.objects.get(user=user) #Dallo user acquisisco il client

                ctx={"prodotto":prodotto}

                if request.method=="POST":
                        valutation=request.POST['valutation']
                        description=request.POST['description']

                        recensione= Recensione()
                        recensione.valutation=valutation
                        recensione.description=description
                        recensione.date= datetime.today()
                        recensione.client=client
                        recensione.save()

                        prodotto.recensioni.add(recensione)

                        return redirect("../id/"+prod_code)
                
        
                return render(request,template_name=templ,context=ctx)
        else:
               return HttpResponse("ERROR: product_code non valido")


#Aggiunta nuovo Prodotto
@login_required
def add_product(request,category):
    
    if category =="computer" or category=="smartphone" or category=="televisore" or category=="cover" or category=="cuffie":
        templ="products/product_form.html"

        ctx= {"title": category}
        if request.method == "POST":

                if category=="computer":
                        c=Computer()
                        c.image= request.FILES['image']
                        c.name= request.POST['name']
                        c.type = "computer" #pongo categoria
                        c.product_code=request.POST['product_code']
                        c.productor=request.POST['productor']
                        c.color=request.POST['color']
                        c.size=request.POST['size']
                        c.weight=request.POST['weight']
                        c.full_price= float(request.POST['full_price'])
                        c.discount=float(request.POST['discount'])
                        c.quantity= int(request.POST['quantity'])
                        c.final_price=round(c.full_price-((c.full_price/100)*c.discount),2) #Calcolo prezzo finale scontato
                        c.supplier=request.user

                        c.display_size=request.POST['display_size']
                        c.display_resolution=request.POST['display_resolution']
                        c.cpu=request.POST['cpu']
                        c.ram=request.POST['ram']
                        c.disk_size=request.POST['disk_size']
                        c.disk_type=request.POST['disk_type']
                        c.operating_system=request.POST['operating_system']
                        c.graphic_card=request.POST['graphic_card']
                        c.battery_autonomy=request.POST['battery_autonomy']
                        c.additional_function=request.POST['additional_function']

                        c.save() #Salvo computer nel DB

                        # controlli aggiuntivi ......
                
                if category == "smartphone":
                        s=Smartphone()
                        s.image= request.FILES['image']
                        s.name= request.POST['name']
                        s.type = "computer" #pongo categoria
                        s.product_code=request.POST['product_code']
                        s.productor=request.POST['productor']
                        s.color=request.POST['color']
                        s.size=request.POST['size']
                        s.weight=request.POST['weight']
                        s.full_price= float(request.POST['full_price'])
                        s.discount=float(request.POST['discount'])
                        s.quantity= int(request.POST['quantity'])
                        s.final_price=round(c.full_price-((c.full_price/100)*c.discount),2) #Calcolo prezzo finale scontato
                        s.supplier=request.user

                        s.display_size=request.POST['display_size']
                        s.cpu=request.POST['cpu']
                        s.ram=request.POST['ram']
                        s.disk_size=request.POST['disk_size']
                        s.operating_system=request.POST['operating_system']
                        s.battery_autonomy=request.POST['battery_autonomy']
                        s.camera= request.POST['camera']
                        s.additional_function=request.POST['additional_function']

                        s.save() #Salvo smartphone nel database

                if category== "televisore":
                        t= Televisore()
                        t.image=request.FILES['image']
                        t.name= request.POST['name']
                        t.type = "televisore" #pongo categoria
                        t.product_code=request.POST['product_code']
                        t.productor=request.POST['productor']
                        t.color=request.POST['color']
                        t.size=request.POST['size']
                        t.weight=request.POST['weight']
                        t.full_price= float(request.POST['full_price'])
                        t.discount=float(request.POST['discount'])
                        t.quantity= int(request.POST['quantity'])
                        t.final_price=round(t.full_price-((t.full_price/100)*t.discount),2) #Calcolo prezzo finale scontato
                        t.supplier=request.user

                        t.display_size=request.POST['display_size']
                        t.display_resolution=request.POST['display_resolution']
                        t.display_technology=request.POST['display_technology']
                        t.display_quality=request.POST['display_quality']
                        t.cpu=request.POST['cpu']
                        t.frame_frequency=request.POST['frame_frequency']
                        t.reception_type=request.POST['reception_type']
                        t.additional_function=request.POST['additional_function']

                        t.save() #Salvo televisore nel database
                
                if category== "cover":
                        c= Cover()
                        c.image= request.FILES['image']
                        c.name= request.POST['name']
                        c.type = "computer" #pongo categoria
                        c.product_code=request.POST['product_code']
                        c.productor=request.POST['productor']
                        c.color=request.POST['color']
                        c.size=request.POST['size']
                        c.weight=request.POST['weight']
                        c.full_price= float(request.POST['full_price'])
                        c.discount=float(request.POST['discount'])
                        c.quantity= int(request.POST['quantity'])
                        c.final_price=round(c.full_price-((c.full_price/100)*c.discount),2) #Calcolo prezzo finale scontato
                        c.supplier=request.user

                        c.compatibilità=request.POST['compatibilità']
                        c.caratteristiche=request.POST['caratteristiche']

                        c.save() #Salvo custodia nel database

                if category== "cuffie":
                        c= Cuffie()
                        c.image= request.FILES['image']
                        c.name= request.POST['name']
                        c.type = "computer" #pongo categoria
                        c.product_code=request.POST['product_code']
                        c.productor=request.POST['productor']
                        c.color=request.POST['color']
                        c.size=request.POST['size']
                        c.weight=request.POST['weight']
                        c.full_price= float(request.POST['full_price'])
                        c.discount=float(request.POST['discount'])
                        c.quantity= int(request.POST['quantity'])
                        c.final_price=round(c.full_price-((c.full_price/100)*c.discount),2) #Calcolo prezzo finale scontato
                        c.supplier=request.user

                        c.cuffie_type=request.POST['cuffie_type']
                        c.caratteristiche=request.POST['caratteristiche']

                        c.save() #Salvo cuffie nel database

                messages.success(request, "Prodotto inserito correttamente!")

        return render(request,template_name=templ,context=ctx)
    
    else:
        return HttpResponse("ERROR: categoria non valida")

@login_required
def delete_product(request,prod_code):

        if Product.objects.filter(product_code=prod_code).exists():
                product = get_object_or_404(Product, product_code=prod_code) 
                product.delete() #elimina oggetto dal db

                return redirect("../allproducts")
        else:
               return HttpResponse("ERROR: product_code non valido")

@login_required
def update_product(request,prod_code):

        if Product.objects.filter(product_code=prod_code).exists():
                templ="products/update_product.html"
                ctx={}

                p= Product.objects.get(product_code=prod_code) 

                if p.type == "computer":
                        c= Computer.objects.get(product_code=prod_code)
                        ctx={ "prodotto":c}

                        if request.method=="POST":
                        
                                c.image = request.FILES.get('image',c.image)
                                c.name= request.POST.get('name',c.name)
                                c.product_code=request.POST.get('product_code',c.product_code)
                                c.productor=request.POST.get('productor',c.productor)
                                c.color=request.POST.get('color',c.color)
                                c.size=request.POST.get('size',c.size)
                                c.weight=request.POST.get('weight',c.weight)
                                c.full_price= float(request.POST.get('full_price',c.full_price))
                                c.discount= float(request.POST.get('discount',c.discount))
                                c.quantity= int(request.POST.get('quantity',c.quantity))
                                
                                c.final_price=round(c.full_price-((c.full_price/100)*c.discount),2) #Calcolo prezzo finale scontato

                                c.display_size=request.POST.get('display_size',c.display_size)
                                c.display_resolution=request.POST.get('display_resolution',c.display_resolution)
                                c.cpu=request.POST.get('cpu',c.cpu)
                                c.ram=request.POST.get('ram',c.ram)
                                c.disk_size=request.POST.get('disk_size',c.disk_size)
                                c.disk_type=request.POST.get('disk_type',c.disk_type)
                                c.operating_system=request.POST.get('operating_system',c.operating_system)
                                c.graphic_card=request.POST.get('graphic_card',c.graphic_card)
                                c.battery_autonomy=request.POST.get('battery_autonomy',c.battery_autonomy)
                                c.additional_function=request.POST.get('additional_function',c.additional_function)
                                c.save()      

                                messages.success(request, "Prodotto computer aggiornato correttamente.")    
                        
                if p.type == "smartphone":
                        s= Smartphone.objects.get(product_code=prod_code)
                        ctx={ "prodotto":s }

                        if request.method=="POST":      

                                s.image = request.FILES.get('image',s.image)
                                s.name= request.POST.get('name',s.name)
                                s.product_code=request.POST.get('product_code',s.product_code)
                                s.productor=request.POST.get('productor',s.productor)
                                s.color=request.POST.get('color',s.color)
                                s.size=request.POST.get('size',s.size)
                                s.weight=request.POST.get('weight',s.weight)
                                s.full_price= float(request.POST.get('full_price',s.full_price))
                                s.discount= float(request.POST.get('discount',s.discount))
                                s.quantity= int(request.POST.get('quantity',s.quantity))
                                
                                s.final_price=round(s.full_price-((s.full_price/100)*s.discount),2) #Calcolo prezzo finale scontato
                                s.display_size=request.POST.get('display_size',s.display_size)
                                s.cpu=request.POST.get('cpu',s.cpu)
                                s.ram=request.POST.get('ram',s.ram)
                                s.disk_size=request.POST.get('disk_size',s.disk_size)
                                s.operating_system=request.POST.get('operating_system',s.operating_system)
                                s.battery_autonomy=request.POST.get('battery_autonomy',s.battery_autonomy)
                                s.camera= request.POST.get('camera',s.camera)
                                s.additional_function=request.POST.get('additional_function',s.additional_function)
                                s.save()

                        
                                messages.success(request, "Prodotto smartphone aggiornato correttamente.")

                if p.type == "televisore":
                        t =Televisore.objects.get(product_code=prod_code)
                        ctx={"prodotto":t }

                        if request.method =="POST":
                                t.image = request.FILES.get('image',t.image)
                                t.name= request.POST.get('name',t.name)
                                t.product_code=request.POST.get('product_code',t.product_code)
                                t.productor=request.POST.get('productor',t.productor)
                                t.color=request.POST.get('color',t.color)
                                t.size=request.POST.get('size',t.size)
                                t.weight=request.POST.get('weight',t.weight)
                                t.full_price= float(request.POST.get('full_price',t.full_price))
                                t.discount= float(request.POST.get('discount',t.discount))
                                t.quantity= int(request.POST.get('quantity',t.quantity))

                                t.display_size=request.POST.get('display_size',t.display_size)
                                t.display_resolution=request.POST.get("display_resolution",t.display_resolution)
                                t.display_technology=request.POST.get("display_technology",t.display_technology)
                                t.display_quality=request.POST.get("display_quality",t.display_quality)
                                t.cpu=request.POST.get("cpu",t.cpu)
                                t.frame_frequency=int(request.POST.get("frame_frequency",t.frame_frequency))
                                t.reception_type=request.POST.get("reception_type",t.reception_type)
                                t.additional_function=request.POST.get("additional_function",t.additional_function)
                                t.save()
                                
                                messages.success(request, "Prodotto televisore aggiornato correttamente.")
                
                if p.type == "cover":
                        c = Cover.objects.get(product_code=prod_code)
                        ctx={"prodotto":c}

                        if request.method == "POST":
                                c.image = request.FILES.get('image',c.image)
                                c.name= request.POST.get('name',c.name)
                                c.product_code=request.POST.get('product_code',c.product_code)
                                c.productor=request.POST.get('productor',c.productor)
                                c.color=request.POST.get('color',c.color)
                                c.size=request.POST.get('size',c.size)
                                c.weight=request.POST.get('weight',c.weight)
                                c.full_price= float(request.POST.get('full_price',c.full_price))
                                c.discount= float(request.POST.get('discount',c.discount))
                                c.quantity= int(request.POST.get('quantity',c.quantity))

                                c.compatibilità=request.POST.get("compatibilità",c.compatibilità)
                                c.caratteristiche=request.POST.get("caratteristiche",c.caratteristiche)
                                c.save()

                                messages.success(request, "Prodotto cover aggiornato correttamente.")
                
                if p.type=="cuffie":
                        c=Cuffie.objects.get(product_code=prod_code)
                        ctx={"prodotto":c}

                        if request.method== "POST":
                                c.image = request.FILES.get('image',c.image)
                                c.name= request.POST.get('name',c.name)
                                c.product_code=request.POST.get('product_code',c.product_code)
                                c.productor=request.POST.get('productor',c.productor)
                                c.color=request.POST.get('color',c.color)
                                c.size=request.POST.get('size',c.size)
                                c.weight=request.POST.get('weight',c.weight)
                                c.full_price= float(request.POST.get('full_price',c.full_price))
                                c.discount= float(request.POST.get('discount',c.discount))
                                c.quantity= int(request.POST.get('quantity',c.quantity))

                                c.cuffie_type=request.POST.get("cuffie_type",c.cuffie_type)
                                c.caratteristiche=request.POST.get("caratteristiche",c.caratteristiche)
                                c.save()

                                messages.success(request, "Prodotto cuffie aggiornato correttamente.")

                return render(request,template_name=templ,context=ctx)
        else:
               return HttpResponse("ERROR: product_code non valido")

class SearchView(ListView):
    model = Product
    template_name = 'products/search.html'
    context_object_name = 'listaricerca'

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = Product.objects.filter(
                  Q(name__contains=query) | Q(type=query) | Q(product_code=query) | Q(productor__contains=query) | Q(color__contains=query)
            )
            result = postresult
        else:
            result = None
        return result

