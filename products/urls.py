from django.urls import path, include
from . import views
from products.apps import ProductsConfig
from .views import *
from django.http import HttpResponse

app_name="products"

urlpatterns = [
    
    path("<str:prod_code>",prodotto,name="prodotto"), #Scheda tecnica del prodotto 
    path("add_product/<str:category>",add_product,name="add_product"), #aggiunta prodotto sulla base della categoria
    path("delete_product/<str:prod_code>",delete_product,name="delete_product"), #cancellazione prodotto
    path("update_product/<str:prod_code>",update_product,name="update_product"), #aggiornamento prodotto
    path('results/',views.SearchView.as_view(), name='search'), #Barra di ricerca dell'header

]
