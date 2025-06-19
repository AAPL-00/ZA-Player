import pygame
import asyncio

def init_mixer():
    try:
        pygame.mixer.init()
        print("[INFO] Mezclador de audio inicializado.")
    except Exception as e:
        print(f"[ERROR] No se pudo inicializar el mezclador: {e}")

def play_audio(path):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        print(f"[INFO] Reproduciendo: {path}")
    except Exception as e:
        print(f"[ERROR] Error cargando {path}: {e}")

async def play_playlist(tracks: list[str]):
    print("DEBUG")
    for path in tracks:
        play_audio(path)
        # Esperar hasta que termine de sonar
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(1)  # no bloquea el event loop
