from django.db import models
from authentication.models import Client
from products.models import Product

class Carrello_Item(models.Model):
    item=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    price=models.FloatField(default=0)

    def __str__(self):
        return self.item.name + " "+ str(self.quantity)
    
class Carrello(models.Model):
    prodotti=models.ManyToManyField(Carrello_Item)
    user=models.OneToOneField(Client, on_delete=models.CASCADE)






