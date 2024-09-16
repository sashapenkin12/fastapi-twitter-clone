def test_create_tweet(client):
    response = client.post('/api/tweets', json={"tweet_data": "Test add tweet 1", "tweet_media_ids": []},
                           headers={'api-key': "test"})
    response_json = response.json()
    assert response_json['result'] is True
    assert isinstance(response_json['tweet_id'], int)
