from django.urls import reverse
from rest_framework import status


def test_happy_list_user_transactions(transaction, api_client):
    url = reverse("api_v1:transactions-list")
    api_client.force_login(transaction.budget.owner)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["results"][0]["id"] == transaction.id


def test_happy_update_transaction_by_budget_owner(
    transaction, user2, api_client
):
    transaction.budget.add_contributors([user2])
    transaction.added_by_user = user2
    transaction.save(update_fields=["added_by_user"])
    url = reverse("api_v1:transactions-detail", args=[transaction.id])
    api_client.force_login(transaction.budget.owner)
    response = api_client.patch(url, {"amount": "40.00"}, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["amount"] == "40.00"


def test_update_transaction_by_other_contributor_forbidden(
    transaction, user2, api_client
):
    transaction.budget.add_contributors([user2])
    url = reverse("api_v1:transactions-detail", args=[transaction.id])
    api_client.force_login(user2)
    response = api_client.patch(url, {"amount": "40.00"}, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN
