def test_like_and_unlike_tweet(client):
    tweet_response = client.post('/api/tweets', json={"tweet_data": "Tweet for likes test", "tweet_media_ids": []},
                                 headers={'api-key': "test"})
    tweet_id = tweet_response.json().get("tweet_id")
    response = client.post(f"/api/tweets/{tweet_id}/likes", headers={'api-key': "test"})
    assert response.json() == {"result": True}
    response = client.delete(f"/api/tweets/{tweet_id}/likes", headers={'api-key': "test"})
    assert response.json() == {"result": True}
    client.delete(f'/api/tweets/{tweet_id}', headers={'api-key': "test"})