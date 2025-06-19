import json
import aiofiles
from pathlib import Path
from .files_manager import find_audio_files, extract_metadata

DEFAULT_REPO_PATH = str(Path.home() / "music" / "zka_repository.json")

async def load_repository():
    path_obj = Path(DEFAULT_REPO_PATH)
    if not path_obj.exists():
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(DEFAULT_REPO_PATH, mode='w') as file:
            await file.write("{}")
        return {}

    async with aiofiles.open(DEFAULT_REPO_PATH) as file:
        content = await file.read()
        return json.loads(content)

async def save_repository(data):
    async with aiofiles.open(DEFAULT_REPO_PATH, mode='w') as file:
        await file.write(json.dumps(data,indent=2, ensure_ascii=False))


async def update_repository(paths):
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
