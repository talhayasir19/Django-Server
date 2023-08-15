from django.core.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from .models import Order, OrderItem
from cart.models import Cart, CartItem
from app_authentication.serializer import UserDetailSerializer
from product.serializers import ProductForOrderSerializer



class OrderSerializer(ModelSerializer):
    # user = UserDetailSerializer()
    class Meta:
        model = Order
        fields = '__all__'
        

    def create(self, validated_data):
        cart = None
        try:
            cart: Cart = Cart.objects.get(user=validated_data.get('user')) 
        except Cart.DoesNotExist:
            raise ValidationError('cart does not exist for this user')
        if cart:          
            order: Order = Order(**validated_data)
            order.total_amount = cart.total
            order.sub_total = cart.sub_total
            order.tax = cart.total_tax
            order.other_cahrges = cart.total - cart.sub_total - cart.total_tax
            order.save() 

            for cart_item in CartItem.objects.filter(cart=cart.id):
                order_item = OrderItem()
                order_item.amount = cart_item.amount
                order_item.order = order
                order_item.product = cart_item.product
                order_item.qty = cart_item.qty
                order_item.save()


            cart = Cart.objects.get(user=order.user)
            cart.delete()   
            return order
       
        return None

class FetchOrderSerializer(ModelSerializer):

    user = UserDetailSerializer()
    
    class Meta:
        model = Order
        fields = '__all__'



class OrderItemSerializer(ModelSerializer):

    product = ProductForOrderSerializer()
    
    class Meta:
        model = OrderItem
        fields = '__all__'

        