from django.db.models import Q
from rest_framework import viewsets, mixins

from budgets.models import Budget
from budgets.serializers import BudgetSerializer


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

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(
            Q(owner=user) | Q(contributors__id=user.id)
        )
        return queryset
