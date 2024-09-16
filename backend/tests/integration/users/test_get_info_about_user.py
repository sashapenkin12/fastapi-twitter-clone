def test_get_info_about_current_user(client):
    response = client.get("/api/users/me", headers={'api-key': "test"})
    response_json = response.json()
    assert response_json['result'] is True


def test_get_info_about_user(client):
    response = client.get("/api/users/1", headers={'api-key': "test"})
    response_json = response.json()
    assert response_json['result'] is True
