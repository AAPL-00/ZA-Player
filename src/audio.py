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
    print("DEBUG: Starting playlist")
    for track in tracks:
        play_audio(track)
        while pygame.mixer.music.get_busy():
            print("Comandos: [p]ausa, [r]eanudar, [s]iguiente, [q]uit")
            comando = input("> ").strip().lower()
            if comando == 'p':
                pygame.mixer.music.pause()
            elif comando == 'r':
                pygame.mixer.music.unpause()
            elif comando == 's':
                pygame.mixer.music.stop()
                # Sal del bucle para ir a la siguiente canción
                break
            elif comando == 'q':
                pygame.mixer.music.stop()
                # Sal completamente de la playlist
                return
            # Si el comando no es 's' ni 'q', NO haces break, sigues esperando input
            # Puedes agregar un pequeño sleep si quieres evitar consumir CPU
            await asyncio.sleep(0.1)
