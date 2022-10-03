from rest_framework import viewsets, mixins

from budgets.models import Budget
from budgets.serializers import BudgetSerializer


class BudgetViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
