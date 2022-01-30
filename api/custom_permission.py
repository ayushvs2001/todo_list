from rest_framework.permissions import  BasePermission

# Custom permission class
class MyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST" and request.user.is_authenticated:
            return True
        if request.method == "GET" and request.user.is_authenticated:
            return True
        return False
