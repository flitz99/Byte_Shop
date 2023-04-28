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

#---- Inizializzazione e popolamento tutti i DB -----

#erase_init_all()



