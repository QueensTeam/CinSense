import os
import requests
from dotenv import load_dotenv
import os

load_dotenv()

def test_get_all_movies_with_right_API_key_returns_200():
    response = requests.get("https://api.themoviedb.org/3/discover/movie?api_key=" + os.environ.get('TMDB_API_KEY') + "&sort_by=popularity.desc&page=1")
    assert response.status_code == 200

def test_get_all_movies_with_wrong_API_key_returns_400():
    response = requests.get("https://api.themoviedb.org/3/discover/movie?api_key=" + "" + "&sort_by=popularity.desc&page=1")
    assert response.status_code != 200

def test_get_genres_returns_JSON():
    response = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=" + os.environ.get('TMDB_API_KEY') + "&language=en-US")
    assert response.headers["Content-Type"] == "application/json;charset=utf-8"