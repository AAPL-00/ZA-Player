import asyncio
from src.json_manager import load_repository, update_repository

async def main():
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

    print("\n✅ Fin del flujo principal.")

if __name__ == "__main__":
    asyncio.run(main())
