from rest_framework.permissions import BasePermission

class IsCreator(BasePermission):
    """Permission to allow only the object's creator (reviewer) to perform actions."""
    def has_object_permission(self, request, view, obj):
        """Return True if the request user is the creator (reviewer) of the object."""
        return request.user == obj.reviewer

class IsCustomer(BasePermission):
    """Permission to allow only users with a 'customer' profile type."""
    def has_permission(self, request, view):
        """Return True if the user is authenticated and is a customer."""
        return (
            request.user.is_authenticated and 
            hasattr(request.user, "userprofile") and 
            request.user.userprofile.type == "customer"
        )

