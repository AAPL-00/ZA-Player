import os
import asyncio
from pathlib import Path
from mutagen._file import File


AUDIO_EXTENSIONS = {"mp3", "flac", "wav", "aac", "m4a", "ogg", "wma", "alac", "opus"}


async def find_audio_files(root_path: str) -> list[str]:
    """
    Asynchronously finds all audio files in a given directory and its subdirectories.

    This function scans the specified directory tree for files matching the extensions
    defined in the `AUDIO_EXTENSIONS` set. The file system I/O is run in a
    separate thread to prevent blocking the asyncio event loop, making it suitable
    for asynchronous applications.

    Args:
        root_path (str): The absolute or relative path to the root directory
                        to start the search from.

    Returns:
        list[str]: A list of strings, where each string is the full path to a
                found audio file. Returns an empty list if the path is not a
                valid directory or if no audio files are found.

    Raises:
        FileNotFoundError: If the initial `root_path` does not exist.
    """
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
    """
    Extracts metadata from a single audio file using the mutagen library.

    This function attempts to open an audio file and read its metadata tags,
    including title, artist, album, and duration. It provides sensible fallbacks
    for any missing information:
    - Title: Falls back to the filename (without extension).
    - Artist/Album: Falls back to "Unknown".
    - Duration: Falls back to 0.0.

    The function is designed to be robust, handling potential errors during file
    processing by returning a dictionary with default values.

    Args:
        path (str): The full path to the audio file.

    Returns:
        dict[str, tuple[str, str, str, float]]: A dictionary where the key is the
        original file path and the value is a tuple containing the
        (title, album, artist, duration).
    """
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
