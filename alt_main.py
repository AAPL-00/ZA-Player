import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from src.files_manager import find_audio_files, extract_metadata
from src.json_manager import load_repository, update_repository
from src.audio import init_mixer, play_playlist
from src.sorts import random_sort

console = Console()

async def main():
    # Initialize audio mixer
    init_mixer()

    # Super cute welcome message with bunny and daisy ASCII art
    console.print(Panel(
        Text(
            "🌸✨ ZKA-Pwayew ✨🌸\n"
            "  (ᵘʷᵘ)  \n"
            "  /) /)  \n"
            " ( ˶• ₒ •˶ ) \n"
            "  >🌼<  \n"
            "  ~*~  \n"
            "Hiii! W-welcome to the cutest music pwayew eva! >w<",
            justify="center",
            style="bold bright_magenta"
        ),
        title="🌸 ZKA-Pwayew 🌸",
        border_style="bright_magenta",
        padding=(1, 2)
    ))

    # Load repository
    repo = await load_repository()

    # Prompt for adding songs with a playful tone
    if Prompt.ask(
        "🌼 [bold bright_cyan]Wanna add some cute songies?[/bold bright_cyan] [bold green](y/n)[/bold green] >w<",
        choices=["y", "n"],
        default="n"
    ).lower() == 'y':
        ruta = Prompt.ask("🎀 [bold bright_cyan]Pwease give a path for your music fiwes:[/bold bright_cyan]")
        await update_repository(ruta.strip())
        repo = await load_repository()  # Reload after modification
        console.print("\n🌸 [bold magenta]Yay! Songies added to your wibrary! >w<[/bold magenta]")
    else:
        console.print("\n🌼 [bold bright_cyan]Here’s your cute songies wibrary! >w<[/bold bright_cyan]")

    # Display song list in a sparkly table
    table = Table(title="🎵 Your Cute Songies Wist! 🌟", title_style="bold bright_cyan", border_style="bright_magenta")
    table.add_column("✨ Titwe", style="magenta", no_wrap=True)
    table.add_column("🎤 Awtist", style="bright_cyan")
    table.add_column("💿 Awbum", style="bright_yellow")
    table.add_column("⏳ Timey (sec)", justify="right", style="green")

    for path, metadata in repo.items():
        title, album, artist, duration = metadata
        table.add_row(title or "Sin titwe >w<", artist or "Unknown awtist", album or "No awbum", f"{duration}")

    console.print(table)

    # Prompt for playback with extra sparkles
    if Prompt.ask(
        "🎶 [bold bright_cyan]Wanna pway your songies?[/bold bright_cyan] [bold green](y/n)[/bold green] *giggles*",
        choices=["y", "n"],
        default="n"
    ).lower() == 'y':
        console.print("\n🌸 [bold magenta]Stawting super cute shuffwe pwayback! >w< 🎶[/bold magenta]")
        console.print("[dim]Pssst! Use: p (pawsie), r (wesume), s (skippy), q (quit) >w<[/dim]")

        # Custom progress bar with a sparkly heart spinner
        playlist = random_sort(repo)
        with Progress(
            SpinnerColumn(spinner_name="hearts", style="bright_magenta"),  # Heart spinner for extra cuteness
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[magenta]Pwaying songies... 🌼✨", total=len(playlist) if playlist else 1)
            await play_playlist(playlist)  # Pass entire playlist to audio.py
            progress.update(task, description="[magenta]Done pwaying aww songies! >w< 🌸")

if __name__ == "__main__":
    asyncio.run(main())