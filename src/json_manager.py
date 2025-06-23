import json
import aiofiles
from pathlib import Path
from .files_manager import find_audio_files, extract_metadata
import logging

# Configure logging for better debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Use pathlib to ensure cross-platform compatibility
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

    Raises:
        PermissionError: If the process lacks permission to access or create the file.
        OSError: For other file system-related errors.
    """
    path_obj = Path(DEFAULT_REPO_PATH).resolve()  # Normalize path for Windows compatibility

    try:
        if not path_obj.exists():
            path_obj.parent.mkdir(parents=True, exist_ok=True)
            async with aiofiles.open(path_obj, mode='w', encoding='utf-8') as file:
                await file.write("{}")
                logger.info("No se ha encontrado un repositorio, se ha creado uno nuevo.")
            return {}

        async with aiofiles.open(path_obj, mode='r', encoding='utf-8') as file:
            content = await file.read()
            logger.info("Se ha cargado el repositorio.")
            return json.loads(content)
    except PermissionError as e:
        logger.error(f"No se pudo acceder o crear el repositorio en {path_obj}: {e}")
        return {}
    except OSError as e:
        logger.error(f"Error del sistema al cargar el repositorio en {path_obj}: {e}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error al decodificar el archivo JSON {path_obj}: {e}")
        return {}


async def save_repository(data):
    """
    Asynchronously saves the music library dictionary to a JSON file.

    This function serializes the given dictionary into a JSON formatted string and
    writes it to the `DEFAULT_REPO_PATH`. The JSON is formatted with an indent
    of 2 spaces for human readability.

    Args:
        data (dict): The dictionary containing the music library data to be saved.

    Raises:
        PermissionError: If the process lacks permission to write to the file.
        OSError: For other file system-related errors.
    """
    path_obj = Path(DEFAULT_REPO_PATH).resolve()  # Normalize path for Windows compatibility

    try:
        async with aiofiles.open(path_obj, mode='w', encoding='utf-8') as file:
            await file.write(json.dumps(data, indent=2, ensure_ascii=False))
            logger.info("Guardado exitosamente.")
    except PermissionError as e:
        logger.error(f"No se pudo escribir en {path_obj}: {e}")
    except OSError as e:
        logger.error(f"Error del sistema al guardar el repositorio en {path_obj}: {e}")


async def update_repository(paths):
    """
    Scans a directory for new audio files and updates the repository.

    This function first loads the existing repository, then scans the specified
    `path_to_scan` for audio files. For each file found, it checks if it already
    exists in the repository. If not, it extracts its metadata and adds the new
    entry to the library. Finally, it saves the updated repository back to disk.

    Args:
        paths (str): The path to the directory to scan for new audio files.

    Raises:
        FileNotFoundError: If the provided path does not exist.
    """
    try:
        repo = await load_repository()
        audio_files_paths = await find_audio_files(paths)
        new_entries = {
            file_path: extract_metadata(file_path)[file_path]
            for file_path in audio_files_paths
            if file_path not in repo
        }
        if not new_entries:
            logger.info("No hay archivos nuevos para agregar.")
            return

        repo.update(new_entries)
        await save_repository(repo)
    except FileNotFoundError as e:
        logger.error(f"No se pudo escanear el directorio {paths}: {e}")
    except Exception as e:
        logger.error(f"Error inesperado al actualizar el repositorio: {e}")