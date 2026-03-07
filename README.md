# Movie Root 🎬 (#ROOT Ecosystem)
Movie Root es el centro de mando para tu consumo visual. Es una aplicación de escritorio desarrollada en Python con una interfaz gráfica en Tkinter, diseñada para que gestiones tu registro de películas y series sin perder tiempo en la mediocridad.
Este módulo del ecosistema #ROOT filtra el ruido del contenido comercial y utiliza tu propio criterio (notas y comentarios) para recomendarte solo obras que cumplan con el estándar Global Tier.
## 🚀 Características
 * Interfaz Gráfica (GUI): Experiencia visual intuitiva construida con Tkinter, dejando atrás la limitación de la línea de comandos.
 * Registro Dual Inteligente: Soporte completo para Películas y Series de TV, permitiéndote separar tu cine de élite de tus maratones de series.
 * Integración con TMDB: Conexión quirúrgica con la API de The Movie Database para obtener posters, sinopsis y metadatos reales.
 * Persistencia Local: Gestión de datos rápida y segura mediante SQLite, manteniendo tu historial bajo tu control total.
 * Algoritmo de Recomendación: Motor lógico que analiza tus preferencias (notas 7+) y palabras clave para encontrar tu próximo objetivo visual.
## 🛠️ Instalación
 * Clona el repositorio:
   git clone https://github.com/tu-usuario/movie-root.git

 * Entorno Virtual:
   python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
pip install -r requirements.txt

 * Configuración de API:
   * Crea un archivo .env en la raíz.
   * Añade tu clave: TMDB_KEY=tu_api_key_aqui
📖 Uso
Para lanzar el centro de mando #ROOT, simplemente ejecuta el script principal desde tu terminal:
python main.py
