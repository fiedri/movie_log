import os
import requests
from .date import parse_date_year
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_KEY")

def search_movie(name):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": API_KEY,
        "query": name,
        "language": "es-ES"    
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if len(data['results']) > 1:
            choice = filter_movie(data['results'])
            return choice
        elif len(data['results']) == 1:
            return data['results'][0]
        else:
            return "No se encontró nada. ¿Estás seguro de que existe?"

def filter_movie(results):
    
    print("Se encontraron varias películas. Por favor, elige una:")
    for idx, movie in enumerate(results):
        fecha = parse_date_year(movie['release_date'])
        print(f"""{idx + 1}. {movie['title']} ({fecha})
""")
        #
    
    choice = int(input("Número de la película que deseas seleccionar: "))
    return results[choice - 1]

