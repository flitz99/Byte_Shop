from django.urls import path, include
from . import views
from products.apps import ProductsConfig
from .views import *
from django.http import HttpResponse

app_name="orders"

#Urls dell'applicazione
urlpatterns = [
    #Url per la visualizzazione degli ordini di un cliente e quelli effettuati sui suoi prodotti per l'admin
    path("my_orders",my_orders,name="my_orders"), 
    #Url per la creazione di un ordine di un cliente
    path("create_order",create_order,name="create_order")

    
]