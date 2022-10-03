from rest_framework import serializers

from budgets.models import Budget, Transaction


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["id", "name", "owner_id"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "budget_id",
            "type",
            "amount",
            "title",
            "made_at",
            "added_by_user",
        ]
