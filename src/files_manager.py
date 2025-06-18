import os
import asyncio
from pathlib import Path

AUDIO_EXTENSIONS = {"mp3", "flac", "wav", "aac", "m4a", "ogg", "wma", "alac", "opus"}


async def find_audio_files(root_path: str) -> list[str]:
    def blocking_walk() -> list[str]:
            return [
                str(Path(dirpath) / f)
                for dirpath, _, filenames in os.walk(root_path)
                for f in filenames
                if f.lower().rsplit('.', 1)[-1] in AUDIO_EXTENSIONS
            ]

    return await asyncio.to_thread(blocking_walk)
