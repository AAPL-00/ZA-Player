import asyncio

from src.json_manager import load_repository, update_repository
from src.audio import init_mixer, play_playlist
from src.sorts import random_sort

async def main():
    init_mixer()
    print("🎧 ZKA-Player inicializado")
    repo = await load_repository()



    if input("Desea agregar canciones? (s/n): ").lower() == 's':
        ruta = input("Introduce una ruta para agregar archivos de audio: ").strip()
        await update_repository(ruta)

        repo = await load_repository()  # Recargar tras modificación
        print("\n🎼 Repositorio actualizado:")
        for path, metadata in repo.items():
            title, album, artist, duration = metadata
            print(f"- {title} | {artist} | {album} | {duration} seg")

    else:
        for path, metadata in repo.items():
            title, album, artist, duration = metadata
            print(f"- {title} | {artist} | {album} | {duration} seg")

    if input("Desea reproducir sus canciones? (s/n): ").lower() == 's':
        print("\n🎶 Iniciando reproducción aleatoria de canciones.")
        await play_playlist(random_sort(repo))


if __name__ == "__main__":
    asyncio.run(main())