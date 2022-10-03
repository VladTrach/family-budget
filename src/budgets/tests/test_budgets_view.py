from django.urls import reverse
from rest_framework import status


def test_happy_retrieve_budget(budget, client):
    url = reverse("api_v1:budgets-detail", args=[budget.id])
    client.force_login(budget.owner)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == budget.id
