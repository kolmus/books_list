import pytest


@pytest.mark.django_db
def test_api_list_books(client, set_up):
    search_data = {"search": "a", "date_from": "1800-01-01", "date_to": "2021-01-07"}
    response2 = client.post("/books/api/", search_data, format="json")
    print(response2.content)
    assert response2.status_code == 200

    search_data = {
        "search": "a",
    }
    response2 = client.post("/books/api/", search_data, format="json")
    print(response2.content)
    assert response2.status_code == 200
