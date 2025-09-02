from rest_framework.permissions import BasePermission

class IsCreator(BasePermission):
    """
    Custom permission to check if the user is the creator (reviewer) of the object.
    This permission ensures that only the user who created the object (i.e., the reviewer) 
    is allowed to perform actions on it.

    Methods:
        has_object_permission(request, view, obj): 
            Checks if the request user is the same as the reviewer (creator) of the object.
    """
    def has_object_permission(self, request, view, obj):
        """
        Checks if the user making the request is the creator (reviewer) of the object.

        Args:
            request: The incoming HTTP request.
            view: The view that is processing the request.
            obj: The object being accessed.

        Returns:
            bool: `True` if the user is the creator, otherwise `False`.
        """
        return request.user == obj.reviewer
    
class IsCustomer(BasePermission):
    """
    Custom permission to check if the user is a customer.
    This permission ensures that only users with a "customer" profile type are allowed
    to perform certain actions.

    Methods:
        has_permission(request, view): 
            Checks if the request user is authenticated and has a user profile with type "customer".
    """
    def has_permission(self, request, view):
        """
        Checks if the user is authenticated and has the "customer" profile type.

        Args:
            request: The incoming HTTP request.
            view: The view that is processing the request.

        Returns:
            bool: `True` if the user is authenticated and is a customer, otherwise `False`.
        """
        return (
            request.user.is_authenticated and 
            hasattr(request.user, "userprofile") and 
            request.user.userprofile.type == "customer"
        )
