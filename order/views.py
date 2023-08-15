from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status


from .models import Order, OrderItem
from .serializers import (OrderSerializer, 
                          OrderItemSerializer, 
                          FetchOrderSerializer,
                          )
from .custom_permission import CustomPermission



class OrderView(ViewSet):

    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
     
    
    def list(self, request: HttpRequest)-> Response:
        status = request.query_params.get('status')
        user_deal = request.query_params.get('user_deal')

        
        if user_deal :
            if user_deal == 'false':
                print(user_deal)
                orders = Order.objects.filter(user_deal=False)
                order_serializer = FetchOrderSerializer(orders, many=True)
                return Response(order_serializer.data)
            else :
                orders = Order.objects.filter(user_deal=True)
                order_serializer = FetchOrderSerializer(orders, many=True)
                return Response(order_serializer.data)
        
        elif status:
            
            orders = Order.objects.filter(status=status, user_deal=True)
            order_serializer = FetchOrderSerializer(orders, many=True)
            return Response(order_serializer.data)
        
        else:
            orders = Order.objects.filter(user_deal=True)
            order_serializer = FetchOrderSerializer(orders, many=True)
            return Response(order_serializer.data)
        
    
    def retrieve(self, request: HttpRequest, pk=None):
        order = None
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response({'error': 'order doesnot exist'},
                             status=status.HTTP_404_NOT_FOUND)

        if order:
            order_serializer = FetchOrderSerializer(order)   
            return Response(order_serializer.data)

    
       
    def create(self, request: HttpRequest)-> Response:
        try:
            order_serializer = OrderSerializer(data=request.data )
            order_serializer.is_valid(raise_exception=True)
            order: Order = order_serializer.save()
            return Response({'order_id': order.id, 
                        'response': 'order created successfully'})

        except Exception  as e:
            return Response({'error': e})

        

    def partial_update(self, request: HttpRequest, pk=None)-> Response:
        order = None
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response({'error': 'order doesnot exist'},
                             status=status.HTTP_404_NOT_FOUND)

        if order:
            order_serializer = OrderSerializer(order, data=request.data, partial=True)
            order_serializer.is_valid(raise_exception=True)
            order_serializer.save()   
            return Response(order_serializer.data)
     


    def delete(self, request: HttpRequest, pk=None)-> Response:
        try:

            order = Order.objects.get(id=pk)
            id = order.id
            order.delete()
            return Response({'order_id':id,'response':'deleted successfully'})      
        except Order.DoesNotExist:
            return Response({'error':'order does not exist'},
                             status=status.HTTP_404_NOT_FOUND)
        


class OrderViewByUser(APIView):
    
     
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        orders = Order.objects.filter(user=request.user.id)
        order_serializer = FetchOrderSerializer(orders, many=True)
        return Response(order_serializer.data)




class OrderItemView(ModelViewSet):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    

    def list(self, request, *args, **kwargs):
        order_id = request.query_params.get('order')
        query = None
        if order_id:
            query = OrderItem.objects.filter(order=order_id)
        else:
            query = self.get_queryset()
        serializer = OrderItemSerializer(query, many=True)
        return Response(serializer.data)
