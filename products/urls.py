from django.urls import path, include
from . import views
from products.apps import ProductsConfig
from .views import *


app_name="products"

urlpatterns = [
    
    path("id/<str:prod_code>",prodotto,name="prodotto"), #Scheda tecnica del prodotto 
    path("add_product/<str:category>",ProductCreateView.as_view(),name="add_product"), #aggiunta prodotto sulla base della categoria
    path("delete_product/<str:prod_code>",delete_product,name="delete_product"), #cancellazione prodotto
    path("update_product/<str:prod_code>",ProductUpdateView.as_view(),name="update_product"), #aggiornamento prodotto
    path('results/',views.SearchView.as_view(), name='search'), #Barra di ricerca dell'header
    path('create_review/<str:prod_code>',RecensioneCreateView.as_view(),name="create_review"),
    path("allproducts",AllProductsListView.as_view(),name="all_products")

]
