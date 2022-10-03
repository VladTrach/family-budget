from django.db.models import Q
from rest_framework import viewsets, mixins

from budgets.models import Budget, Transaction
from budgets.permissions import (
    BudgetOwnerOrReadOnlyPermission,
    TransactionAccessOrReadOnlyPermission,
)
from budgets.serializers import BudgetSerializer, TransactionSerializer

ACTION_LIST = "list"


class BudgetViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [BudgetOwnerOrReadOnlyPermission]
    filterset_fields = ["name", "owner_id", "created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(Q(owner=user) | Q(contributors__id=user.id))
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TransactionViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [TransactionAccessOrReadOnlyPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(
            Q(budget__owner=user) | Q(budget__contributors__id=user.id)
        ).order_by("made_at")
        return queryset
