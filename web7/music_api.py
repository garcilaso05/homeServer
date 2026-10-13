from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ytmusicapi import YTMusic
import yt_dlp
import requests
import os
import tempfile
import shutil

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
yt = YTMusic()

class TrackInfo(BaseModel):
    youtube_id: str
    titulo: str
    artista: str
    portada: str
    duracion: str

def cleanup_temp(path: str):
    """Borra la carpeta temporal después de enviar el archivo al móvil"""
    try:
        shutil.rmtree(os.path.dirname(path), ignore_errors=True)
    except:
        pass

@app.get("/api/search")
def search(q: str):
    try:
        results = yt.search(q, filter="songs", limit=20)
        tracks = []
        for r in results:
            artist_id = r["artists"][0].get("id") if r.get("artists") else None
            tracks.append({
                "youtube_id": r["videoId"],
                "title": r["title"],
                "artist": r["artists"][0]["name"] if r.get("artists") else "Desconocido",
                "artist_id": artist_id,
                "cover": r["thumbnails"][-1]["url"].replace("w120-h120", "w512-h512") if r.get("thumbnails") else "",
                "duration": r.get("duration", "0:00")
            })
        return tracks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stream")
def stream(id: str):
    ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={id}", download=False)
            return RedirectResponse(info['url'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/artist-radio")
def artist_radio(artist_id: str):
    try:
        artist = yt.get_artist(artist_id)
        songs = artist.get("songs", {}).get("results", [])
        tracks = []
        for r in songs:
            tracks.append({
                "youtube_id": r["videoId"],
                "title": r["title"],
                "artist": artist["name"],
                "artist_id": artist_id,
                "cover": r["thumbnails"][-1]["url"].replace("w120-h120", "w512-h512") if r.get("thumbnails") else "",
                "duration": r.get("duration", "0:00")
            })
        return tracks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/save-to-db")
def save_to_db(track: TrackInfo):
    """Descarga la canción localmente y la sube a PocketBase"""
    try:
        temp_dir = tempfile.mkdtemp()
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': os.path.join(temp_dir, "%(id)s.%(ext)s"),
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={track.youtube_id}", download=True)
            ext = info.get('ext', 'm4a')
            file_path = os.path.join(temp_dir, f"{track.youtube_id}.{ext}")

        # Subir a PocketBase (localhost)
        pb_url = "http://127.0.0.1:8090/api/collections/descargas/records"
        with open(file_path, 'rb') as f:
            files = {'archivo': (f"{track.titulo}.{ext}", f, f"audio/{ext}")}
            data = {
                'youtube_id': track.youtube_id, 'titulo': track.titulo,
                'artista': track.artista, 'portada': track.portada, 'duracion': track.duracion
            }
            res = requests.post(pb_url, data=data, files=files)
        
        cleanup_temp(file_path)
        if res.status_code >= 400: raise Exception(res.text)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download-local")
def download_local(id: str, title: str, background_tasks: BackgroundTasks):
    """Descarga la canción y se la sirve al navegador del usuario (Móvil/PC) para guardarla"""
    try:
        temp_dir = tempfile.mkdtemp()
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': os.path.join(temp_dir, "%(id)s.%(ext)s"),
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={id}", download=True)
            ext = info.get('ext', 'm4a')
            file_path = os.path.join(temp_dir, f"{id}.{ext}")
        
        filename = f"{title}.{ext}".replace("/", "_")
        background_tasks.add_task(cleanup_temp, file_path)
        return FileResponse(file_path, filename=filename, media_type="audio/mp4")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
