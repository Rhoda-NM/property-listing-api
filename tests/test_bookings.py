def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}



def create_listing(client, token):
    resp = client.post(
        "/listings",
        headers=auth_headers(token),
        json={
            "title": "Booking Test Listing",
            "price": 50000,
            "bedrooms": 1,
            "bathrooms": 1,
            "property_type": "apartment",
            "city": "Nairobi",
        },
    )
    assert resp.status_code == 201
    return resp.get_json()["id"]


def test_booking_overlap_is_rejected(client, agent_token):
    listing_id = create_listing(client, agent_token)

    # First booking
    r1 = client.post(
        "/bookings",
        json={
            "listing_id": listing_id,
            "guest_name": "Guest One",
            "guest_email": "guest1@example.com",
            "start_date": "2025-12-01",
            "end_date": "2025-12-05",
        },
    )
    assert r1.status_code == 201

    # Overlapping booking should fail
    r2 = client.post(
        "/bookings",
        json={
            "listing_id": listing_id,
            "guest_name": "Guest Two",
            "guest_email": "guest2@example.com",
            "start_date": "2025-12-03",
            "end_date": "2025-12-06",
        },
    )
    assert r2.status_code == 400
    data = r2.get_json()
    assert "Dates not available" in data["message"]
    assert "conflict" in data
