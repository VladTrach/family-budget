from rest_framework import serializers

from budgets.models import Budget, Transaction
from users.models import User


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["id", "name", "owner_id", "amount"]
        read_only_fields = ["amount"]


class DetailBudgetSerializer(serializers.ModelSerializer):
    contributors = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True
    )

    class Meta:
        model = Budget
        fields = ["id", "name", "owner_id", "amount", "contributors"]
        read_only_fields = ["amount"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "budget",
            "type",
            "amount",
            "title",
            "made_at",
            "added_by_user",
        ]
