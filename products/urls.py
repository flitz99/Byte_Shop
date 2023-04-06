from django.urls import path, include
from . import views
from products.apps import ProductsConfig
from .views import *
from django.http import HttpResponse

app_name="products"

urlpatterns = [
    
    path("category/<str:prod_code>",prodotto,name="prodotto"), #Scheda tecnica del prodotto 
    path("add_product/<str:category>",add_product,name="add_product"), #aggiunta prodotto
    path("delete_product/<int:id>",delete_product,name="delete_product"), #cancellazione prodotto
    path("update_product/<int:id>",update_product,name="update_product"), #aggiornamento prodotto
    path("orders/<int:client_id>",orders,name="ordini"), #ordini di un cliente
    #path("search/<str:search>",search,name="ricerca") #Risultati barra ricerca
    path('results/',views.SearchView.as_view(), name='search'),

    
]
