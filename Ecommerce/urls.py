from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from django.conf.urls.static import static 
from django.conf import settings
from .initdb import * #definizione di erase e init_db

#Urls
urlpatterns = [
    #Urls relativi alla gestione admin di django
    path('admin/', admin.site.urls),
    #Url della homepage
    re_path(r"^$|^/$|^home/$",views.home,name="home"),
    #Urls dell'applicazione products
    path('products/', include('products.urls')),
    #Urls dell'applicazione authentication
    path('authentication/',include('authentication.urls')),
    #Urls dell'applicazione cart 
    path('cart/',include('cart.urls')),
    #Urls dell'applicazione orders
    path('orders/',include('orders.urls')) 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#---- Inizializzazione e popolamento tutti i DB -----

#Metodo per inizializzare il database con utenti, prodotti, ordini e recensioni
#erase_init_all() 



