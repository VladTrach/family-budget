import pytest
from rest_framework.test import APIClient

from budgets.models import Budget, Transaction
from users.models import User


@pytest.fixture()
def api_client():
    """A Django REST Framework test client instance."""
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="test_user",
        password="password",
        email="test_user@family.budget",
    )


@pytest.fixture
def user2(db):
    return User.objects.create_user(
        username="test_user2",
        password="password",
        email="test_user2@family.budget",
    )


@pytest.fixture
def budget(db, user):
    return Budget.objects.create(name="Test budget", owner=user)


@pytest.fixture
def budget_with_contributor(db, budget):
    contributor = User.objects.create_user(
        username="budget_contributor",
        password="password",
        email="contributor@family.budget",
    )
    budget.contributors.add(contributor)
    return budget


@pytest.fixture
def transaction(db, budget):
    return Transaction.objects.create(
        budget=budget,
        type=Transaction.TYPE_INCOME,
        amount=10.00,
        title="Test transaction",
        added_by_user=budget.owner,
    )


@pytest.fixture
def transaction_expense(db, budget):
    return Transaction.objects.create(
        budget=budget,
        type=Transaction.TYPE_EXPENSE,
        amount=17.00,
        title="Test expense transaction",
        added_by_user=budget.owner,
    )
