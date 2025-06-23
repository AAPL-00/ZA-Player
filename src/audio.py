import pygame
import asyncio


def init_mixer():
    """
    Initializes the pygame mixer for audio playback.
    """
    pygame.mixer.init()


def play_audio(track: tuple[str, str]):
    """
    Plays an audio file and displays its title.

    Args:
        path (str): File path to the audio file.
        title (str): Song title to display.
    """
    try:
        pygame.mixer.music.load(track[0])
        pygame.mixer.music.play()
        print(f"[INFO] Playing: {track[1]} 🎶")
    except Exception as e:
        print(f"[ERROR] Oh no! Couldn't play {track[1]}: {e}")


async def play_playlist(tracks: list[tuple[str, str]]):
    """
    Plays a list of audio tracks asynchronously, displaying their titles.

    Args:
        tracks (list[tuple[str, str]]): List of (path, title) tuples.
    """
    for track in tracks:
        play_audio(track)
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
