from .views import *
from django.urls import path, include

app_name="cart"

urlpatterns = [
    path("carrello",carrello,name="carrello"), #Scheda tecnica del prodotto
    path("delete_item/<str:prod_code>",delete_item,name="delete_item") #cancella item dal carrello
]