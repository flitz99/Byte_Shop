from django.db import models
from django.contrib.auth.models import User
from authentication.models import Client # importo la classe Client

category = (
    ('1', 'computer'),
    ('2', 'smartphone')

)
#Classe prodotto generico
class Product(models.Model):
    image= models.ImageField(blank=True, null=True)
    name= models.CharField(max_length=200)
    type= models.CharField(max_length=20, choices= category , default=1)
    product_code=models.CharField(max_length=20, unique=True)
    productor= models.CharField(max_length=50) #tolto anno uscita....
    color= models.CharField(max_length=40)
    size=models.CharField(max_length=100)
    weight=models.FloatField(default=0)
    price= models.FloatField(default=0)
    available= models.BooleanField(default=False) #booleano per verifica disponibilita
    quantity= models.PositiveIntegerField(default=0)
    supplier= models.ForeignKey(User,on_delete=models.CASCADE) #Utente staff che ha inserito il prodotto

#Classe per gli acquisiti effettuati da un utente
class Ordine(models.Model):
    id_ordine= models.CharField(max_length=20, unique=True)
    date = models.DateField(blank=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    client= models.ForeignKey(User, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0)
    total_price=models.FloatField(default=0)

#Classe recensione 
class Recensione(models.Model):
    valutation=models.PositiveIntegerField( default=0) # valore tra 0 e 5
    description = models.CharField( max_length=300) # recensione
    product= models.ForeignKey(Product, on_delete=models.CASCADE) #Prodotto acquistato
    client= models.ForeignKey(User,on_delete=models.CASCADE) #cliente che ha acquistato il prodotto

#Classe prodotto della categoria smartphone
class Smartphone(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    display_size= models.FloatField(default=0)
    cpu= models.CharField(max_length=50)
    ram= models.PositiveIntegerField(default=0)
    disk_size= models.FloatField(default=0)
    operating_system= models.CharField(max_length=100)
    battery_autonomy= models.FloatField(default=0)
    camera= models.IntegerField(default=0)
    additional_function= models.CharField(max_length=1000) 

#Classe prodotto della categoria computer
class Computer(models.Model):
    product= models.OneToOneField(Product, on_delete=models.CASCADE)
    display_size= models.FloatField(default=0)
    display_resolution= models.CharField(max_length=20)
    cpu= models.CharField(max_length=50)
    ram= models.PositiveIntegerField(default=0)
    disk_size= models.FloatField(default=0)
    disk_type= models.CharField(max_length=20) 
    operating_system= models.CharField(max_length=100)
    graphic_card= models.CharField(max_length=50) 
    battery_autonomy= models.FloatField(default=0)
    additional_function= models.CharField(max_length=1000)
    