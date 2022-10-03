from django.urls import path, include
from rest_framework.routers import SimpleRouter

from budgets import views

router = SimpleRouter()
router.register(
    "budgets",
    views.BudgetViewSet,
    basename="budgets",
)

urlpatterns = [
    path("", include(router.urls)),
]
