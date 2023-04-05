from http.client import HTTPResponse
from re import template
from django.shortcuts import render, redirect
from .models import Smartphone, Computer, Product, Ordine, Recensione
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django.contrib import messages
import string
import random
import datetime

def home(request):
    return redirect('../')

def categoria_prodotto(request,category):
       if category=="computer" or category=="smartphone":
                templ="products/categoria_prodotto.html"
        
                products = Product.objects.filter(type=category)

                ctx={"listaprodotti":products,
             "category":category
                }
        
                return render(request,template_name=templ,context=ctx)
       else:
                return HTTPResponse("ERROR: page not found")

def prodotto(request,prod_code):

        templ="products/prodotto.html"
        ctx={}
        
        product= Product.objects.get(product_code=prod_code)     

        if product.type=="computer": # Se è un computer
                computer=Computer.objects.get(product_id=product.id)
                ctx={"prodotto":computer}

        if product.type=="smartphone": # Se è uno smartphone
                smartphone=Smartphone.objects.get(product_id=product.id)
                ctx={"prodotto":smartphone}
        
        #Quando premo pulsante "acquista" inserendo quantità
        if request.method == "POST":
                quantity=request.POST['quantity']
                if quantity != '':
                        q=int(quantity)
                        #Genero codice ordine
                        length_of_string = 8
                        order_code=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))

                        date= datetime.date.today()
                        cliente= request.user
                        
                        order=Ordine.objects.create(id_ordine=order_code,date=date,product=product,client=cliente,quantity=q)
                        order.save()

                        #Decremento quantità per quel prodotto
                        product.quantity=product.quantity-q
                        if product.quantity == 0: #Se quantità è diventata zero
                                product.available=False

                        order.save() #Aggiungo ordine
                        product.save() #Aggiungo modifiche al prodotto ( quantità diminuita )

                        messages.success(request, "Ordine effettuato correttamente")

                else:
                        messages.error(request,"Inserire una quantità per effettuare l'acquisto!")
                

        return render(request,template_name=templ,context=ctx)

def orders(request,client_id):

        templ="products/orders.html"

        lista_ordini=Ordine.objects.filter(client_id=client_id) #Acquisisco lista ordini per dato cliente

        ctx={"client":client_id, "listaordini":lista_ordini}

        return render(request,template_name=templ,context=ctx)
        
#Aggiunta nuovo Product di tipo Computer
def add_product(request,category):
    
    templ="products/product_form.html"

    ctx= {"title": category}
    if request.method == "POST":

        image= request.FILES['image']
        name= request.POST['name']
        type = category #pongo categoria
        product_code=request.POST['product_code']
        productor=request.POST['productor']
        color=request.POST['color']
        size=request.POST['size']
        weight=request.POST['weight']
        price= request.POST['price']
        quantity= int(request.POST['quantity'])

        if quantity>0:
                available=True 
        else:
                available=False
        # controlli aggiuntivi ......

        prod = Product.objects.create(image=image,name=name,product_code=product_code,productor=productor,color=color,size=size,weight=weight,price=price,available=available,supplier=request.user, type=type,quantity=quantity)
        prod.save()

        if category == "computer":
        
                display_size=request.POST['display_size']
                display_resolution=request.POST['display_resolution']
                cpu=request.POST['cpu']
                ram=request.POST['ram']
                disk_size=request.POST['disk_size']
                disk_type=request.POST['disk_type']
                operating_system=request.POST['operating_system']
                graphic_card=request.POST['graphic_card']
                battery_autonomy=request.POST['battery_autonomy']
                additional_function=request.POST['additional_function']

                computer= Computer.objects.create(product=prod,display_size=display_size,display_resolution=display_resolution,cpu=cpu,ram=ram,disk_size=disk_size,disk_type=disk_type,operating_system=operating_system,graphic_card=graphic_card,battery_autonomy=battery_autonomy,additional_function=additional_function)
                computer.save()

        if category == "smartphone":
        
                display_size=request.POST['display_size']
                cpu=request.POST['cpu']
                ram=request.POST['ram']
                disk_size=request.POST['disk_size']
                operating_system=request.POST['operating_system']
                battery_autonomy=request.POST['battery_autonomy']
                camera= request.POST['camera']
                additional_function=request.POST['additional_function']

                smartphone= Smartphone.objects.create(product=prod,display_size=display_size,cpu=cpu,ram=ram,disk_size=disk_size,operating_system=operating_system,battery_autonomy=battery_autonomy,camera=camera,additional_function=additional_function)
                smartphone.save()


        return redirect('home')

    return render(request,template_name=templ,context=ctx)

def delete_product(request,id):

        product = get_object_or_404(Product, id=id)
        product.delete() #elimina oggetto dal db

        return redirect('home')


def update_product(request,id):
        templ="products/update_product.html"
        ctx={}

        product= Product.objects.get(id=id) 
        if product.type == "computer":
                computer= Computer.objects.get(product_id=id)
                ctx={   "prodotto":product,
                        "computer":computer}
        if product.type == "smartphone":
                smartphone= Smartphone.objects.get(product_id=id)
                ctx={   "prodotto":product,
                        "smartphone":smartphone}

        if request.method=="POST":

                product.image = request.FILES.get('image',product.image)
                
                
                product.name= request.POST.get('name',product.name)
                product.product_code=request.POST.get('product_code',product.product_code)
                product.productor=request.POST.get('productor',product.productor)
                product.color=request.POST.get('color',product.color)
                product.size=request.POST.get('size',product.size)
                product.weight=request.POST.get('weight',product.weight)
                product.price= request.POST.get('price',product.price)

                quantity= int(request.POST.get('quantity',product.quantity))
                if quantity>0:
                        product.available=True 
                else:
                        product.available=False
                product.quantity=quantity
                
                product.save()
                

                if product.type == "computer":
                
                        computer.display_size=request.POST.get('display_size',computer.display_size)
                        computer.display_resolution=request.POST.get('display_resolution',computer.display_resolution)
                        computer.cpu=request.POST.get('cpu',computer.cpu)
                        computer.ram=request.POST.get('ram',computer.ram)
                        computer.disk_size=request.POST.get('disk_size',computer.disk_size)
                        computer.disk_type=request.POST.get('disk_type',computer.disk_type)
                        computer.operating_system=request.POST.get('operating_system',computer.operating_system)
                        computer.graphic_card=request.POST.get('graphic_card',computer.graphic_card)
                        computer.battery_autonomy=request.POST.get('battery_autonomy',computer.battery_autonomy)
                        computer.additional_function=request.POST.get('additional_function',computer.additional_function)
                        computer.save()

                if product.type =="smartphone":

                        smartphone.display_size=request.POST.get('display_size',smartphone.display_size)
                        smartphone.cpu=request.POST.get('cpu',smartphone.cpu)
                        smartphone.ram=request.POST.get('ram',smartphone.ram)
                        smartphone.disk_size=request.POST.get('disk_size',smartphone.disk_size)
                        smartphone.operating_system=request.POST.get('operating_system',smartphone.operating_system)
                        smartphone.battery_autonomy=request.POST.get('battery_autonomy',smartphone.battery_autonomy)
                        smartphone.camera= request.POST.get('camera',smartphone.camera)
                        smartphone.additional_function=request.POST.get('additional_function',smartphone.additional_function)
                        smartphone.save()

                return redirect('home')

        return render(request,template_name=templ,context=ctx)