from rest_framework.permissions import BasePermission

class IsCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.reviewer
    
class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            hasattr(request.user, "userprofile") and 
            request.user.userprofile.type == "customer"
        )