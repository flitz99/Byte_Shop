from django.urls import path, include
from . import views
from products.apps import ProductsConfig
from .views import *
from django.http import HttpResponse

app_name="orders"

urlpatterns = [
    path("my_orders",my_orders,name="my_orders"), #ordini di un cliente
    path("create_order",create_order,name="create_order") #Funzione per la creazione di un nuovo ordine

    
]