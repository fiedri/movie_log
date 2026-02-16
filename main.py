from src.utils.search import search_movie
from src.utils.search import get_movie_details
import sqlite3


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
        details = get_movie_details(info['id'])
        
        # title = info['title']
        # overview = info['overview']
        # vote_average = info['vote_average']

        cursor.execute('''
            INSERT OR IGNORE INTO movies (tmdb_id, title, overview, average_score, relaese_date, director)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (int(info['id']), info['title'], info['overview'], float(info['vote_average']), info['release_date'], details['director']))
        conn.commit()
        print("Película agregada a la base de datos (simulado).")
        score = input("¿Qué puntuación le das a la película? (1-10): ")
        comment = input("¿Quieres agregar un comentario? (opcional): ")
        cursor.execute('''
            INSERT INTO my_ratings (tmdb_id, score, comment)
            VALUES (?, ?, ?)
        ''', (int(info['id']), float(score), comment))
        conn.commit()
        print(f"Puntuación guardada: {score}")

        for genre in details['genres']:
            g_id = genre['id']
            g_name = genre['name']
            cursor.execute('''
                INSERT OR IGNORE INTO genres (genre_id, name)
                VALUES (?, ?)
            ''', (int(g_id), g_name))
            conn.commit()
            cursor.execute('''
                INSERT OR IGNORE INTO movies_genres (tmdb_id, genre_id)
                VALUES (?, ?)
            ''', (int(info['id']), g_id))
            conn.commit()
        
        for keyword in details['keywords']:
            k_id = keyword['id']
            k_name = keyword['name']
            cursor.execute('''
                INSERT OR IGNORE INTO keyword (keyword_id, keyword)
                VALUES (?, ?)
            ''', (int(k_id), k_name))
            conn.commit()
            cursor.execute('''
                INSERT OR IGNORE INTO movies_keyword (tmdb_id, keyword_id)
                VALUES (?, ?)
            ''', (int(info['id']), k_id))
            conn.commit()

    elif option.strip() == '2':
        cursor.execute('''
            SELECT m.title, r.score, r.comment, r.created_at
            FROM movies m
            JOIN my_ratings r ON m.tmdb_id = r.tmdb_id
            ORDER BY r.created_at DESC
        ''')
        ratings = cursor.fetchall()
        if ratings:
            for title, score, comment, created_at in ratings:
                print(f"{title} - Puntuación: {score} - Comentario: {comment} - Fecha: {created_at}")
        else:
            print("No has calificado ninguna película aún.")
    elif option.strip() == '4':
        print("Saliendo del programa. ¡Hasta luego!")
        conn.close()
        break
    else:
        print("Opción no válida. Por favor, seleccione una opción del 1 al 4.")


