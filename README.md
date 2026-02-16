# Movie Root 🎬

**Movie Root** es el santuario personal para tu Ego cinéfilo. Una aplicación de línea de comandos (CLI) que te permite gestionar tu propio registro de películas y series, calificarlas y recibir recomendaciones inteligentes basadas en tus gustos de élite.

> ⚠️ **Nota de la Versión**: Esta es una **versión de prueba** funcional bajo CLI. Se planea la implementación de una interfaz gráfica en futuras actualizaciones para mejorar la experiencia visual.

## 🚀 Características

- **Registro Dual**: Soporte completo para Películas y Series de TV.
- **Integración con TMDB**: Búsqueda automática de metadatos.
- **Base de Datos Unificada**: Almacenamiento local en SQLite.
- **Motor de Recomendación**: Aprende de tus preferencias (nota 7+) con un sistema de barajado para ofrecer variedad.

## 🛠️ Instalación

1. Clona el repositorio.
2. Crea un entorno virtual e instala las dependencias:
   ```bash
   python -m venv env
   source env/bin/activate  # En Windows: env\Scripts\activate
   pip install -r requirements.txt
   ```
3. Configura tu API Key de TMDB:
   - Crea un archivo `.env` en la raíz del proyecto.
   - Añade tu clave: `TMDB_KEY=tu_api_key_aqui`

## 📖 Uso

1. **Inicializar la Base de Datos**:
   ```bash
   python src/db.py
   ```

2. **Lanzar la aplicación**:
   ```bash
   python main.py
   ```

---
*Desarrollado para cinéfilos que saben lo que quieren.*
