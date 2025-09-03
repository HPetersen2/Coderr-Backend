from rest_framework.permissions import BasePermission

class IsBusinessUser(BasePermission):
    """
    Custom permission to check if the user is authenticated and has a 'business' profile type.
    Method:
        has_permission(request, view): Returns True if the user is authenticated and their profile type is 'business'.
    """

    def has_permission(self, request, view):
        user_profile = getattr(request.user, "userprofile", None)
        return bool(
            request.user.is_authenticated
            and user_profile is not None
            and user_profile.type == "business"
        )

class IsOwner(BasePermission):
    """
    Custom permission to check if the authenticated user is the owner of the object.
    Method:
        has_object_permission(request, view, obj): Returns True if the user is the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user

