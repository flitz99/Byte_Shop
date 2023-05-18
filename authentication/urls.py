from django.urls import path, include
from . import views
from .views import *

app_name="authentication"

#Url dell'applicazione
urlpatterns = [

    #Url per il logout di clienti e admin
    path('signout', views.signout, name='signout'),
    #Url per la registrazione di clienti e admin
    path('<str:user_type>/signup',SignupCreateView.as_view(),name="signup"),
    #Url per il login di clienti e admin
    path('<str:user_type>/signin',views.signin,name="signin"),
    #Url per la gestione dei clienti registrati da parte dell'admin
    path('users',views.users,name="users"),
    #Url per la cancellazione degli utenti clienti
    path('delete_user/<str:user_id>',views.delete_user,name="delete_user"),
    #Url per la modifica dei dati di un utente cliente o admin
    path('profile',views.profile,name="profile"),
    #Url per il cambio della password
    path('profile/change_password',views.change_password,name="change_password")
]
