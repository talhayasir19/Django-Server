from django.db import models
from app_authentication.models import AppUser
from cart.models import Cart
from product.models import Product



class Order(models.Model):
    
    STATUS_PENDING = 'pending'
    STATUS_DELIVERED = 'delivered'
    STATUS_IN_PROCESS = 'in process'

    status_choices = (

        ('0', STATUS_PENDING),
        ('1', STATUS_IN_PROCESS),
        ('2', STATUS_DELIVERED),

    )


    user = models.ForeignKey(to=AppUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    
    
    total_amount = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    sub_total = models.DecimalField(max_digits=50, decimal_places=2,default=0)
    tax = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    other_cahrges = models.DecimalField(max_digits=50, decimal_places=0, default=0)
    
    date = models.DateTimeField(auto_created=True, auto_now=True)
    status = models.CharField(max_length=50, choices=status_choices)
    long = models.DecimalField(max_digits=50, decimal_places=6)
    lat = models.DecimalField(max_digits=50, decimal_places=6)
    extra = models.CharField(max_length=100)
    user_deal = models.BooleanField(default=True)




class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE )
    product = models.ForeignKey(to=Product, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    qty = models.IntegerField()
    





