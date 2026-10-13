# HOMEsERVER: Servidor Doméstico 100% Privado y Ligero

Este proyecto nace con un objetivo claro: **revivir un ordenador o portátil antiguo** que ya no utilizas y convertirlo en un servidor doméstico personal, seguro y de bajo consumo.

A diferencia de los servidores tradicionales, este proyecto se centra en la **privacidad extrema**. No abriremos ni un solo puerto de nuestro router a internet. Utilizaremos una red privada virtual (VPN en malla) para que los servicios que alojemos solo sean accesibles por nosotros mismos, desde nuestros dispositivos autorizados, estemos donde estemos.

Aquí encontrarás todo lo necesario para montar tu propia infraestructura y desplegar un ecosistema de aplicaciones web ligeras (sin depender de nubes comerciales).

---

## 1. Requisitos e Instalación del Sistema Operativo

Para que un ordenador viejo funcione fluido y consuma poca energía, necesitamos un sistema operativo sólido y sin elementos innecesarios. Usaremos **Debian Linux**.

### Preparación del USB (Rufus)
1. Descarga la imagen ISO de **Debian (versión netinst)** desde su web oficial. Es una imagen muy pequeña que descarga lo necesario durante la instalación.
2. Descarga **Rufus** (si estás en Windows) o usa BalenaEtcher.
3. Conecta un pendrive USB, abre Rufus, selecciona la ISO de Debian y flashea la unidad.

### Instalación de Debian (Sin Interfaz Gráfica)
1. Arranca tu ordenador viejo desde el USB.
2. Sigue los pasos del instalador (idioma, teclado, particionado de disco guiado borrando todo el disco).
3. **EL PASO MÁS IMPORTANTE:** Llegará un momento en que te pedirá seleccionar los programas a instalar (*Software selection*).
   - **DESMARCA** "Debian desktop environment", "GNOME", "KDE", etc. No queremos interfaz gráfica, solo consume RAM.
   - **MARCA** "SSH server" (fundamental para controlarlo desde otro PC) y "standard system utilities".
4. Termina la instalación, saca el USB y reinicia. Ahora tendrás una pantalla negra con letras blancas: tu servidor está listo.

---

## 2. Conectividad y Seguridad

Dado que el servidor no tiene pantalla, todo el control lo haremos desde nuestro ordenador principal mediante SSH (`ssh usuario@ip-del-servidor`). 

### Tailscale (Nuestra Nube Privada)
Para no abrir puertos en el router (lo cual es peligroso), usaremos **Tailscale**. Es una VPN tipo malla basada en WireGuard.
1. Instala Tailscale en el servidor ejecutando: `curl -fsSL https://tailscale.com/install.sh | sh`
2. Ejecuta `sudo tailscale up` y abre el enlace que te da en tu móvil u ordenador principal para autenticar el servidor.
3. Instala Tailscale en tu móvil y portátil. Ahora todos están en la misma red privada. Puedes acceder a tu servidor usando su IP de Tailscale (ej. `100.x.x.x`) o su nombre mágico de red (MagicDNS, ej. `debianruchi`).

### Cortafuegos (UFW)
Para blindar el servidor frente a cualquier usuario que esté conectado a la misma red Wi-Fi de tu casa, configuraremos un Firewall básico:
```bash
sudo apt install ufw
sudo ufw default deny incoming  # Bloquea todo lo que entra por defecto
sudo ufw default allow outgoing # Permite que el servidor salga a internet
sudo ufw allow ssh  # Salvavidas: Permite conexiones SSH locales
sudo ufw allow in on tailscale0 # Permite TODO el tráfico, pero SOLO si viene por la VPN
sudo ufw enable # Activar cortafuegos
```

---

## 3. Infraestructura Base

El corazón de nuestro servidor se compone de dos herramientas extremadamente ligeras, escritas en Go:

