import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_KEY")


def search_media_gui(query, media_type="movie"):
    url = f"https://api.themoviedb.org/3/search/{media_type}"
    params = {"api_key": API_KEY, "query": query, "language": "es-ES"}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data.get('results', [])
    except:
        return []

def get_media_details_gui(tmdb_id, media_type="movie"):
    url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}"
    params = {"api_key": API_KEY, "language": "es-ES", "append_to_response": "credits,keywords"}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        title = data.get("title") if media_type == "movie" else data.get("name")
        date = data.get("release_date") if media_type == "movie" else data.get("first_air_date")
        
        if media_type == "movie":
            crew = data.get('credits', {}).get('crew', [])
            director = next((m['name'] for m in crew if m['job'] == 'Director'), "Desconocido")
            keywords = data.get("keywords", {}).get("keywords", [])
        else:
            creators = data.get('created_by', [])
            director = creators[0]['name'] if creators else "Desconocido"
            keywords = data.get("keywords", {}).get("results", [])
            
        return {
            "tmdb_id": data.get("id"), "title": title, "overview": data.get("overview"),
            "vote_average": data.get("vote_average"), "release_date": date,
            "director": director, "genres": data.get("genres", []),
            "keywords": keywords, "media_type": media_type
        }
    except: return None
