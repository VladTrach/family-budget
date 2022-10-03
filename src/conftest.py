import pytest

from budgets.models import Budget
from users.models import User


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="test_user",
        password="password",
        email="test_user@famil",
    )


@pytest.fixture
def budget(db, user):
    return Budget.objects.create(name="Test budget", owner=user)
