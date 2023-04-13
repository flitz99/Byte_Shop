from django.contrib import admin
from .models import Ordine, Recensione, Ordine_Item

admin.site.register(Ordine)
admin.site.register(Ordine_Item)
admin.site.register(Recensione)

