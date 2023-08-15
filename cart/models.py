from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_delete

from app_authentication.models import AppUser
from product.models import Product

class Cart(models.Model):

    user = models.OneToOneField(to=AppUser, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=30, decimal_places=2, default=0.0, )
    sub_total = models.DecimalField(max_digits=30, decimal_places=2, default=0.0,)
    total_tax = models.DecimalField(max_digits=100, decimal_places=2, default=0.0)



class CartItem(models.Model):

    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE)
    qty  = models.IntegerField()
    date = models.DateTimeField(auto_created=True, auto_now=True)
    product = models.OneToOneField(to=Product, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)



@receiver(post_delete, sender=CartItem)
def update_cart_on_item_delete(sender, **kwargs):
    instance: CartItem = kwargs.get('instance')
    cart:Cart = instance.cart
    product: Product = instance.product
    amount = instance.amount
    qty = instance.qty

    total_sale_tax = product.sale_tax * qty
    
    cart.sub_total = cart.sub_total - (amount)

    cart.total = cart.total - (amount + total_sale_tax)
    cart.total_tax = cart.total_tax - total_sale_tax
    cart.save()

