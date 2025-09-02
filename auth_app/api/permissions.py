from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission class that checks if the requesting user is the owner of the object.
    
    This class inherits from `BasePermission` and overrides the `has_object_permission` method
    to define custom object-level permission logic. The `has_object_permission` method is called
    to check if the user making the request has the required permissions to access or modify a specific object.
    """

    def has_object_permission(self, request, view, obj):
        """
        Checks whether the user making the request is the owner of the object.
        
        Args:
            request: The HTTP request object.
            view: The view that is being accessed (not used in this method).
            obj: The object being accessed or modified, which should have a 'user' attribute.
        
        Returns:
            bool: True if the user making the request is the owner of the object, False otherwise.
        """
        return request.user == obj.user