1. **Caddy (Servidor Web):** Sustituye a alternativas más pesadas como Apache o Nginx. Caddy se encargará de servir nuestros archivos HTML en diferentes puertos (80, 81, 82...). Su configuración se hace en el archivo `/etc/caddy/Caddyfile`.
2. **PocketBase (Base de Datos / Backend):** Una maravilla todo-en-uno. Es una base de datos NoSQL con panel de administración y API lista para usar. Lo ejecutamos en el puerto `8090` y almacena toda la información (textos, recordatorios y archivos) en la carpeta `/home/usuario/pb_data`.

---

## 4. El Ecosistema de Aplicaciones (Webs)

En este repositorio (en las carpetas de código adjuntas) encontrarás los archivos HTML individuales para montar estos 7 servicios. La filosofía es **1 servicio = 1 archivo HTML** (con CSS y JS integrados) que se conecta a PocketBase mediante peticiones `fetch`.

*   **Web 1 (Puerto 80) - Centro de Juegos:** Una web ligera con juegos en JavaScript (como Sudoku) para pasar el rato, adaptada a pantallas táctiles.
*   **Web 2 (Puerto 81) - Gestor de Recordatorios:** Una app CRUD completa. Crea, edita, borra y marca tareas como completadas guardándolas en PocketBase.
*   **Web 3 (Puerto 82) - Galería de Fotos:** Sistema de subida múltiple de imágenes empaquetadas como "posts" o memorias.
*   **Web 4 (Puerto 83) - Nube Privada (Drive):** Un sistema de archivos virtual. Simula carpetas padre-hijo usando la base de datos NoSQL para organizar PDFs, apuntes y documentos.
* **Web 5 (Puerto 84) - Buzón Efímero:** Sube un archivo desde el móvil y al descargarlo en el PC, se elimina permanentemente del servidor. Ideal para pasarse archivos sin dejar basura. 
  👉 [Leer la documentación técnica del Buzón Efímero](buzon_efimero_readme.md)
  *   **Web 6 (Puerto 85) - Gestor de Snippets:** Un baúl para programadores. Guarda tus comandos de Linux, configuraciones y fragmentos de código con botón de copiar al portapapeles.
* **Web 7 (Puerto 86) - MiMusica:** La joya de la corona. Un reproductor de música sin anuncios (estilo Spotify) con backend en Python. Permite reproducción sin pausas (Gapless), descargas, letras sincronizadas y control desde la pantalla de bloqueo.
  👉 [Leer la documentación técnica de MiMusica](mi_musica_readme.md)
---

## 5. Configuración de Colecciones en PocketBase

Para que las aplicaciones web funcionen correctamente, es imprescindible crear las siguientes colecciones en PocketBase y configurar sus campos exactos.

Regla general obligatoria: En todas las colecciones descritas a continuación, debes acceder a la pestaña API Rules, desbloquear los 5 candados (List, View, Create, Update, Delete) dejándolos en blanco y guardar los cambios.
### Web 1: Juegos

Nota: Esta aplicación se ejecuta íntegramente en el navegador del cliente mediante JavaScript y no requiere base de datos ni conexión con PocketBase.

### Web 2: App de Recordatorios

Nombre de la colección: recordatorios

Campos:

- Nombre (Tipo: Text)

- Descripcion (Tipo: Text)

- Fecha_Hora (Tipo: Date)

- URL (Tipo: URL)

- Completado (Tipo: Bool)

### Web 3: Galería de Fotos (Paquetes)

Nombre de la colección: MisFotos

Campos:

- Titulo (Tipo: Text - Marcado como obligatorio/Nonempty)

- Descripcion (Tipo: Text)

- Fecha (Tipo: Date)

- Imagenes (Tipo: File - Marcado como Múltiple, límite 99, y obligatorio/Nonempty)

### Web 4: Mi Nube Privada (Sistema de Archivos)

Nombre de la colección: Drive

Campos:

- nombre (Tipo: Text)

- es_carpeta (Tipo: Bool)

- padre (Tipo: Text)

- archivo (Tipo: File - Límite de tamaño: 0 para permitir subidas sin restricción)

### Web 5: Buzón Efímero (Transfer temporal)

Nombre de la colección: Transfer

Campos:

- nombre (Tipo: Text)

- archivo (Tipo: File - Límite de tamaño: 0 para archivos grandes)

