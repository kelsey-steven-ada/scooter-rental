def test_get_all_scooters_with_no_records(client):
    # Act
    response = client.get("/scooters")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_all_scooters_with_3_records(client, three_scooters):
    # Act
    response = client.get("/scooters")
    response_body = response.get_json()

    # Assert``
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0] == {
        "id": 1,
        "model": "Speedster VII",
        "charge_percent": 25.0,
        "is_available": True 
    }
    assert response_body[1] == {
        "id": 2,
        "model": "Nimbus Sparkle",
        "charge_percent": 100.0,
        "is_available": True 
    }
    assert response_body[2] == {
        "id": 3,
        "model": "Thunderbolt III",
        "charge_percent": 78.5,
        "is_available": True 
    }

def test_get_all_scooters_3_records_one_rental(client, three_scooters_two_rentals_one_returned):
    # Act
    response = client.get("/scooters")
    response_body = response.get_json()

    # Assert``
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0] == {
        "id": 1,
        "model": "Speedster VII",
        "charge_percent": 25.0,
        "is_available": False 
    }
    assert response_body[1] == {
        "id": 2,
        "model": "Nimbus Sparkle",
        "charge_percent": 100.0,
        "is_available": True 
    }
    assert response_body[2] == {
        "id": 3,
        "model": "Thunderbolt III",
        "charge_percent": 78.5,
        "is_available": True 
    }

def test_available_only_param_returns_two_scooters(client, low_charge_scooter):
    # Act
    response = client.get("/scooters?available_only=True")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0] == {
        "id": 2,
        "model": "Nimbus Sparkle",
        "charge_percent": 100.0,
        "is_available": True 
    }
    assert response_body[1] == {
        "id": 3,
        "model": "Thunderbolt III",
        "charge_percent": 78.5,
        "is_available": True 
    }

def test_rent_available_scooter(client, two_users):
    response = client.patch("/scooters/2/rent", json={
        "user_id": 2
    })
    
    response_body = response.get_json()
    assert response_body == {
        "rental_id": 3,
        "user_id": 2,
        "scooter_id": 2,
        "model": "Nimbus Sparkle",
        "is_returned": False
    }

def test_rent_unavailable_scooter(client, two_users):
    response = client.patch("/scooters/1/rent", json={
        "user_id": 2
    })
    
    response_body = response.get_json()
    assert response_body == {"message": "Scooter #1 is not available"}

def test_rent_low_charge_scooter_fails(client, low_charge_scooter):
    response = client.patch("/scooters/4/rent", json={
        "user_id": 2
    })
    
    response_body = response.get_json()
    assert response_body == {"message": "Scooter #4 is not available"}

def test_rent_scooter_user_ineligible(client, scooter_rented_twice):
    response = client.patch("/scooters/2/rent", json={
        "user_id": 1
    })
    
    response_body = response.get_json()
    assert response_body == {"message": "User cannot rent a scooter at this time"}

def test_return_rented_scooter(client, two_users):
    response = client.patch("/scooters/1/return", json={
        "user_id": 1
    })
    
    response_body = response.get_json()
    assert response_body == {
        "rental_id": 2,
        "user_id": 1,
        "scooter_id": 1,
        "model": "Speedster VII",
        "is_returned": True
    }