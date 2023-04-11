from django.shortcuts import render
from django.shortcuts import render, redirect

def home(request):
    return redirect('../')

def add_cart_item(request,category):
    
    templ="cart/product_form.html"

    ctx= {"title": category}

'''Creo ordine:
    path("<str:prod_code>",add_cart_item,name="aggiunta prodotto"), #Scheda tecnica del prodotto

    #Genero codice ordine
    length_of_string = 8
    order_code=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))

    date= datetime.date.today()
    cliente= request.user
    
    #order=Ordine.objects.create(id_ordine=order_code,date=date,product=product,client=cliente,quantity=q)
    #order.save()

'''

