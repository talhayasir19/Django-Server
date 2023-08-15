from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryView,
    add_category,
    get_categories,
    add_product,
    get_products,
    ProductView,
    FavouriteView,
    ChargesView


    )

router = DefaultRouter()

router.register('favouriteProduct',FavouriteView, basename='favourite' )
router.register('charges', ChargesView, basename='charges')


urlpatterns = [
    path('category/<int:id>/' , CategoryView.as_view()),
    path('addCategory/' , add_category),
    path('categories' , get_categories),


    path('addProduct/' , add_product),
    path('products' , get_products),
    path('product/<int:id>/' , ProductView.as_view()),

    path('', include(router.urls))
    
    
]