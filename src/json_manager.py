import json
import aiofiles
from pathlib import Path
from .files_manager import find_audio_files, extract_metadata


DEFAULT_REPO_PATH = str(Path.home() / "za_player" / "za_repository.json")


async def load_repository():
    """
    Asynchronously loads the music library from a JSON file.

    This function checks if the repository file exists at the `DEFAULT_REPO_PATH`.
    If it doesn't, it creates the necessary parent directories and an empty JSON file.
    It then reads the file and deserializes its JSON content into a Python dictionary.

    Returns:
        dict: A dictionary representing the music library, where keys are file paths
            and values are metadata tuples. Returns an empty dictionary if the
            repository is new or empty.
    """
    path_obj = Path(DEFAULT_REPO_PATH)
    if not path_obj.exists():
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(DEFAULT_REPO_PATH, mode='w') as file:
            await file.write("{}")
            print("[INFO] No se ha encontrado un repositorio, se ha creado uno nuevo.")
        return {}

    async with aiofiles.open(DEFAULT_REPO_PATH) as file:
        content = await file.read()
        return json.loads(content)
        print("[INFO] Se ha cargado el repositorio.")



async def save_repository(data):
    """
    Asynchronously saves the music library dictionary to a JSON file.

    This function serializes the given dictionary into a JSON formatted string and
    writes it to the `DEFAULT_REPO_PATH`. The JSON is formatted with an indent
    of 2 spaces for human readability.

    Args:
        data (dict): The dictionary containing the music library data to be saved.
    """
    async with aiofiles.open(DEFAULT_REPO_PATH, mode='w') as file:
        await file.write(json.dumps(data, indent=2, ensure_ascii=False))
        print("[INFO] Guardado exitosamente.")


async def update_repository(paths):
    """
    Scans a directory for new audio files and updates the repository.

    This function first loads the existing repository, then scans the specified
    `path_to_scan` for audio files. For each file found, it checks if it already
    exists in the repository. If not, it extracts its metadata and adds the new
    entry to the library. Finally, it saves the updated repository back to disk.

    Args:
        path_to_scan (str): The path to the directory to scan for new audio files.
    """
    repo = await load_repository()
    audio_files_paths = await find_audio_files(paths)
    new_entries = {
            file_path: extract_metadata(file_path)[file_path]
            for file_path in audio_files_paths
            if file_path not in repo
    }
    if not new_entries:
        print("[INFO] No hay archivos nuevos para agregar.")
        return

    repo.update(new_entries)
    await save_repository(repo)
