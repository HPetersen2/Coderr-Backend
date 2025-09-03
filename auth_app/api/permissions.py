from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Permission class to check if the requesting user is the object's owner.
    """

    def has_object_permission(self, request, view, obj):
        """
        Return True if the request user is the object's owner.
        """
        return request.user == obj.user

