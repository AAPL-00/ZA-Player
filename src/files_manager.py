import os
import asyncio
from pathlib import Path
from mutagen._file import File


AUDIO_EXTENSIONS = {"mp3", "flac", "wav", "aac", "m4a", "ogg", "wma", "alac", "opus"}


async def find_audio_files(root_path: str) -> list[str]:
    def blocking_walk() -> list[str]:
        if not os.path.isdir(root_path):
            raise FileNotFoundError(f"Ruta inexistente: {root_path}")

        return [
            str(Path(dirpath) / f)
            for dirpath, _, filenames in os.walk(root_path)
            for f in filenames
            if f.lower().rsplit('.', 1)[-1] in AUDIO_EXTENSIONS
        ]

    try:
        return await asyncio.to_thread(blocking_walk)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        return []

def extract_metadata(path: str) -> tuple[str, str, str, float]:
    audio = File(path)
    if audio is None:
        return ("Desconocido", "Desconocido", "Desconocido", 0.0)

    tags = audio.tags or {}

    title = str(tags.get("TIT2") or tags.get("title") or Path(path).stem)
    artist = str(tags.get("TPE1") or tags.get("artist") or "Desconocido")
    album = str(tags.get("TALB") or tags.get("album") or "Desconocido")
    duration = round(getattr(audio.info, "length", 0.0), 2)

    return (title, album, artist, duration)
