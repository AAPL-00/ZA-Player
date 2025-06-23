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
from src.sorts import random_sort, album_sort, artist_sort

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
        "🌼 [bold bright_cyan]Wanna add some cute songies?[/bold bright_cyan] >w<",
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

    # Check if repository is empty
    if not repo:
        console.print("\n🌸 [bold red]Oh noes! No songies in your wibrary yet! >w<[/bold red]")
        return

    # Prompt for playback with extra sparkles
    if Prompt.ask(
        "🎶 [bold bright_cyan]Wanna pway your songies?[/bold bright_cyan] *giggles*",
        choices=["y", "n"],
        default="n"
    ).lower() == 'y':
        # Prompt for playback mode
        modes = {
            "r": "Wandom shuffwe (so sparkwy!)",
            "a": "By awbum (wike a cute CD!)",
            "t": "By awtist (fow your fave!)",
        }
        mode = Prompt.ask(
            "🌟 [bold bright_cyan]How do you wanna pway?[/bold bright_cyan]\n"
            f"  [bold magenta]r:[/bold magenta] {modes['r']}\n"
            f"  [bold magenta]a:[/bold magenta] {modes['a']}\n"
            f"  [bold magenta]t:[/bold magenta] {modes['t']}\n"
            "Choose a mode >w<: ",
            choices=["r", "a", "t"],
            default="r"
        ).lower()

        playlist = []
        if mode == "r":
            console.print("\n🌸 [bold magenta]Stawting super cute shuffwe pwayback! >w< 🎶[/bold magenta]")
            playlist = random_sort(repo)
        elif mode == "a":
            # Get unique albums
            albums = sorted({metadata[1] or "No awbum" for metadata in repo.values()})
            console.print("\n🌼 [bold bright_cyan]Choose an awbum! >w<[/bold bright_cyan]")
            for i, album in enumerate(albums, 1):
                console.print(f"  [bold magenta]{i}:[/bold magenta] {album}")
            choice = Prompt.ask(
                "Pick an awbum numbew (1-{}) >w<: ".format(len(albums)),
                choices=[str(i) for i in range(1, len(albums) + 1)]
            )
            selected_album = albums[int(choice) - 1]
            console.print(f"\n🌸 [bold magenta]Pwaying aww songies fwom {selected_album}! >w< 🎶[/bold magenta]")
            playlist = album_sort(repo, selected_album)
        elif mode == "t":
            # Get unique artists
            artists = sorted({metadata[2] or "Unknown awtist" for metadata in repo.values()})
            console.print("\n🌼 [bold bright_cyan]Choose an awtist! >w<[/bold bright_cyan]")
            for i, artist in enumerate(artists, 1):
                console.print(f"  [bold magenta]{i}:[/bold magenta] {artist}")
            choice = Prompt.ask(
                "Pick an awtist numbew (1-{}) >w<: ".format(len(artists)),
                choices=[str(i) for i in range(1, len(artists) + 1)]
            )
            selected_artist = artists[int(choice) - 1]
            console.print(f"\n🌸 [bold magenta]Pwaying aww songies by {selected_artist}! >w< 🎶[/bold magenta]")
            playlist = artist_sort(repo, selected_artist)

        if not playlist:
            console.print("\n🌸 [bold red]Oh noes! No songies fow this mode! >w<[/bold red]")
            return

        # Custom progress bar with a sparkly heart spinner
        with Progress(
            SpinnerColumn(spinner_name="hearts", style="bright_magenta"),  # Heart spinner for extra cuteness
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[magenta]Pwaying songies... 🌼✨", total=len(playlist))
            await play_playlist(playlist)  # Pass entire playlist to audio.py
            progress.update(task, description="[magenta]Done pwaying aww songies! >w< 🌸")

if __name__ == "__main__":
    asyncio.run(main())