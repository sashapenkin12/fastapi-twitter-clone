import os.path


def test_load_image(client):
    with open(os.path.abspath('./tests/integration/media/test_image.png'),
              'rb') as file:
        client.post('/api/medias', headers={'api-key': 'test'},
                    files={'file': ('test_image.png', file, 'image/png')})
    response = client.get('/api/images/test_image.png')
    assert response.status_code == 200
