from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Client
from django.shortcuts import get_object_or_404
from cart.models import *

# Create your views here.
def home(request):
    return redirect('../')

def signup(request,user_type):
 if user_type=="admin" or user_type=="client": #check in modo che non si inserisca <str:user_type> diverso da client o admin

    templ="authentication/signup.html"
    ctx={"title":user_type}

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username già presente, provare con un altro.")
            return redirect('signup',user_type)
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email già registrata! Inserirne un altra!")
            return redirect('signup',user_type)
        
        if len(username)>20:
            messages.error(request, "Lo username deve avere meno di 20 caratteri!")
            return redirect('signup',user_type)
        
        if pass1 != pass2:
            messages.error(request, "Le password inserite non corrispondono!")
            return redirect('signup',user_type)
        
        if not username.isalnum():
            messages.error(request, "Lo username deve essere alfanumerico!")
            return redirect('signup',user_type)

        # Se tutti i controlli passati, creo l'utente   
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.is_active = True

        if user_type=="client": # Se cliente imposto check staff a False
            myuser.is_staff=False
        else:
            myuser.is_staff=True
            myuser.is_superuser=True

        myuser.save() #Salvo su database l'utente

        if user_type=="client":  # Se utente cliente prendo campi aggiuntivi
            birth_date=request.POST['birth_date']
            telephone = request.POST['telephone']
            address = request.POST['address']
            house_number=request.POST['house_number']
            city = request.POST['city']
            province = request.POST['province']
            cap = request.POST['cap']
            
            #Creo dato cliente
            myclient= Client(user=myuser,telephone=telephone,address=address,house_number=house_number,city=city,province=province,cap=cap,birth_date=birth_date)
            myclient.save() # salvo sul database il cliente

            #Creo carrello per utente cliente
            carrello= Carrello()
            carrello.user=myclient
            carrello.save()

        messages.success(request, "il tuo account è stato creato correttamente!")
        
        return redirect('signin',user_type)
 
    return render(request,template_name=templ,context=ctx)
 else:
    return HttpResponse("ERROR: Page not found")


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

        if username != user.username and User.objects.filter(username=username):
            messages.error(request, "Username già presente, provare con un altro.")
            return redirect('profile')
        
        if email != user.email and User.objects.filter(email=email).exists():
            messages.error(request, "Email già registrata! Inserirne un altra!")
            return redirect('profile')
        
        if len(username)>20:
            messages.error(request, "Lo username deve avere meno di 20 caratteri!")
            return redirect('profile')

        if not username.isalnum():
            messages.error(request, "Lo username deve essere alfanumerico!")
            return redirect('profile')

        user.username=username
        user.email=email
        user.first_name=fname
        user.last_name=lname
        user.save()

        if user.is_staff==False:
            image= request.FILES.get('image',client.profile_image)
            birth_date=request.POST.get('birth_date',client.birth_date)
            telephone = request.POST.get('telephone',client.telephone)
            address = request.POST.get('address',client.address)
            house_number=request.POST.get('house_number',client.house_number)
            city = request.POST.get('city',client.city)
            province = request.POST.get('province',client.province)
            cap = request.POST.get('cap',client.cap)

            client.profile_image=image
            client.birth_date=birth_date
            client.telephone=telephone
            client.address=address
            client.house_number=house_number
            client.city=city
            client.province=province
            client.cap=cap
            client.save()

        messages.success(request, "Account aggiornato correttamente!")
        return redirect ("profile")
        

    return render(request,template_name=templ,context=ctx)


def signout(request):
    logout(request)
    return redirect('home')

def signin(request,user_type):
 if user_type=="admin" or user_type=="client": #check in modo che non si inserisca <str:user_type> diverso da client o admin
    templ="authentication/signin.html"
    ctx={"title":user_type}

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)

        if user is not None and user_type=="admin" and user.is_staff==True:
            login(request, user)
            # messages.success(request, "Logged In Sucessfully!!")
            return redirect('home')
        elif user is not None and user_type=="client" and user.is_staff==False:
            login(request, user)
            # messages.success(request, "Logged In Sucessfully!!")
            return redirect('home')
        else:
            messages.error(request, "Credenziali errate!")
            return redirect("signin",user_type)
    
    return render(request,template_name=templ,context=ctx)
 else:
    return HttpResponse("ERROR: Page not found")

def users(request):
    templ="authentication/users.html"
    clients=Client.objects.all()

    ctx={"listaclients":clients}

    return render(request,template_name=templ,context=ctx)

def delete_user(request,user_id):
    
     client = get_object_or_404(Client, id=user_id)
     user= get_object_or_404(User,id=client.user_id)
     client.delete() #elimina oggetto dal db
     user.delete()
     
     return redirect('home')

def change_password(request):
    templ="authentication/change_pswd.html"
    user= request.user
    ctx={"user":user}

    if request.method == "POST":
        oldpassword= request.POST['oldpassword']
        newpassword= request.POST['newpassword1']
        newpassword2= request.POST['newpassword2']

        if user.check_password(oldpassword):
            if newpassword == newpassword2:
                user.set_password(newpassword2)
                user.save()
                print(newpassword2)
                logout(request)
                return redirect('home')
            else:
                messages.error(request, "Le due password non coincidono!")
                return redirect("change_password")
        else:
            messages.error(request, "Password vecchia errata!")
            return redirect("change_password")


    return render(request,template_name=templ,context=ctx)
