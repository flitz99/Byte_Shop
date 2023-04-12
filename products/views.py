from django.shortcuts import render, redirect
from .models import Smartphone, Computer, Product
from django.shortcuts import get_object_or_404
from django.contrib import messages
from cart.models import *
from django.views.generic.list import ListView
from django.db.models import Q
from django.contrib.auth.models import User

def home(request):
    return redirect('../')

def prodotto(request,prod_code):

        templ="products/prodotto.html"
        ctx={}
        prodotto=Product.objects.get(product_code=prod_code) #Acquisisco prodotto dal product code

        if prodotto.type=="computer": #Se è un computer
                computer=Computer.objects.get(product_code=prod_code) #Acquisisco computer dal product code
                ctx={"prodotto":computer}
    
        if prodotto.type=="smartphone": # Se è uno smartphone
                smartphone=Smartphone.objects.get(product_code=prod_code) #Acquisisco smartphone dal product code
                ctx={"prodotto":smartphone}
        
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
        
#Aggiunta nuovo Prodotto
def add_product(request,category):
    
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

        return redirect('home')

    return render(request,template_name=templ,context=ctx)

def delete_product(request,prod_code):

        product = get_object_or_404(Product, product_code=prod_code) 
        product.delete() #elimina oggetto dal db

        return redirect('home')

def update_product(request,prod_code):

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

                        return redirect('home')     
                  
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

                
                        return redirect('home')

        return render(request,template_name=templ,context=ctx)

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

