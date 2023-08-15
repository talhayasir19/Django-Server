from django.http import HttpRequest
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from .serializer import AppUserRegisterSerializer,LoginSeriliazer, UserDetailSerializer
from .models import AppUser

RESPONSE = 'response'
ERROR = 'error'

class RegisterView(APIView):

    def post(self, request: HttpRequest)-> Response:
        register_serializer = AppUserRegisterSerializer(data=request.data)
        register_serializer.is_valid(raise_exception=True)
        user = register_serializer.save()
        token = Token.objects.create(user=user)
        return Response({'token':str(token), 'respose': 'Register Successfully'})
    
    



class LoginView(APIView):

    def post(self, request: HttpRequest)-> Response:
        login_serializer = LoginSeriliazer(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        user: AppUser = None
        try:
            user = AppUser.objects.get(email=login_serializer.validated_data['email'])
        except ObjectDoesNotExist:
            return Response({ERROR:'user doesnot exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({ERROR:'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if user:
            if user.check_password(raw_password=login_serializer.validated_data['password']):
                token, created = Token.objects.get_or_create(user=user)

                return Response({'email': str(user.email),
                                 'token':str(token),
                                 'is_staff':user.is_staff, 
                                 'is_superuser':user.is_superuser,
                                 RESPONSE: 'login successfully'})
            else :
                return Response({ERROR:'password is not correct'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request: HttpRequest)-> Response:

    request.user.auth_token.delete()
    return Response({RESPONSE:'logout successsfully'})



@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request: HttpRequest)-> Response:
    user = UserDetailSerializer(request.user)
    return Response(user.data)


@api_view(["GET"])
def verify_user(request, token):
    user:AppUser = AppUser.objects.get(verification_token=token)
    if not user.is_verified:
        user.is_verified = True
        user.save()
        print("verfires view", token)
        return render(request=request, template_name="verified_page.html", context={'user':user.email})
    return render(request, template_name='verified_page.html')





