from rest_framework import serializers

from budgets.models import Budget


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["id", "name", "owner_id"]
