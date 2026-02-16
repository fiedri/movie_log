import os
import requests
import json
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

def get_movie_details(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
    params = {
        "api_key": API_KEY,
        "language": "es-ES",
        "append_to_response": "credits,keywords"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # 1. Extraer el Director de la lista de Crew
        # Buscamos a la persona cuyo trabajo sea 'Director'
        crew = data.get('credits', {}).get('crew', [])
        director = next((member['name'] for member in crew if member['job'] == 'Director'), "Desconocido")
        
        # 2. Construir el objeto filtrado (Solo lo esencial para tu Ego)
        movie_object = {
            "tmdb_id": data.get("id"),
            "title": data.get("title"),
            "overview": data.get("overview"),
            "vote_average": data.get("vote_average"),
            "release_date": data.get("release_date"),
            "director": director,
            "genres": data.get("genres", []),        # Lista de {'id': X, 'name': '...'}
            "keywords": data.get("keywords", {}).get("keywords", []) # Lista de {'id': X, 'name': '...'}
        }
        
        return movie_object
    
    return None

"""

"""