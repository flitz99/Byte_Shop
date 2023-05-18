from django.urls import path
from . import views
from .views import *


app_name="products"

#Urls dell'applicazione
urlpatterns = [
    #Url per la visualizzazione dei dati di un prodotto sualla base del suo product code
    path("id/<str:prod_code>",prodotto,name="prodotto"),
    #Url per l'aggiunta di un prodotto sulla base della categoria
    path("add_product/<str:category>",ProductCreateView.as_view(),name="add_product"), 
    #Url per la cancellazione di un prodotto sulla base del suo product code
    path("delete_product/<str:prod_code>",delete_product,name="delete_product"), 
    #Url per l'aggiornamento dei dati di un prodotto basato sul suo product code
    path("update_product/<str:prod_code>",ProductUpdateView.as_view(),name="update_product"), 
    #Url per i risultati della ricerca sui prodotti
    path('results/',views.SearchView.as_view(), name='search'),
    #Url per la creazione della recensione da parte di un cliente su un prodotto acquistato
    path('create_review/<str:prod_code>',RecensioneCreateView.as_view(),name="create_review"),
    #Url per la visualizzazione di più prodotti
    path("allproducts",AllProductsListView.as_view(),name="all_products")

]
