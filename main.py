import asyncio
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from src.files_manager import find_audio_files, extract_metadata
from src.json_manager import load_repository, update_repository
from src.audio import init_mixer, play_playlist
from src.sorts import random_sort

async def main():
    # Initialize rich console
    console = Console()

    # Initialize audio mixer
    init_mixer()
    console.print("🎧 [bold cyan]ZKA-Player inicializado[/bold cyan]")

    # Load repository
    repo = await load_repository()

    # Ask if user wants to add songs
    if Prompt.ask("🎵 ¿Desea agregar canciones? [bold green](s/n)[/bold green]", choices=["s", "n"], default="n").lower() == 's':
        ruta = Prompt.ask("📁 Introduce una ruta para agregar archivos de audio")
        await update_repository(ruta.strip())
        repo = await load_repository()  # Reload after modification
        console.print("\n🎼 [bold green]Repositorio actualizado:[/bold green]")
    else:
        console.print("\n🎼 [bold magenta]Canciones en el repositorio:[/bold magenta]")

    # Display songs in a table
    table = Table(title="Lista de Canciones", box=None, style="dim")
    table.add_column("Título", style="cyan")
    table.add_column("Artista", style="magenta")
    table.add_column("Álbum", style="green")
    table.add_column("Duración", justify="right", style="yellow")
    
    for path, metadata in repo.items():
        title, album, artist, duration = metadata
        table.add_row(title or "Sin título", artist or "Desconocido", album or "Sin álbum", f"{duration} seg")
    
    console.print(table)

    # Ask if user wants to play songs
    if Prompt.ask("🎶 ¿Desea reproducir sus canciones? [bold green](s/n)[/bold green]", choices=["s", "n"], default="n").lower() == 's':
        console.print("\n🎵 [bold cyan]Iniciando reproducción aleatoria de canciones...[/bold cyan]")
        await play_playlist(random_sort(repo))

if __name__ == "__main__":
    asyncio.run(main())