from django.urls import reverse
from rest_framework import status

from budgets.models import Budget


def test_happy_list_user_budgets(budget, api_client):
    url = reverse("api_v1:budgets-list")
    api_client.force_login(budget.owner)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["results"][0]["id"] == budget.id


def test_list_user_budgets_forbidden(budget, api_client):
    url = reverse("api_v1:budgets-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_happy_list_contributed_budgets(budget_with_contributor, api_client):
    url = reverse("api_v1:budgets-list")
    contributor = budget_with_contributor.contributors.first()
    api_client.force_login(contributor)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["results"][0]["id"] == budget_with_contributor.id


def test_happy_retrieve_budget(budget, api_client):
    url = reverse("api_v1:budgets-detail", args=[budget.id])
    api_client.force_login(budget.owner)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == budget.id


def test_happy_destroy_budget(budget, api_client):
    url = reverse("api_v1:budgets-detail", args=[budget.id])
    api_client.force_login(budget.owner)
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Budget.objects.filter(id=budget.id).exists()


def test_happy_edit_budget(budget, api_client):
    url = reverse("api_v1:budgets-detail", args=[budget.id])
    new_budget_name = "New name of the budget"
    api_client.force_login(budget.owner)
    response = api_client.patch(url, {"name": new_budget_name}, format="json")
    assert response.status_code == status.HTTP_200_OK
    budget.refresh_from_db()
    assert new_budget_name == budget.name


def test_update_budget_by_contributor_forbidden(
    budget_with_contributor,
    api_client,
):
    url = reverse("api_v1:budgets-detail", args=[budget_with_contributor.id])
    contributor = budget_with_contributor.contributors.first()
    api_client.force_login(contributor)
    response = api_client.patch(
        url,
        {"name": "you can't change name"},
        format="json",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_budget_by_contributor_forbidden(
    budget_with_contributor,
    api_client,
):
    url = reverse("api_v1:budgets-detail", args=[budget_with_contributor.id])
    contributor = budget_with_contributor.contributors.first()
    api_client.force_login(contributor)
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_happy_filter_budgets_by_name(budget, api_client):
    url = reverse("api_v1:budgets-list")
    api_client.force_login(budget.owner)
    Budget.objects.create(
        owner=budget.owner,
        name="The second budget",
    )

    # test without filtering first
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 2

    response = api_client.get(url, {"name": budget.name})
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1


def test_pagination_user_budgets(budget, api_client):
    url = reverse("api_v1:budgets-list")
    Budget.objects.create(
        owner=budget.owner,
        name="The second budget",
    )
    api_client.force_login(budget.owner)
    response = api_client.get(url, {"offset": 0, "limit": 1})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 2
    assert len(response.data["results"]) == 1

    next_page_response = api_client.get(response.data["next"])
    assert len(next_page_response.data["results"]) == 1


def test_create_budget(user, api_client):
    url = reverse("api_v1:budgets-list")
    data = {
        "name": "Budget created by API",
    }

    api_client.force_login(user)
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    fetched_budget = Budget.objects.get(name=data["name"])
    assert response.data["id"] == fetched_budget.id
    assert response.data["owner_id"] == user.id
