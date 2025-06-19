import json
import aiofiles
from pathlib import Path

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
        await file.write(json.dumps(data))
