from django.contrib import admin

from budgets.models import Budget, Transaction


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass
