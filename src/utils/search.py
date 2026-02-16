import os
import requests
import json
import random
from .date import parse_date_year
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_KEY")

GENRE_MAP = {
    "tv_to_movie": {10759: [28, 12], 10765: [878, 14], 10768: [10752]},
    "movie_to_tv": {28: [10759], 12: [10759], 878: [10765], 14: [10765], 10752: [10768]}
}

def search_media(query, media_type="movie"):
    url = f"https://api.themoviedb.org/3/search/{media_type}"
    params = {"api_key": API_KEY, "query": query, "language": "es-ES"}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        results = data.get('results', [])
        if not results: return "No se encontró nada."
        return filter_media(results, media_type) if len(results) > 1 else results[0]
    except: return "Error de conexión."

def filter_media(results, media_type):
    print(f"\nSelecciona una opción:")
    for idx, item in enumerate(results[:10]):
        title = item.get('title') if media_type == "movie" else item.get('name')
        date = parse_date_year(item.get('release_date' if media_type == "movie" else 'first_air_date'))
        print(f"{idx + 1}. {title} ({date})")
    
    choice = input("\nNúmero (o 'c'): ")
    if choice.lower() == 'c': return None
    try: return results[int(choice) - 1]
    except: return None

def get_media_details(tmdb_id, media_type="movie"):
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

def get_recommendations(cursor, media_type="movie"):
    try:
        cursor.execute("SELECT mg.genre_id FROM media_genres mg JOIN my_ratings r ON mg.tmdb_id = r.tmdb_id WHERE r.score >= 7")
        all_genres = list(set([row[0] for row in cursor.fetchall()]))
        if not all_genres: return "Agrega más favoritos (7+)."

        mapped_genres = set()
        map_key = "movie_to_tv" if media_type == "tv" else "tv_to_movie"
        for g_id in all_genres:
            if g_id in GENRE_MAP[map_key]: mapped_genres.update(GENRE_MAP[map_key][g_id])
            else: mapped_genres.add(g_id)

        cursor.execute("SELECT director FROM media m JOIN my_ratings r ON m.tmdb_id = r.tmdb_id WHERE r.score >= 9 GROUP BY director ORDER BY COUNT(*) DESC LIMIT 1")
        row = cursor.fetchone()
        top_director = row[0] if row else None

    except Exception as e: return f"Error: {e}"

    url = "https://api.themoviedb.org/3/discover/" + media_type
    params = {
        "api_key": API_KEY, "language": "es-ES", "sort_by": "popularity.desc",
        "vote_count.gte": 150, "vote_average.gte": 7.0,
        "with_genres": "|".join(map(str, mapped_genres)),
        "page": random.randint(1, 2)
    }

    try:
        response = requests.get(url, params=params)
        results = response.json().get('results', [])
        
        cursor.execute("SELECT tmdb_id FROM media")
        owned_ids = {row[0] for row in cursor.fetchall()}
        candidates = [p for p in results if p['id'] not in owned_ids]
        
        for p in candidates:
            p['title'] = p.get('title') if media_type == "movie" else p.get('name')
            
        return candidates
    except: return "Error al obtener recomendaciones."

def search_movie(n): return search_media(n, "movie")
def get_movie_details(i): return get_media_details(i, "movie")
def search_tv(n): return search_media(n, "tv")
def get_tv_details(i): return get_media_details(i, "tv")
