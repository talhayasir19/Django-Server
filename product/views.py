from django.http import HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ViewSet

import boto3
from botocore.exceptions import ClientError

from .serializers import (
    CategorySerilaizer,
    ProductSerializer,
    FavouriteSerializer,
    FetchFavouriteSerializer,
    ChargesSerializer
)

from .models import (
    Category,
    Product,
    FavouriteProducts,
    Charges
    )



RESPONSE = 'response'
ERROR = 'error'



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def add_category(request: HttpRequest) -> Response:
        category_serializer = CategorySerilaizer(data=request.data)
        category_serializer.is_valid(raise_exception=True)
        category: Category = category_serializer.save()
        return Response({RESPONSE: 'category added successfully', 'category_id': category.id })



@api_view(['GET'])
def get_categories(request: HttpRequest)-> Response:
    categories = Category.objects.all()
    category_serializer: CategorySerilaizer = CategorySerilaizer(categories, many=True)
    return Response(category_serializer.data)


class CategoryView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def patch(self, request: HttpRequest, id)-> Response:
        category: Category = None

        try:
             category = Category.objects.get(id=id) 
        except ObjectDoesNotExist :
             return Response({ERROR: 'Category not found with this id',}, status= status.HTTP_404_NOT_FOUND)
        
        if category:
            category_serializer = CategorySerilaizer(category,data=request.data, partial=True)
            category_serializer.is_valid(raise_exception=True)
            updated_category = category = category_serializer.save()
            return Response({RESPONSE: 'updated sucessfully', 'category_id':updated_category.id})
       

    def delete(self, request: HttpRequest, id)-> Response:
        
        try:
             category: Category = Category.objects.get(id=id) 
             print(category)
             category.delete()
             print("exception")
             return Response({RESPONSE: 'category delete successfully', "category_id":id})
        except ObjectDoesNotExist :
             return Response({ERROR: 'Category not found with this id',}, status= status.HTTP_404_NOT_FOUND)

        except Exception as e:
             return Response(str(e))


def upDateImage(name, image,):
        s3_client = boto3.client('s3',
                                aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID, 
                                aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY)
        
        s3_client.upload_fileobj(image,
                                settings.AWS_STORAGE_BUCKET_NAME,
                                name    
                                )
       


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def add_product(request: HttpRequest)-> Response:

    product_serializer = ProductSerializer(data=request.data)
    product_serializer.is_valid(raise_exception=True)
    
    image = product_serializer.validated_data['image']
    prod_name = product_serializer.validated_data['product_name']
    
    try:
        upDateImage(f'images/{prod_name}/{image.name}',image)
    except ClientError:
        return Response({ERROR:'imagefile not uploaded'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({ERROR:'Something went wrong when uploading file'},
                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)

 
    product: Product = product_serializer.save()
    return Response(data={RESPONSE: 'product added successfully',
                           'product_id': product.id,
                           })


@api_view(['GET'])
def get_products(request: HttpRequest):
    product_name = request.query_params.get('productName')
    category = request.query_params.get('category')
    products = None
    if product_name:
        products = Product.objects.filter(product_name__contains=product_name)
    elif category:
        try:
           cate  = Category.objects.get(id=category)
        except Category.DoesNotExist:
            return Response({ERROR:'category with this name not found'},status=status.HTTP_404_NOT_FOUND)
        products = Product.objects.filter(category=cate.id)
    else: 
        products = Product.objects.all()
    
    product_serializer = ProductSerializer(products, many=True)
    return Response(product_serializer.data)




class ProductView(APIView):
     
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
   
    

    def delete(self, request: HttpRequest, id):
        product: Product = None
        try:
            product = Product.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({ERROR: 'product does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if product:
            product.delete()
            return Response({RESPONSE: 'product deleted successfully', })    


    def put(self, request, id):
        product = None
        
        try:
            product = Product.objects.get(id=id)              
        except Product.DoesNotExist:
            return Response({ERROR: 'product not found'},status=status.HTTP_404_NOT_FOUND)   
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data.get('image')
        prod_name = serializer.validated_data.get('product_name')
        try:
           upDateImage(f'images/{prod_name}/{image.name}', image=image)
        except ClientError:
            return Response({ERROR:'imagefile not uploaded'}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({ERROR:'Something went wrong when uploading file'},
                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        updated_product = serializer.save()
        return Response(data={RESPONSE: 'product updated successfully',
                            'product_id': updated_product.id,
                            'url': f'{updated_product.image}'})
     


class ChargesView(ViewSet):

    """
    Extra Charges like delivery charges etc
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request)-> Response:
        charges = Charges.objects.all()
        charges_serializer = ChargesSerializer(charges, many=True)
        return Response(charges_serializer.data)
    
    
    def create(self, request)-> Response:
        charges_serializer = ChargesSerializer(data=request.data)
        charges_serializer.is_valid(raise_exception=True)
        charges = charges_serializer.save()
        return Response({RESPONSE: 'added into charges', 'id': charges.id})
    
    

    def destroy(self, request, pk=None):
        try:
            charges = Charges.objects.get(id=pk)
            charges.delete()
        except Charges.DoesNotExist:
            return Response({ERROR:'Charges with this id not found'}
                            ,status=status.HTTP_404_NOT_FOUND, )    
        return Response({RESPONSE: 'deleted successfully'})
    




class FavouriteView(ViewSet):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    
    """
    Favourte View 
    """
    def list(self, request)-> Response:
        favourite_products = FavouriteProducts.objects.filter(
            user=request.user.id)
        favourite_serializer = FetchFavouriteSerializer(
            favourite_products, many=True)
        return Response(favourite_serializer.data)
    
    
    def create(self, request)-> Response:
        favourite_serializer = FavouriteSerializer(data=request.data, )
        favourite_serializer.is_valid(raise_exception=True)
        favourite_serializer.save()
        return Response({RESPONSE: 'added into favourite successfully'})
    

    def destroy(self, request, pk=None):
        try:
            fav_product = FavouriteProducts.objects.get(id=pk)
            fav_product.delete()
        except FavouriteProducts.DoesNotExist:
            return Response({ERROR:'favourite product not found'}
                            ,status=status.HTTP_404_NOT_FOUND, )    
        return Response({RESPONSE: 'deleted successfully'})
    




    

    



