def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}



def test_get_empty_listings(client):
    resp = client.get("/listings")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["items"] == []
    assert data["total"] == 0


def test_agent_can_create_listing(client, agent_token):
    resp = client.post(
        "/listings",
        headers=auth_headers(agent_token),
        json={
            "title": "2BR in Kilimani",
            "price": 80000,
            "bedrooms": 2,
            "bathrooms": 2,
            "property_type": "apartment",
            "city": "Nairobi",
        },
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["title"] == "2BR in Kilimani"
    assert data["city"] == "Nairobi"


def test_filter_listings_by_city(client, agent_token):
    # create two listings in different cities
    client.post(
        "/listings",
        headers=auth_headers(agent_token),
        json={
            "title": "Kilimani Apt",
            "price": 90000,
            "bedrooms": 2,
            "bathrooms": 2,
            "property_type": "apartment",
            "city": "Nairobi",
        },
    )

    client.post(
        "/listings",
        headers=auth_headers(agent_token),
        json={
            "title": "Mombasa House",
            "price": 70000,
            "bedrooms": 3,
            "bathrooms": 2,
            "property_type": "house",
            "city": "Mombasa",
        },
    )

    # filter by Nairobi
    resp = client.get("/listings?city=Nairobi")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["total"] == 1
    assert data["items"][0]["city"] == "Nairobi"
