from django.db import models
from products.models import Product
from authentication.models import Client
from django.contrib.auth.models import User

class Ordine_Item(models.Model):
    item=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    price=models.FloatField(default=0)

#Classe per gli acquisiti effettuati da un utente
class Ordine(models.Model):
    id_ordine= models.CharField(max_length=20, unique=True)
    date = models.DateField(blank=False)
    prodotti=models.ManyToManyField(Ordine_Item)
    client= models.ForeignKey(Client, on_delete=models.CASCADE)
    total_price=models.FloatField(default=0)

#Classe recensione 
class Recensione(models.Model):
    valutation=models.PositiveIntegerField( default=0) # valore tra 0 e 5
    date = models.DateField(blank=False)
    description = models.CharField( max_length=300) # recensione
    product= models.ForeignKey(Product, on_delete=models.CASCADE) #Prodotto acquistato
    client= models.ForeignKey(Client,on_delete=models.CASCADE) #cliente che ha acquistato il prodotto

