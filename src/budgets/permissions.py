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


class TransactionAccessOrReadOnlyPermission(permissions.BasePermission):
    message = "Allow access just for a user added by or a budget owner."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True
        if obj.added_by_user == user:
            return True
        return obj.budget.owner == user


class CreateTransactionPermission(permissions.BasePermission):
    message = (
        "Allow to create a transaction for a budget owner or contributor."
    )

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        serializer = view.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        budget = serializer.validated_data["budget"]
        return budget.owner == user or budget.contributors.filter(id=user.id)
