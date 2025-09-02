from rest_framework import permissions

from rest_framework import permissions

class IsCustomerUser(permissions.BasePermission):
    """
    Custom permission to allow only users with type='customer' to create orders.

    This permission class checks if the user has a linked UserProfile, and if the user profile type is 'customer'.
    It is used to restrict the creation of orders to customers only (i.e., users with a 'customer' type).
    """

    def has_permission(self, request, view):
        """
        Determines whether the user has permission to create an order (POST request).

        Args:
            request (HttpRequest): The HTTP request being processed.
            view (View): The view being accessed.

        Returns:
            bool: True if the user is a 'customer' and is allowed to make a POST request; False otherwise.
        """
        if request.method != 'POST':
            return True
        return hasattr(request.user, 'userprofile') and request.user.userprofile.type == 'customer'


class IsBusinessUser(permissions.BasePermission):
    """
    Custom permission to allow only users with type='business' to create orders.

    This permission class checks if the user has a linked UserProfile, and if the user profile type is 'business'.
    It is used to restrict the creation of orders to business users only (i.e., users with a 'business' type).
    """

    def has_permission(self, request, view):
        """
        Determines whether the user has permission to create an order (POST request).

        Args:
            request (HttpRequest): The HTTP request being processed.
            view (View): The view being accessed.

        Returns:
            bool: True if the user is a 'business' and is allowed to make a POST request; False otherwise.
        """
        return hasattr(request.user, 'userprofile') and request.user.userprofile.type == 'business'

