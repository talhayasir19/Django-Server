from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.decorators import(
    api_view,
    permission_classes,
    authentication_classes
    )
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from app_authentication.models import AppUser
from .models import Cart, CartItem
from .serializers import (CartSerializer,
                          CartItemSerializer,
                        AddCartItemSerializer,
                        GetCartSerializer)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_cart_Exist(request: HttpRequest)-> Response:
    user = request.user
    cart: Cart = None

    try :
        cart = Cart.objects.get(user=user.id)
    except Cart.DoesNotExist:
        return Response({'ERROR': 'cart does not exist'}, 
                        status=status.HTTP_404_NOT_FOUND)

    if cart:
        return Response({'cart': str(cart.id)})



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_cart(request: HttpRequest)-> Response:
    user = request.user
    existingCart = None
    try:
        existingCart = Cart.objects.get(user=user.id)
        return Response({'error': 'cart is already created'}, 
                        status=status.HTTP_409_CONFLICT)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user)
        cart.save()
        return Response({'id': cart.id, 'response':'cart created successfulyy'})   
    except :
        return Response({'error':'somethign went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])    
def get_cart(request: HttpRequest)-> Response:
    cart = None 
    try:
        cart = Cart.objects.get(user=request.user.id)
    except Cart.DoesNotExist:
        return Response({'error': 'cart not exist'},
                  status=status.HTTP_404_NOT_FOUND)
    if cart:
        try:
            cart_serializer = GetCartSerializer(cart)
            return Response(cart_serializer.data)
        except Exception as e:
            print(e)
            return Response()


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_cart(request: HttpRequest)-> Response:
    user = request.user
    try:
        cart = Cart.objects.get(user=user.id)
        cart.delete()
        return Response({'response': 'deleted successfully'})
    
    except Cart.DoesNotExist:
        return Response({'error': 'cart doesnot exist'},
                         status=status.HTTP_404_NOT_FOUND)    
    


class CartItemView(ViewSet):
    

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def list(self, request)->Response:
        
        user = request.user
        cart = None
        try:
            cart = Cart.objects.get(user=user.id)
        except Cart.DoesNotExist:
            return Response({'error': 'cart doesnot exist'})
        if cart:    
            cart_items = CartItem.objects.filter(cart=cart.id)
            cartitem_serializer = CartItemSerializer(cart_items, many=True)
            return Response(cartitem_serializer.data)
    


    def create(self, request: HttpRequest)-> Response:
        
            
        cartitem_serializer = AddCartItemSerializer(data=request.data)
        cartitem_serializer.is_valid(raise_exception=True)
        cartitem = cartitem_serializer.save()
        return Response({'cart_item':cartitem.id,
                          'response': 'item added successfully'})
    


    def partial_update(self, request: HttpRequest, pk=None)-> Response:
        cart_item = None
        try:
            cart_item = CartItem.objects.get(id=pk)            
        except:
            return Response({'error': 'cart item does not exist'}, 
                            status=status.HTTP_404_NOT_FOUND)
        if cart_item:    
            cartitem_serializer = AddCartItemSerializer(cart_item,
                                                     data=request.data,
                                                     partial=True)
            cartitem_serializer.is_valid(raise_exception=True)
            
            cartitem_serializer.save()
            return Response({'response': 'item updated successfully'})



    def destroy(self, request: HttpRequest, pk=None)-> Response:
        try:
            cart_item = CartItem.objects.get(id=pk)
            cart_item.delete()
            return Response({'response': 'item deleted successfully'})
        except CartItem.DoesNotExist:
            return Response({'error': 'cart item does not exist'}, 
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'error':'something went wrong'})
            



        
    


        
