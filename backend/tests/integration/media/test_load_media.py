import os


def test_load_media(client):
    with open(os.path.abspath('./tests/integration/media/test_image.png'),
              'rb') as file:

        response = client.post('/api/medias', headers={'api-key': 'test'},
                               files={'file': ('test_image.png', file, 'image/png')})
    response_json = response.json()
    assert response_json == {"result": True, "media_id": 1}
    assert response_json['result'] is True
    assert isinstance(response_json['media_id'], int)
