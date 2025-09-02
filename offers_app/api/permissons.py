from rest_framework.permissions import BasePermission

class IsBusinessUser(BasePermission):
    """
    Custom permission class that checks if the user is authenticated and is of type 'business'.

    This permission is used to restrict access to certain views or actions based on the user's profile type.
    Specifically, it ensures that the user has a 'business' type in their profile and is authenticated.

    Methods:
        has_permission(request, view): Determines whether the user has permission to access a particular view.
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated and has a 'business' profile.

        This method checks the user's profile type to ensure it is 'business' and that the user is authenticated.

        Args:
            request (Request): The HTTP request object, containing user and other request details.
            view (View): The view that is being accessed.

        Returns:
            bool: True if the user is authenticated and their profile type is 'business', False otherwise.
        """
        user_profile = getattr(request.user, "userprofile", None)
        return bool(
            request.user.is_authenticated
            and user_profile is not None
            and user_profile.type == "business"
        )

class IsOwner(BasePermission):
    """
    Custom permission class that checks if the authenticated user is the owner of the object.

    This permission is used to ensure that only the owner of a resource (e.g., an offer, profile) can modify or access it.

    Methods:
        has_object_permission(request, view, obj): Checks if the user has permission to access or modify a specific object.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the authenticated user is the owner of the given object.

        This method compares the user making the request with the owner of the object (typically represented by the 'user' field).

        Args:
            request (Request): The HTTP request object, containing user and other request details.
            view (View): The view that is being accessed.
            obj (Model): The object that is being accessed (e.g., an Offer or Profile).

        Returns:
            bool: True if the user is the owner of the object, False otherwise.
        """
        return request.user == obj.user
