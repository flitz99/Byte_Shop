from django.db import models
from django.contrib.auth.models import User

#Model Client che estende lo User di default di Django con alcuni campi
class Client (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(blank=True, null=True, default="unknown.jpeg")
    telephone = models.CharField( max_length=15)
    address= models.CharField(max_length=30)
    house_number= models.IntegerField(default=1)
    city= models.CharField(max_length=40)
    province= models.CharField(max_length=40)
    cap= models.IntegerField(default=11111)
    birth_date= models.DateField(null=True, blank=True)



