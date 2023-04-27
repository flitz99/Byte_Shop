from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from django.conf.urls.static import static 
from django.conf import settings
from .initdb import * #definizione di erase e init_db


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^$|^/$|^home/$",views.home,name="home"), #mostra template html per il login
    path('products/', include('products.urls')),    #aggiungo gli url dell'app products
    path('authentication/',include('authentication.urls')), #Aggiungo gli url dell'app authentication
    path('cart/',include('cart.urls')), #Aggiungo gli url dell'app cart
    path('orders/',include('orders.urls')) #Aggiungo gli url dell'app orders
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#---- Inizializzazione del database 

#Table User
#erase_db_Users() #Cancello DB User
#init_db_Users() #Inizializzo DB User

#Table Products
#erase_db_Products() #Cancello DB Product
#init_db_Products() #Inizializzo DB Product

#Table Orders
#erase_db_Orders() #Cancello DB Orders
#init_db_Orders() #Inizializzo DB Orders


