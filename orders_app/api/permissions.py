from rest_framework import permissions

class IsCustomerUser(permissions.BasePermission):
    """
    Allows only 'customer' users to create orders.
    """
    def has_permission(self, request, view):
        if request.method != 'POST':
            return True
        return hasattr(request.user, 'userprofile') and request.user.userprofile.type == 'customer'


class IsBusinessUser(permissions.BasePermission):
    """
    Allows only 'business' users to create orders.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'userprofile') and request.user.userprofile.type == 'business'


