from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user