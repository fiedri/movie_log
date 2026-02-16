from src.utils.search import search_movie
import sqlite3
from datetime import date

conn = sqlite3.connect('movie_root.db')
cursor = conn.cursor()

while True:
    print("Menu")
    print("1. Agregar película")
    print("2. Ver películas")
    print("3. ver recomendaciones")
    print("4. Salir")

    option = input("Seleccione una opción: ")
    
    if option.strip() == '1':
        name = input("Ingrese el nombre de la película: ")
        info = search_movie(name)
        if isinstance(info, str):
            print(info)
            continue
        
        # title = info['title']
        # overview = info['overview']
        # vote_average = info['vote_average']

        cursor.execute('''
            INSERT OR IGNORE INTO movies (tmdb_id, title, overview, average_score, relaese_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (int(info['id']), info['title'], info['overview'], float(info['vote_average']), info['release_date']))
        conn.commit()
        print("Película agregada a la base de datos (simulado).")
        score = input("¿Qué puntuación le das a la película? (1-10): ")
        comment = input("¿Quieres agregar un comentario? (opcional): ")
        cursor.execute('''
            INSERT INTO my_ratings (tmdb_id, score, comment, created_at)
            VALUES (?, ?, ?, ?)
        ''', (int(info['id']), float(score), comment, date.today()))
        conn.commit()
        print(f"Puntuación guardada: {score}")
    elif option.strip() == '4':
        print("Saliendo del programa. ¡Hasta luego!")
        conn.close()
        break
    else:
        print("Opción no válida. Por favor, seleccione una opción del 1 al 4.")


