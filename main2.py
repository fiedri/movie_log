import os
import requests
from dotenv import load_dotenv

# 1. Cargar las variables del archivo .env
load_dotenv()
API_KEY = os.getenv("TMDB_KEY")

def buscar_pelicula(nombre):
    # Configurar la URL y los parámetros de búsqueda
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": API_KEY,
        "query": nombre,
        "language": "es-ES" # Traer los datos en español
    }

    # Lanzar la petición (El "Disparo" al servidor)
    response = requests.get(url, params=params)

    # Verificar si el servidor respondió con éxito (Código 200)
    if response.status_code == 200:
        data = response.json() # Convertir la respuesta a un diccionario de Python
        
        if data['results']:
            # Tomamos el primer resultado (el más probable)
            pelicula = data['results'][0]
            print(f"--- Datos de: {pelicula['title']} ---")
            print(f"ID TMDB: {pelicula['id']}")
            print(f"Sinopsis: {pelicula['overview']}")
            print(f"Puntuación Global: {pelicula['vote_average']}")
        else:
            print("No se encontró nada. ¿Estás seguro de que existe?")
    else:
        print(f"Error en la conexión: {response.status_code}")

# Ejecución
if __name__ == "__main__":
    buscar_pelicula("The Prestige")