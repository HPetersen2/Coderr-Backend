from rest_framework.permissions import BasePermission

class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        user_profile = getattr(request.user, "userprofile", None)
        return bool(
            request.user.is_authenticated
            and user_profile is not None
            and user_profile.type == "business"
        )

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user