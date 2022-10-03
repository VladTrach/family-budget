from decimal import Decimal
from typing import List

from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from family_budget import settings


class Group(models.Model):
    name = models.CharField(max_length=255)


class Budget(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="budgets",
    )
    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="contributed_budgets",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(Group, related_name="budgets")

    def add_contributors(self, contributors: List):
        self.contributors.add(*contributors)

    @cached_property
    def amount(self):
        income_sum = self.transactions.filter(
            type=Transaction.TYPE_INCOME
        ).aggregate(Sum("amount"))
        income_sum = income_sum.get("amount__sum") or Decimal("0")
        expenses_sum = self.transactions.filter(
            type=Transaction.TYPE_EXPENSE
        ).aggregate(Sum("amount"))
        expenses_sum = expenses_sum.get("amount__sum") or Decimal("0")
        return income_sum - expenses_sum


class Transaction(models.Model):
    TYPE_INCOME = "income"
    TYPE_EXPENSE = "expense"
    TYPE_CHOICES = [
        (TYPE_INCOME, _("Income")),
        (TYPE_EXPENSE, _("Expense")),
    ]

    budget = models.ForeignKey(
        Budget,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=TYPE_EXPENSE,
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    title = models.CharField(max_length=255)
    added_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    made_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
