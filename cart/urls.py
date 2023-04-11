from .views import *
from django.urls import path, include

app_name="cart"

urlpatterns = [
    path("<str:prod_code>",add_cart_item,name="aggiunta prodotto"), #Scheda tecnica del prodotto
    
]