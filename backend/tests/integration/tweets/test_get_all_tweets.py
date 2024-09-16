def test_get_all_tweets(client):
    response = client.get("/api/tweets", headers={'api-key': "test"})
    assert response.json() == {"result": True, "tweets": []}
