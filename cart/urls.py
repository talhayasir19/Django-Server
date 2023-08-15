from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (check_cart_Exist,
                    create_cart,
                    CartItemView,
                    get_cart,
                    delete_cart
                    )


router = DefaultRouter()
router.register('cartItem', CartItemView, 'cartitem')

urlpatterns = [
    path('checkCartExist', check_cart_Exist),
    path('createCart/', create_cart),
    path('fetchCart', get_cart),
    path('deleteCart/', delete_cart),
    path('', include(router.urls))  
]