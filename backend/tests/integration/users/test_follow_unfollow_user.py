def test_follow_and_unfollow_user(client):
    response = client.get('/api/users/me', headers={'api-key': "test 2"})
    user_json = response.json()['user']
    user_id = user_json.get('id')
    response = client.post(f'/api/users/{user_id}/follow', headers={'api-key': "test"})
    assert response.json() == {"result": True}
    response = client.delete(f'/api/users/{user_id}/follow', headers={'api-key': "test"})
    assert response.json() == {"result": True}
