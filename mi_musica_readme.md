# MiMusica: Tu Propio "Spotify" Privado y Gratuito

**MiMusica** es la joya de la corona de este servidor doméstico. Es una aplicación web progresiva (PWA) de streaming musical que te permite acceder a un catálogo infinito de música sin pagar suscripciones, sin anuncios y con el máximo respeto a tu privacidad.

Si alguna vez has querido tener tu propia plataforma de música bajo demanda alojada en casa, esto es exactamente lo que buscas.

## ¿Cómo funciona por debajo?

A diferencia de los servicios comerciales, MiMusica no indexa millones de canciones en tu disco duro (lo cual requeriría terabytes de espacio). En su lugar, actúa como un puente inteligente hacia el catálogo de **YouTube Music**:

1. **El Buscador:** Cuando buscas una canción, el backend en Python utiliza `ytmusicapi` para consultar silenciosamente la base de datos de YouTube y devolverte los metadatos (portadas de alta calidad, artistas, duraciones).
2. **El Stream Directo:** Al darle al "Play", nuestro servidor utiliza `yt-dlp` para interceptar la URL real del flujo de audio (en formato de alta calidad WebM/Opus o AAC) directamente desde los servidores de Google.
3. **Cero Publicidad:** Como el backend extrae el archivo de audio puro sin cargar los reproductores comerciales ni los scripts de rastreo de YouTube, los anuncios simplemente no existen.

## Características Principales

*   **Reproducción Sin Pausas (Gapless Playback):** El reproductor incluye un sistema de precarga inteligente. Cuando faltan unos 15 segundos para que termine la pista actual, el navegador solicita la siguiente canción al servidor por debajo. El resultado es una transición perfecta sin tiempos de carga.
*   **Letras en Directo (Sincronizadas):** Se conecta con APIs públicas libres (como LrcLib) para buscar las letras de la canción actual. La letra baja automáticamente de forma sincronizada con el tiempo de reproducción.
*   **Deslizador de Tiempo Interactivo (SeekBar):** Puedes arrastrar la barra de progreso para saltar a cualquier punto de la canción al instante, y la letra se re-sincronizará mágicamente con ese segundo exacto.
*   **Descargas Locales y en el Servidor:** ¿Te gusta mucho un disco? Puedes descargarlo como archivo `m4a` a la memoria de tu teléfono, o pulsar "Guardar en el Servidor" para que se almacene físicamente en PocketBase (en la colección `descargas`).
*   **Gestión Dual de Playlists:**
    *   *Playlists de Streaming:* Listas de reproducción estándar que guardan las referencias de las canciones en streaming.
    *   *Playlists Locales:* Listas que agrupan exclusivamente los archivos físicos que has descargado en el servidor, garantizando que nunca perderás esa música aunque desaparezca de internet (colección `playlists_locales`).
*   **Pantalla de Inicio de Descubrimiento:** Al entrar a la web no verás un vacío negro. El sistema te recomienda música al azar basándose en tus descargas previas para que la música empiece a sonar con un solo clic.
*   **Sugerencias de Búsqueda:** Autocompletado inteligente mientras escribes para encontrar tu música más rápido.
*   **Integración Nativa Móvil:** Gracias a la *Media Session API*, cuando apagas la pantalla de tu móvil o bloqueas tu PC, MiMusica sigue sonando en segundo plano, mostrando la carátula y permitiéndote pasar de canción desde los controles nativos del sistema. Diseño UI/UX oscuro, cristalino y 100% optimizado para pantallas táctiles.

## Tecnologías Utilizadas
*   **Frontend:** HTML5, CSS3 (Glassmorphism), JavaScript Vanilla (Fetch API, HTMLAudioElement).
*   **Backend:** Python 3 (FastAPI, Uvicorn, yt-dlp, ytmusicapi).
*   **Base de Datos:** PocketBase (Colecciones: `playlists`, `tracks`, `descargas`, `playlists_locales`).