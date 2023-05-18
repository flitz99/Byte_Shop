from .views import *
from django.urls import path

app_name="cart"

#Urls dell'applicazione
urlpatterns = [
    #Url per la visualizzazione dei prodotti nel carrello
    path("carrello",carrello,name="carrello"), 
    #Url per la rimozione di un prodotto dal carrello
    path("delete_item/<str:prod_code>",delete_item,name="delete_item") 
]