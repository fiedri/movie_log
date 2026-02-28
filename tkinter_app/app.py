import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import os
import sys

# Ensure the app can find the src modules in the root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.search import get_recommendations
from tkinter_app.gui_utils import search_media_gui, get_media_details_gui

class MovieRootGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Root - Tu Ego Cinéfilo")
        self.root.geometry("800x600")

        # Database connection
        self.db_path = os.path.join(os.path.dirname(__file__), "..", "movie_root.db")
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # UI Components
        self.tab_control = ttk.Notebook(root)
        
        self.tab_library = ttk.Frame(self.tab_control)
        self.tab_add = ttk.Frame(self.tab_control)
        self.tab_recommendations = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab_library, text='Biblioteca')
        self.tab_control.add(self.tab_add, text='Agregar')
        self.tab_control.add(self.tab_recommendations, text='Recomendaciones')
        self.tab_control.pack(expand=1, fill="both")
        
        self.setup_library_tab()
        self.setup_add_tab()
        self.setup_recommendations_tab()

    def setup_library_tab(self):
        # Refresh button
        self.btn_refresh = tk.Button(self.tab_library, text="Actualizar Biblioteca", command=self.load_library)
        self.btn_refresh.pack(pady=10)
        
        # Treeview for the library
        columns = ("Tipo", "Título", "Nota", "Comentario", "Fecha")
        self.tree_library = ttk.Treeview(self.tab_library, columns=columns, show='headings')
        for col in columns:
            self.tree_library.heading(col, text=col)
            self.tree_library.column(col, width=100)
        
        self.tree_library.pack(expand=True, fill="both", padx=10, pady=10)
        self.load_library()

    def load_library(self):
        # Clear existing
        for i in self.tree_library.get_children():
            self.tree_library.delete(i)
            
        self.cursor.execute('''
            SELECT m.media_type, m.title, r.score, r.comment, r.created_at
            FROM media m
            JOIN my_ratings r ON m.tmdb_id = r.tmdb_id
            ORDER BY r.created_at DESC
        ''')
        ratings = self.cursor.fetchall()
        for media_type, title, score, comment, created_at in ratings:
            tipo = "Peli" if media_type == 'movie' else "Serie"
            self.tree_library.insert("", "end", values=(tipo, title, score, comment, created_at))

    def setup_add_tab(self):
        # Media type selector
        frame_search = tk.Frame(self.tab_add)
        frame_search.pack(pady=10, padx=10, fill="x")
        
        tk.Label(frame_search, text="Buscar:").pack(side="left")
        self.entry_search = tk.Entry(frame_search)
        self.entry_search.pack(side="left", fill="x", expand=True, padx=5)
        
        self.media_type_var = tk.StringVar(value="movie")
        tk.Radiobutton(frame_search, text="Película", variable=self.media_type_var, value="movie").pack(side="left")
        tk.Radiobutton(frame_search, text="Serie", variable=self.media_type_var, value="tv").pack(side="left")
        
        self.btn_search = tk.Button(frame_search, text="Buscar", command=self.perform_search)
        self.btn_search.pack(side="left", padx=5)
        
        # List of results
        self.listbox_results = tk.Listbox(self.tab_add)
        self.listbox_results.pack(expand=True, fill="both", padx=10, pady=5)
        
        self.btn_add_selected = tk.Button(self.tab_add, text="Añadir Seleccionado", command=self.add_selected_media)
        self.btn_add_selected.pack(pady=10)
        
        self.search_results_data = []

    def perform_search(self):
        query = self.entry_search.get()
        if not query:
            return
        
        media_type = self.media_type_var.get()
        results = search_media_gui(query, media_type)
        
        self.listbox_results.delete(0, tk.END)
        self.search_results_data = results
        
        for item in results[:10]:
            title = item.get('title') if media_type == "movie" else item.get('name')
            date = item.get('release_date' if media_type == "movie" else 'first_air_date', "N/A")
            self.listbox_results.insert(tk.END, f"{title} ({date[:4] if date else 'N/A'})")

    def add_selected_media(self):
        selection = self.listbox_results.curselection()
        if not selection:
            messagebox.showwarning("Selección", "Elige algo de la lista.")
            return
            
        index = selection[0]
        media_info = self.search_results_data[index]
        media_type = self.media_type_var.get()
        
        details = get_media_details_gui(media_info['id'], media_type)
        if not details:
            messagebox.showerror("Error", "No se pudieron obtener detalles.")
            return
            
        # Add to DB
        score = simpledialog.askfloat("Puntuación", f"¿Qué puntuación le das a '{details['title']}'? (1-10)", minvalue=1, maxvalue=10)
        if score is None: return
        
        comment = simpledialog.askstring("Comentario", "¿Quieres agregar un comentario? (opcional)")
        
        try:
            self.cursor.execute('''
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
            
            self.cursor.execute('''
                INSERT INTO my_ratings (tmdb_id, score, comment)
                VALUES (?, ?, ?)
            ''', (int(details['tmdb_id']), float(score), comment))
            
            for genre in details['genres']:
                self.cursor.execute('INSERT OR IGNORE INTO genres (genre_id, name) VALUES (?, ?)', (int(genre['id']), genre['name']))
                self.cursor.execute('INSERT OR IGNORE INTO media_genres (tmdb_id, genre_id) VALUES (?, ?)', (int(details['tmdb_id']), genre['id']))
            
            for keyword in details['keywords']:
                self.cursor.execute('INSERT OR IGNORE INTO keyword (keyword_id, keyword) VALUES (?, ?)', (int(keyword['id']), keyword['name']))
                self.cursor.execute('INSERT OR IGNORE INTO media_keyword (tmdb_id, keyword_id) VALUES (?, ?)', (int(details['tmdb_id']), keyword['id']))
            
            self.conn.commit()
            messagebox.showinfo("Éxito", f"'{details['title']}' guardado con éxito.")
            self.load_library()
        except sqlite3.Error as e:
            messagebox.showerror("Error DB", str(e))

    def setup_recommendations_tab(self):
        frame_recom = tk.Frame(self.tab_recommendations)
        frame_recom.pack(pady=10, padx=10, fill="x")
        
        self.recom_type_var = tk.StringVar(value="movie")
        tk.Radiobutton(frame_recom, text="Películas", variable=self.recom_type_var, value="movie").pack(side="left")
        tk.Radiobutton(frame_recom, text="Series", variable=self.recom_type_var, value="tv").pack(side="left")
        
        tk.Button(frame_recom, text="Obtener Recomendaciones", command=self.load_recommendations).pack(side="left", padx=10)
        
        self.tree_recom = ttk.Treeview(self.tab_recommendations, columns=("Título", "Nota", "Sinopsis"), show='headings')
        self.tree_recom.heading("Título", text="Título")
        self.tree_recom.heading("Nota", text="Nota")
        self.tree_recom.heading("Sinopsis", text="Sinopsis")
        self.tree_recom.column("Sinopsis", width=400)
        self.tree_recom.pack(expand=True, fill="both", padx=10, pady=10)

    def load_recommendations(self):
        for i in self.tree_recom.get_children():
            self.tree_recom.delete(i)
            
        recom_type = self.recom_type_var.get()
        recoms = get_recommendations(self.cursor, recom_type)
        
        if isinstance(recoms, list):
            for p in recoms:
                self.tree_recom.insert("", "end", values=(p['title'], p.get('vote_average', 'N/A'), p.get('overview', '')[:100] + "..."))
        else:
            messagebox.showinfo("Recomendaciones", str(recoms))

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieRootGUI(root)
    root.mainloop()
