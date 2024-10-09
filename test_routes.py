import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_songs(client):
    response = client.get('/songs?page=1&per_page=10')
    assert response.status_code == 200

def test_average_difficulty(client):
    response = client.get('/songs/difficulty')
    assert response.status_code == 200

def test_add_rating(client):
    response = client.post('/songs/rating', json={"song_id": "1", "rating": 5})
    assert response.status_code == 200
