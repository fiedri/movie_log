import sqlite3

def crear_base_de_datos():
    # Conexión al archivo de base de datos
    conn = sqlite3.connect('movie_root.db')
    cursor = conn.cursor()

    # Activar soporte para claves foráneas
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Tabla de Películas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            tmdb_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            overview TEXT,
            relaese_date TIMESTAMP,
            director TEXT,
            average_score REAL
        )
    ''')

    # 2. Tabla de Géneros
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS genres (
            genre_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # 3. Tabla de Keywords
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keyword (
            keyword_id INTEGER PRIMARY KEY,
            keyword TEXT UNIQUE NOT NULL
        )
    ''')

    # 4. Tabla de tus Calificaciones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS my_ratings (
            rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tmdb_id INTEGER,
            score REAL CHECK(score >= 1 AND score <= 10),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            comment TEXT,
            FOREIGN KEY (tmdb_id) REFERENCES movies (tmdb_id)
        )
    ''')

    # 5. Tablas Intermedias (Relaciones Many-to-Many)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies_genres (
            tmdb_id INTEGER,
            genre_id INTEGER,
            PRIMARY KEY (tmdb_id, genre_id),
            FOREIGN KEY (tmdb_id) REFERENCES movies (tmdb_id),
            FOREIGN KEY (genre_id) REFERENCES genres (genre_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies_keyword (
            tmdb_id INTEGER,
            keyword_id INTEGER,
            PRIMARY KEY (tmdb_id, keyword_id),
            FOREIGN KEY (tmdb_id) REFERENCES movies (tmdb_id),
            FOREIGN KEY (keyword_id) REFERENCES keyword (keyword_id)
        )
    ''')
    #
    conn.commit()
    conn.close()
    print("Arquitectura #ROOT desplegada con éxito.")

if __name__ == "__main__":
    crear_base_de_datos()