### Web 6: Gestor de Snippets y Configuraciones

Nombre de la colección: Snippets

Campos:

- Titulo (Tipo: Text)

- Lenguaje (Tipo: Text)

- Codigo (Tipo: Text)

- Descripcion (Tipo: Text)

### Web 7: Reproductor de Streaming Musical

Colección 1: playlists

- nombre (Tipo: Text)

- descripcion (Tipo: Text)

Colección 2: tracks

- playlist_id (Tipo: Text - Almacena el ID de la lista padre)

- youtube_id (Tipo: Text)

- titulo (Tipo: Text)

- artista (Tipo: Text)

- portada (Tipo: URL)

- duracion (Tipo: Text)

Colección 3: descargas

- youtube_id (Tipo: Text)

- titulo (Tipo: Text)

- artista (Tipo: Text)

- portada (Tipo: Text - Almacena la URL de la carátula)

- duracion (Tipo: Text)

- archivo (Tipo: File - Límite de tamaño: 0)

Colección 4: playlists_locales

- nombre (Tipo: Text)

- descargas (Tipo: Relation - Múltiple, apuntando a la colección descargas)

## 6. Mantenimiento y Autorreparación

Para no tener que recordar comandos de Linux, creamos un script llamado `doctor.sh`. Si alguna vez se va la luz o el servidor se queda atascado, al entrar por SSH solo hay que ejecutar `sudo ./doctor.sh`.

```bash
#!/bin/bash
echo "Iniciando Autodiagnóstico del Servidor..."
# 1. Comprobar permisos de la BD
chown -R usuario:usuario /home/usuario/pb_data 2>/dev/null
# 2. Limpiar procesos colgados
killall pocketbase 2>/dev/null
sleep 1
# 3. Recargar y reiniciar servicios
systemctl daemon-reload
systemctl enable caddy --now
systemctl restart caddy
systemctl enable pocketbase --now
systemctl restart pocketbase
echo "Diagnóstico y reparación finalizados."
```

---

## 7. Solución de Problemas (Troubleshooting)

Durante el desarrollo nos topamos con varios retos técnicos interesantes. Aquí explicamos cómo los solucionamos:

### 1. Error 404 al subir webs (Permisos de Linux)
Al transferir archivos HTML por SSH (`scp`), estos llegan con permisos restrictivos. Caddy (el servidor web) no puede leerlos y lanza un error 404.
**Solución:** Otorgar permisos de lectura global y ejecución a la carpeta:
```bash
sudo chmod 755 /var/www/web1
sudo chmod 644 /var/www/web1/index.html
```

### 2. El backend de música falla (Error 500 / Fallo de DNS)
De repente, Python no puede descargar música y el sistema reporta `Fallo temporal en la resolución del nombre`. Esto ocurre porque Tailscale a veces sobreescribe el gestor de DNS del sistema (`/etc/resolv.conf`) y pierde la conexión temporalmente si hay microcortes en el router.
**Solución:** Forzar el DNS de Google manualmente y reiniciar el túnel:
```bash
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf > /dev/null
sudo systemctl restart tailscaled
```

### 3. Error en Firefox: `SSL_ERROR_RX_RECORD_TOO_LONG`
Al intentar entrar a `http://tuservidor:85`, Firefox bloquea la página entera.
**Causa:** Firefox tiene activado el "Modo solo HTTPS" e intenta forzar una conexión cifrada (`https://`), pero Caddy en nuestra red local privada está sirviendo en HTTP plano.
**Solución:** En los ajustes de Firefox -> Privacidad y seguridad -> Modo solo HTTPS -> "Gestionar excepciones". Añade la IP de tu servidor o su nombre de Tailscale para indicarle al navegador que no intente forzar el candado SSL en esa ruta interna.

---

## 8. Próximos Pasos
Este proyecto está vivo. La ventaja de este ecosistema es que añadir un nuevo servicio cuesta menos de 5 minutos (solo requiere crear una tabla en PocketBase, diseñar un archivo HTML y abrir un puerto en Caddy). 

¡Cualquier sugerencia, *Pull Request* o nueva idea de servicio es bienvenida!