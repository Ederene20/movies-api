import pytest

from movies.models import Movie


@pytest.mark.django_db
def test_add_movie(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        "/api/movies/",
        {
            "title": "The big Lebowski",
            "genre": "comedy",
            "year": "1998"
        },
        content_type="application/json"
    )

    assert resp.status_code == 201
    assert resp.data["title"] == "The big Lebowski"

    movies = Movie.objects.all()
    assert len(movies) == 1


@pytest.mark.django_db
def test_add_movie_invalid_json(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        '/api/movies/',
        {},
        content_type='application/json'
    )

    assert resp.status_code == 400

    movies = Movie.objects.all()
    assert len(movies) == 0


@pytest.mark.django_db
def test_add_movie_invalid_json_keys(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        "/api/movies/",
        {
            "title": "The big Lebowski",
            "genre": "comedy"
        },
        content_type="application/json"
    )

    assert resp.status_code == 400

    movies = Movie.objects.all()
    assert len(movies) == 0


@pytest.mark.django_db
def test_get_single_movie(client, add_movie):
    movie = add_movie(title="Batman", genre="sci-fi", year="2015")
    resp = client.get(f'/api/movies/{movie.id}/')
    assert resp.status_code == 200
    assert resp.data["title"] == "Batman"


def test_get_single_movie_invalid_id(client):
    resp = client.get(f'/api/movies/foo/')
    assert resp.status_code == 404


@pytest.mark.django_db
def test_get_all_movies(client, add_movie):
    movie_one = add_movie(title="Batman", genre="sci-fi", year="2015")
    movie_two = add_movie(title="Man of Steel", genre="sci-fi", year="2016")

    resp = client.get(f'/api/movies/')

    assert resp.status_code == 200
    assert resp.data[0]["title"] == movie_one.title
    assert resp.data[1]["title"] == movie_two.title


@pytest.mark.django_db
def test_remove_movie(client, add_movie):
    movie = add_movie(title="Mamadou et Bineta sont devenus grands", genre="blank", year="2000")

    response = client.get(f'/api/movies/{movie.id}/')
    assert response.status_code == 200
    assert response.data['title'] == "Mamadou et Bineta sont devenus grands"

    response_two = client.delete(f'/api/movies/{movie.id}/')
    assert response_two.status_code == 204

    response_three = client.get(f'/api/movies/')
    assert response_three.status_code == 200
    assert len(response_three.data) == 0


@pytest.mark.django_db
def test_remove_movie_invalid_id(client):
    response = client.delete(f'/api/movies/99/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_movie(client, add_movie):
    movie = add_movie(title="Les chevaliers du zodiac", year="2002", genre="Anime")

    response = client.put(f'/api/movies/{movie.id}/',
                          {"title": "Les chevaliers du zodiac", "year": "2004", "genre": "Anime"},
                          content_type='application/json')

    assert response.status_code == 200
    assert response.data['title'] == "Les chevaliers du zodiac"
    assert response.data['year'] == "2004"

    response_two = client.get(f'/api/movies/{movie.id}/')
    assert response.status_code == 200
    assert response_two.data['title'] == "Les chevaliers du zodiac"
    assert response_two.data['year'] == "2004"


@pytest.mark.django_db
def test_update_movie_incorrect_id(client):
    response = client.get(f'/api/movies/99/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_movie_invalid_json(client, add_movie):
    movie = add_movie(title="Les chevaliers du zodiac", year="2002", genre="Anime")
    response = client.put(f'/api/movies/{movie.id}/',
                          {},
                          content_type='application/json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_update_movie_invalid_json_key(client, add_movie):
    movie = add_movie(title="Les chevaliers du zodiac", year="2002", genre="Anime")

    response = client.put(f'/api/movies/{movie.id}/',
                          {"title": "Les chevaliers du zodiac", "year": "2004"},
                          content_type='application/json')

    assert response.status_code == 400
