from django.db import models
from app_authentication.models import AppUser
 




class Category(models.Model):
    category_name = models.CharField(unique=True, max_length=100)
    


class Product(models.Model):
    
    # def path(instance, filename):
    #     return ''.join(['images/',f'{instance.product_name}/',filename])
   
    product_name = models.CharField(unique=True, max_length=100)
    image = models.ImageField()
    qty = models.IntegerField()
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.CharField(max_length=200)
    sale_tax = models.DecimalField(max_digits=20,decimal_places=2)
    
    


class Charges(models.Model):
    charges_name = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(decimal_places=2,max_digits=10)



    
class FavouriteProducts(models.Model):
    user = models.ForeignKey(to=AppUser, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    




