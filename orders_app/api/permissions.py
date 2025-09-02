from rest_framework import permissions

class IsCustomerUser(permissions.BasePermission):
    """
    Erlaubt nur Usern mit type='customer', Orders zu erstellen.
    """

    def has_permission(self, request, view):
        if request.method != 'POST':
            return True
        return hasattr(request.user, 'userprofile') and request.user.userprofile.type == 'customer'
    
class IsBusinessUser(permissions.BasePermission):
    """
    Erlaubt nur Usern mit type='business', Orders zu erstellen.
    """

    def has_permission(self, request, view):
        return hasattr(request.user, 'userprofile') and request.user.userprofile.type == 'business'
