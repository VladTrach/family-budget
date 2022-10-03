from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class BudgetOwnerOrReadOnlyPermission(permissions.BasePermission):
    message = "Allow access just for a budget owner."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user
