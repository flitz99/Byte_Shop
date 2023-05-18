from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Client
from cart.models import *
from orders.views import svuota_carrello
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import *
import re

#Createview per la registrazione degli utenti clienti e admin
class SignupCreateView(CreateView):
    template_name="authentication/signup.html"
    success_url= reverse_lazy('authentication:signin',kwargs={'user_type':None})

    #Scelta del form da utilizzare
    def get_form_class(self):
        user_type = self.kwargs.get('user_type')
        if user_type == 'admin':
            return CustomUserCreationForm
        elif user_type=='client':
            return ClientCreationForm
        else:
            raise Http404("Tipologia di utente non valida")  
    
    #Se il form è valido
    def form_valid(self,form):
        user_type = self.kwargs.get('user_type')

        if user_type == 'client':
            User = get_user_model()
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_staff=False
            user.save()
            client = Client.objects.create(
                user=user,
                profile_image=form.cleaned_data['profile_image'],
                telephone=form.cleaned_data['telephone'],
                address=form.cleaned_data['address'],
                house_number=form.cleaned_data['house_number'],
                city=form.cleaned_data['city'],
                province=form.cleaned_data['province'],
                birth_date=form.cleaned_data['birth_date'],
                cap=form.cleaned_data['cap'],
            )
            
            client.save()

            #Creazione carrello del cliente
            carrello= Carrello()
            carrello.user=client
            carrello.save()
            self.success_url = reverse_lazy("authentication:signin", kwargs={'user_type': "client"}) #Redireziono al login da cliente

        elif user_type == 'admin':
            User = get_user_model()
            user = form.save(commit=False)
            user.is_staff=True
            user.is_superuser=True
            user.set_password(form.cleaned_data['password1'])

            user.save()
            self.success_url = reverse_lazy("authentication:signin", kwargs={'user_type': "admin"}) #Redireziono al login da cliente

        return super().form_valid(form)
    
    #Modifica delle variabili di context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['user_type'] #Introduco ctx con tipo utente
        return context          

#View per il login degli utenti clienti e admin
def signin(request,user_type):
 
 if user_type=="admin" or user_type=="client": #check in modo che non si inserisca <str:user_type> diverso da client o admin
    templ="authentication/signin.html"
    ctx={"title":user_type}

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)

        #Se utente admin 
        if user is not None and user_type=="admin" and user.is_staff==True:
            login(request, user)
            return redirect('home')
        
        #Se utente cliente
        elif user is not None and user_type=="client" and user.is_staff==False:
            login(request, user)
            return redirect('home')
        else: 
            messages.error(request, "Credenziali errate!") 
            return redirect("authentication:signin",user_type)
    
    return render(request,template_name=templ,context=ctx)
 else:
    raise Http404("Tipologia di utente non valida") 
 
        
#View per la modifica dei dati degli utenti admin e client
@login_required
def profile(request):
    templ="authentication/profile.html"
    user= request.user
    ctx={"user":user}
    
    if user.is_staff == False: #Se utente cliente
        client= Client.objects.get(user_id=user.id)
        ctx={"user":user,
            "client":client
        }
    
    if request.method =='POST':
        
        username = request.POST.get('username',user.username)
        fname = request.POST.get('fname',user.first_name)
        lname = request.POST.get('lname',user.last_name)
        email = request.POST.get('email',user.email)   # DA FARE PASSWORD

        #--- Controlli dati dello User ---
        #Controlle se username già presente
        if username != user.username and User.objects.filter(username=username):
            messages.error(request, "Username già presente, provare con un altro.")
            return redirect('authentication:profile')
        
        #Controllo se email già presente
        if email != user.email and User.objects.filter(email=email).exists():
            messages.error(request, "Email già registrata! Inserirne un altra!")
            return redirect('authentication:profile')
        
        #Controllo che nome  e cognome siano composti solo da caratteri
        if (not re.match(r'^[a-zA-Z\s]+$', fname)) or (not re.match(r'^[a-zA-Z\s]+$', lname)):
            messages.error(request, "Il nome e il cognome devono contenere solo caratteri.")
            return redirect('authentication:profile')

        user.username=username
        user.email=email
        user.first_name=fname
        user.last_name=lname
        user.save()

        user.save() #Salvo lo user nel DB

        if user.is_staff==False: # Se cliente
            image= request.FILES.get('image',client.profile_image)
            birth_date=request.POST.get('birth_date',client.birth_date)
            telephone = request.POST.get('telephone',client.telephone)
            address = request.POST.get('address',client.address)
            house_number=request.POST.get('house_number',client.house_number)
            city = request.POST.get('city',client.city)
            province = request.POST.get('province',client.province)
            cap = request.POST.get('cap',client.cap)

            #--- Controlli dati del client ---
            #Controllo che la città non contenga numeri
            if any(char.isdigit() for char in city):
                messages.error(request,"La città può contenere solo caratteri.")
                return redirect('authentication:profile')
            
            #Controllo che provincia non contenga numeri
            if any(char.isdigit() for char in province):
                messages.error(request, "La provincia può contenere solo caratteri.")
                return redirect('authentication:profile')
            
            client.profile_image=image
            client.birth_date=birth_date
            client.telephone=telephone
            client.address=address
            client.house_number=house_number
            client.city=city
            client.province=province
            client.cap=cap
            client.save()
            
            client.save() #Salvo il cliente nel DB

        messages.success(request, "Account aggiornato correttamente!")
        return redirect ("authentication:profile")
        
    return render(request,template_name=templ,context=ctx)

#Mostra gli utenti clienti registrati all'amministratore
@login_required
def users(request):
    templ="authentication/users.html"
    clients=Client.objects.all()

    ctx={"listaclients":clients}

    return render(request,template_name=templ,context=ctx)

#Eliminazione degli utenti clienti da parte degli amministratori
@login_required
def delete_user(request,user_id):
    
    if Client.objects.filter(id=user_id).exists(): #Controllo che lo user id passato esista
        client = get_object_or_404(Client, id=user_id)
        user= get_object_or_404(User,id=client.user_id)
        client.delete() #elimina oggetto dal db
        user.delete()
     
        return redirect('authentication:users')
    
    else:
        return HttpResponse("ERROR: user_id non valido")

#Form per il cambio della password
@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'La password è stata cambiata con successo.')
            update_session_auth_hash(request, user)  # Aggiorna l'hash della sessione per evitare il logout automatico
            return redirect('authentication:profile')  # Redirigi l'utente alla home page dopo il cambio password
        else:
            messages.error(request, 'Si è verificato un errore. Correggi i seguenti errori:')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'authentication/change_pswd.html', {'form': form})

#Logout degli utenti (clienti e admin)
@login_required
def signout(request):

    user=User.objects.get(username=request.user) #acquisisco user

    #Se utente cliente svuoto il carrello
    if user.is_staff == False:
        client=Client.objects.get(user=user) #acquisisco client
        carrello=Carrello.objects.get(user=client) #Acquisisco carrello relativo all'utente loggato
        svuota_carrello(carrello)

    logout(request)
    return redirect('home')

