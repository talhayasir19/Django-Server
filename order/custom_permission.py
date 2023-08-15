from rest_framework.permissions import BasePermission
from .models import Order

class CustomPermission(BasePermission):


    def has_permission(self, request, view):
        print("request.user")
        return super().has_permission(request, view)
    

    def has_object_permission(self, request, view, obj: Order):
        print("request.user")
        if obj.user == request.user:
            return True
        return False