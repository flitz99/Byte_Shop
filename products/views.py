from typing import Any, Dict
from django.shortcuts import render, redirect
from .models import Smartphone, Computer, Product, Recensione, Televisore, Cuffie, Cover
from django.shortcuts import get_object_or_404
from django.contrib import messages
from cart.models import *
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.db.models import Q
from django.contrib.auth.models import User
from orders.models import Ordine
from django.utils.timezone import datetime 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import *
from django.views.generic.edit import UpdateView
from django.http import Http404

class AllProductsListView(ListView):
      model=Product
      template_name="products/allproducts.html"
      context_object_name='listaprodotti'

      def get_queryset(self):
            queryset=super().get_queryset()
            if self.request.user.is_authenticated and self.request.user.is_staff:
                queryset=queryset.filter(supplier=self.request.user.id) #Acquisisco tutti i prodotti inseriti da quel fornitore
                return queryset
            else:
                queryset=queryset.all() #Acquisisco tutti i prodotti
                return queryset 

@login_required
def delete_product(request,prod_code):

        if Product.objects.filter(product_code=prod_code).exists():
                product = get_object_or_404(Product, product_code=prod_code) 
                product.delete() #elimina oggetto dal db

                return redirect("../allproducts")
        else:
               return HttpResponse("ERROR: product_code non valido")


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

                #Controllo tipologia di prodotto      
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
        
#ci vuole login_required
class RecensioneCreateView(CreateView):
       model=Recensione
       form_class=RecensioneForm
       template_name="products/create_review.html"
       success_url = reverse_lazy("products:prodotto", kwargs={'product_code': None})  #product_code aggiunto in seguito
       
       #controlla validità dei campi del form
       def form_valid(self,form):
              recensione=form.save(commit=False)
              recensione.date=datetime.today()
              user=User.objects.get(username=self.request.user) #acquisisco user
              client=Client.objects.get(user=user) #Dallo user acquisisco il client
              recensione.client=client
              recensione.save()

              #Aggiungo recensione al prodotto
              prod_code=self.kwargs['prod_code']
              product=Product.objects.get(product_code=prod_code)
              product.recensioni.add(recensione)
              
              self.success_url = reverse_lazy("products:prodotto", kwargs={'prod_code': product.product_code}) #Redireziono al prodotto
              return super().form_valid(form)
       
       #Aggiunge il prodotto alle variabili di contesto
       def get_context_data(self, **kwargs):
              context=super().get_context_data(**kwargs)
              prod_code=self.kwargs['prod_code']
              product=Product.objects.get(product_code=prod_code)
              context['prodotto']=product
              return context
       
       
       #Restituisce 404 se prodotto non trovato
       def dispatch(self, request, *args, **kwargs):
              prod_code = self.kwargs['prod_code']
              prodotto = get_object_or_404(Product, product_code=prod_code)
              return super().dispatch(request, prodotto=prodotto, *args, **kwargs)

#ci va login required   
class ProductCreateView(CreateView):
    model = Product
    template_name = 'products/product_form.html'
    success_url = reverse_lazy("products:all_products")
    
    def get_context_data(self, **kwargs):
        category = self.kwargs['category']
        context = super().get_context_data(**kwargs)
        context['title'] = category
        return context

    def get_form_class(self):
        category = self.kwargs['category']
        if category == "computer":
            return ComputerForm
        elif category == "smartphone":
            return SmartphoneForm
        elif category == "televisore":
            return TelevisoreForm
        elif category == "cover":
            return CoverForm
        elif category == "cuffie":
            return CuffieForm   
        else:
            raise Http404("Categoria non valida")  
        
    def form_valid(self,form):
        prodotto=form.save(commit=False)
        prodotto.type=self.kwargs['category']
        prodotto.final_price=round(prodotto.full_price-((prodotto.full_price/100)*prodotto.discount),2) #Calcolo prezzo finale scontato
        prodotto.supplier=self.request.user
        prodotto.save()
        return super().form_valid(form)

#Ci va login required
class ProductUpdateView(UpdateView):
        model= None
        template_name="products/update_product.html"
        success_url= reverse_lazy('products:update_product',kwargs={'prod_code': None})
        slug_field='product_code'
        slug_url_kwarg='prod_code'

       #Per usare il prod code 
        def get_object(self,queryset=None):
                prod_code=self.kwargs.get(self.slug_url_kwarg)
                product=self.get_prodotto(prod_code)
                self.model=type(product)
                return product
       
        def get_prodotto(self, prod_code):
           try:
                product= Product.objects.get(product_code=prod_code)
                categoria=product.type
                if categoria=="computer":
                      product= Computer.objects.get(product_code=prod_code)
                elif categoria=="smartphone":
                      product= Smartphone.objects.get(product_code=prod_code)
                elif categoria=="televisore":
                      product= Televisore.objects.get(product_code=prod_code)
                elif categoria=="cover":
                      product = Cover.objects.get(product_code=prod_code)
                elif categoria=="cuffie":
                      product=Cuffie.objects.get(product_code=prod_code)
           except Product.DoesNotExist: 
                raise Http404("Il prodotto con il codice %s non esiste." %prod_code)
           return product
       
        def get_form_class(self):
           categoria= self.object.type
           if categoria=="computer":
                return ComputerForm
           elif categoria=="smartphone":
                return SmartphoneForm
           elif categoria=="televisore":
                return TelevisoreForm
           elif categoria=="cover":
                return CoverForm
           elif categoria=="cuffie":
                return CuffieForm
           else:
                raise Http404("Categoria memorizzata nel prodotto non valida") 
        
        def get_context_data(self, **kwargs):
                prod_code = self.kwargs['prod_code']
                context = super().get_context_data(**kwargs)
                prodotto=self.get_prodotto(prod_code)
                context['prodotto']=prodotto
                self.object=prodotto
                FormClass = self.get_form_class()
                context['form']=FormClass(instance=prodotto)
                return context

       
        def form_valid(self,form,**kwargs):
            prodotto=form.save(commit=False)
            prodotto.final_price=round(prodotto.full_price-((prodotto.full_price/100)*prodotto.discount),2) #Calcolo prezzo finale scontato
            prodotto.save()
            
            prod_code=self.kwargs['prod_code']
            product=Product.objects.get(product_code=prod_code)
            messages.success(self.request, "Dati prodotto aggiornati correttamente!")
            self.success_url = reverse_lazy("products:update_product", kwargs={'prod_code': product.product_code}) 
            
            return super().form_valid(form)
                    

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

