def test_delete_tweet(client):
    response = client.post('/api/tweets', json={"tweet_data": "Test add tweet 1", "tweet_media_ids": []},
                           headers={'api-key': "test"})
    tweet_id = response.json().get('tweet_id')
    response = client.delete(f'/api/tweets/{tweet_id}', headers={'api-key': "test"})
    assert response.json() == {"result": True}
