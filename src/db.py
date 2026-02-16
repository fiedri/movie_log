import sqlite3

def crear_base_de_datos():
    conn = sqlite3.connect('movie_root.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS media (
            tmdb_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            overview TEXT,
            release_date TIMESTAMP,
            director TEXT,
            average_score REAL,
            media_type TEXT CHECK(media_type IN ('movie', 'tv')) NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS genres (
            genre_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keyword (
            keyword_id INTEGER PRIMARY KEY,
            keyword TEXT UNIQUE NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS my_ratings (
            rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tmdb_id INTEGER,
            score REAL CHECK(score >= 1 AND score <= 10),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            comment TEXT,
            FOREIGN KEY (tmdb_id) REFERENCES media (tmdb_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS media_genres (
            tmdb_id INTEGER,
            genre_id INTEGER,
            PRIMARY KEY (tmdb_id, genre_id),
            FOREIGN KEY (tmdb_id) REFERENCES media (tmdb_id),
            FOREIGN KEY (genre_id) REFERENCES genres (genre_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS media_keyword (
            tmdb_id INTEGER,
            keyword_id INTEGER,
            PRIMARY KEY (tmdb_id, keyword_id),
            FOREIGN KEY (tmdb_id) REFERENCES media (tmdb_id),
            FOREIGN KEY (keyword_id) REFERENCES keyword (keyword_id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Arquitectura #ROOT desplegada con éxito.")

if __name__ == "__main__":
    crear_base_de_datos()
