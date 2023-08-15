
from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import Cart, CartItem
from product.models import Product, Charges
from product.serializers import ProductSerializer, ChargesSerializer


class CartSerializer(ModelSerializer):
    
    class Meta:
        model = Cart
        fields = '__all__'




class GetCartSerializer(CartSerializer):

    charges = SerializerMethodField()

    class Meta(CartSerializer.Meta):
        fields = ['charges', 'user','total', 'sub_total', 'total_tax']


    def get_charges(self, obj):
        list_of_charges = []
        charges = Charges.objects.all()
        for charg in charges:
            list_of_charges.append({'name': charg.charges_name,
                                     'ammount': charg.amount})
            
        return  list_of_charges
    



class CartItemSerializer(ModelSerializer):

    
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'        


   


class AddCartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'  


    def create(self, validated_data):
        cart: Cart = validated_data.get('cart')
        product: Product = validated_data.get('product') 
        cartitem: CartItem = CartItem.objects.create(**validated_data)
        print(cartitem.qty)
        print(product.price)
        cartitem.amount = cartitem.qty * product.price
        cartitem.save()

        sub_total = 0
        sale_tax = 0
        other_charges = 0

        for item in CartItem.objects.filter(cart=cart.id):
            sub_total = sub_total + (item.qty * item.product.price)
            sale_tax = sale_tax + (item.qty * item.product.sale_tax)

        for charges in Charges.objects.all():
           other_charges = other_charges + charges.amount

        cart.sub_total = sub_total
        cart.total_tax = sale_tax
        cart.total = sub_total + sale_tax + other_charges
        cart.save()
        return cartitem


    def update(self, instance: CartItem, validated_data):

        cartitem: CartItem = super().update(instance, validated_data)
        cartitem.amount = cartitem.qty * instance.product.price
        
        cartitem.save()
        
        if self.partial:
            
            sub_total = 0
            sale_tax = 0
            other_charges = 0
            
            for item in CartItem.objects.filter(cart=instance.cart.id):
                sub_total = sub_total+ (item.qty * item.product.price)
                sale_tax = sale_tax + (item.qty * item.product.sale_tax)
        
            for charges in Charges.objects.all():
                other_charges = other_charges + charges.amount
            
            instance.cart.sub_total = sub_total
            instance.cart.total_tax = sale_tax
            instance.cart.total = sub_total + sale_tax + other_charges
            
            
            try:
               instance.cart.save()
            except Exception as e:
               print(e) 
        return cartitem
        