from django.db import models
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
    added_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
