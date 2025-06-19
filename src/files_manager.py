import os
import asyncio
from pathlib import Path
from mutagen._file import File


AUDIO_EXTENSIONS = {"mp3", "flac", "wav", "aac", "m4a", "ogg", "wma", "alac", "opus"}


async def find_audio_files(root_path: str) -> list[str]:
    def walk() -> list[str]:
        path = Path(root_path)
        if not path.is_dir():
            raise FileNotFoundError(f"Ruta inexistente: {root_path}")

        return [
            str(Path(dirpath) / name)
            for dirpath, _, filenames in os.walk(path)
            for name in filenames
            if name.lower().rsplit('.', 1)[-1] in AUDIO_EXTENSIONS
        ]

    try:
        return await asyncio.to_thread(walk)
    except NotADirectoryError as e:
        print(f"[ERROR] {e}")
        return []


def extract_metadata(path: str) -> dict[str, tuple[str, str, str, float]]:
    try:
        audio = File(path)
        if audio is None:
            return {path: ("Desconocido", "Desconocido", "Desconocido", 0.0)}


        tags = audio.tags or {}

        title = str(tags.get("TIT2") or tags.get("title") or Path(path).stem)
        artist = str(tags.get("TPE1") or tags.get("artist") or "Desconocido")
        album = str(tags.get("TALB") or tags.get("album") or "Desconocido")
        duration = round(getattr(audio.info, "length", 0.0), 2)

        return {path: (title, album, artist, duration)}

    except Exception as e:
        print(f"[WARN] Error extrayendo metadatos de {path}: {e}")
        return {path: ("Desconocido", "Desconocido", "Desconocido", 0.0)}
