from src.utils.search import search_media, get_media_details, get_recommendations
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_KEY")

conn = sqlite3.connect('movie_root.db')
cursor = conn.cursor()

print("Bienvenido a Movie Root, el santuario de tu Ego cinéfilo.")

while True:
    print("\n--- Menú Principal ---")
    print("1. Agregar contenido (Película/Serie)")
    print("2. Ver mi biblioteca")
    print("3. Ver recomendaciones")
    print("4. Salir")

    option = input("Seleccione una opción: ")
    
    if option.strip() == '1':
        print("\n¿Qué deseas agregar?")
        print("1. Película")
        print("2. Serie")
        type_choice = input("Seleccione (1 o 2): ")
        
        media_type = "movie" if type_choice == '1' else "tv"
        name = input(f"Ingrese el nombre de la { 'película' if media_type == 'movie' else 'serie' }: ")
        
        info = search_media(name, media_type)
        if isinstance(info, str) or info is None:
            print(info if info else "Operación cancelada.")
            continue
            
        details = get_media_details(info['id'], media_type)
        if not details:
            print("No se pudieron obtener los detalles.")
            continue

        try:
            cursor.execute('''
                INSERT OR IGNORE INTO media (tmdb_id, title, overview, average_score, release_date, director, media_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                int(details['tmdb_id']), 
                details['title'], 
                details['overview'], 
                float(details['vote_average']), 
                details['release_date'], 
                details['director'],
                details['media_type']
            ))
            conn.commit()

            score = input(f"¿Qué puntuación le das a '{details['title']}'? (1-10): ")
            comment = input("¿Quieres agregar un comentario? (opcional): ")
            
            cursor.execute('''
                INSERT INTO my_ratings (tmdb_id, score, comment)
                VALUES (?, ?, ?)
            ''', (int(details['tmdb_id']), float(score), comment))
            conn.commit()
            
            for genre in details['genres']:
                cursor.execute('INSERT OR IGNORE INTO genres (genre_id, name) VALUES (?, ?)', (int(genre['id']), genre['name']))
                cursor.execute('INSERT OR IGNORE INTO media_genres (tmdb_id, genre_id) VALUES (?, ?)', (int(details['tmdb_id']), genre['id']))
            
            for keyword in details['keywords']:
                cursor.execute('INSERT OR IGNORE INTO keyword (keyword_id, keyword) VALUES (?, ?)', (int(keyword['id']), keyword['name']))
                cursor.execute('INSERT OR IGNORE INTO media_keyword (tmdb_id, keyword_id) VALUES (?, ?)', (int(details['tmdb_id']), keyword['id']))
            
            conn.commit()
            print(f"\n¡'{details['title']}' guardado con éxito!")
            
        except sqlite3.Error as e:
            print(f"Error en la base de datos: {e}")

    elif option.strip() == '2':
        cursor.execute('''
            SELECT m.title, m.media_type, r.score, r.comment, r.created_at
            FROM media m
            JOIN my_ratings r ON m.tmdb_id = r.tmdb_id
            ORDER BY r.created_at DESC
        ''')
        ratings = cursor.fetchall()
        if ratings:
            print("\n--- Tu Biblioteca ---")
            for title, m_type, score, comment, created_at in ratings:
                tipo = "[PELI]" if m_type == 'movie' else "[SERIE]"
                print(f"{tipo} {title} - Puntuación: {score} - Fecha: {created_at}")
                if comment: print(f"   Nota: {comment}")
        else:
            print("\nNo has calificado nada aún.")

    elif option.strip() == '3':
        print("\n--- Recomendaciones ---")
        print("1. Películas")
        print("2. Series")
        recom_choice = input("Seleccione (1 o 2): ")
        recom_type = "movie" if recom_choice == '1' else "tv"
        
        recoms = get_recommendations(cursor, recom_type)
        
        if isinstance(recoms, list) and recoms:
            start_index = 0
            while start_index < len(recoms):
                batch = recoms[start_index : start_index + 5]
                for i, p in enumerate(batch):
                    print(f"[{start_index + i + 1}] {p['title']} (Nota: {p.get('vote_average', 'N/A')})")
                    print(f"    Sinopsis: {p.get('overview', 'Sin descripción')[:100]}...")
                
                start_index += 5
                if start_index < len(recoms):
                    more = input("\n¿Ver más? (s/n): ")
                    if more.lower() != 's':
                        break
                else:
                    print("\nNo hay más recomendaciones.")
        else:
            print(recoms if isinstance(recoms, str) else "No se encontraron resultados.")

    elif option.strip() == '4':
        print("Saliendo de Movie-log Root. ¡Hasta la próxima!")
        conn.close()
        break
    else:
        print("Opción no válida.")
