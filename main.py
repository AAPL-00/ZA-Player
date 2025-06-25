import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.text import Text
from src.json_manager import load_repository, update_repository
from src.audio import init_mixer, play_playlist
from src.sorts import random_sort, album_sort, artist_sort

console = Console()

async def main():
    # Initialize audio mixer
    init_mixer()

    # Welcome banner
    console.print(Panel(
        Text(
            "ZA-PLAYER\n"
            "══════════\n"
            "A minimalist audio player for your music collection.",
            justify="center",
            style="bold blue"
        ),
        title="ZA-Player",
        border_style="blue",
        padding=(1, 2)
    ))

    # Load repository
    repo = await load_repository()

    # Prompt for adding songs
    if Prompt.ask(
        "[blue]Would you like to add songs?[/blue]",
        choices=["y", "n"],
        default="n"
    ).lower() == 'y':
        ruta = Prompt.ask("[blue]Enter the path to your audio files:[/blue]")
        await update_repository(ruta.strip())
        repo = await load_repository()  # Reload after modification
        console.print("\n[blue]Repository updated successfully.[/blue]")
    else:
        console.print("\n[blue]Current song library:[/blue]")

    # Display song list in a table
    table = Table(title="Song Library", title_style="bold blue", border_style="dim")
    table.add_column("Title", style="white")
    table.add_column("Artist", style="grey78")
    table.add_column("Album", style="grey78")
    table.add_column("Duration (sec)", justify="right", style="white")

    for path, metadata in repo.items():
        title, album, artist, duration = metadata
        table.add_row(title or "Unknown", artist or "Unknown", album or "Unknown", f"{duration}")

    console.print(table)

    # Check if repository is empty
    if not repo:
        console.print("\n[red]The song library is empty.[/red]")
        return

    # Prompt for playback
    if Prompt.ask(
        "[blue]Would you like to play your songs?[/blue]",
        choices=["y", "n"],
        default="n"
    ).lower() == 'y':
        # Prompt for playback mode
        modes = {
            "r": "Random shuffle",
            "a": "By album",
            "t": "By artist",
        }
        mode = Prompt.ask(
            "[blue]Select playback mode:[/blue]\n"
            f"  [bold]r:[/bold] {modes['r']}\n"
            f"  [bold]a:[/bold] {modes['a']}\n"
            f"  [bold]t:[/bold] {modes['t']}\n"
            "Enter mode: ",
            choices=["r", "a", "t"],
            default="r"
        ).lower()

        playlist = []
        if mode == "r":
            console.print("\n[blue]Starting random playback.[/blue]")
            playlist = random_sort(repo)
        elif mode == "a":
            # Get unique albums
            albums = sorted({metadata[1] or "Unknown" for metadata in repo.values()})
            console.print("\n[blue]Available albums:[/blue]")
            for i, album in enumerate(albums, 1):
                console.print(f"  [bold]{i}:[/bold] {album}")
            choice = Prompt.ask(
                f"Select album number (1-{len(albums)}): ",
                choices=[str(i) for i in range(1, len(albums) + 1)]
            )
            selected_album = albums[int(choice) - 1]
            console.print(f"\n[blue]Playing songs from {selected_album}.[/blue]")
            playlist = album_sort(repo, selected_album)
        elif mode == "t":
            # Get unique artists
            artists = sorted({metadata[2] or "Unknown" for metadata in repo.values()})
            console.print("\n[blue]Available artists:[/blue]")
            for i, artist in enumerate(artists, 1):
                console.print(f"  [bold]{i}:[/bold] {artist}")
            choice = Prompt.ask(
                f"Select artist number (1-{len(artists)}): ",
                choices=[str(i) for i in range(1, len(artists) + 1)]
            )
            selected_artist = artists[int(choice) - 1]
            console.print(f"\n[blue]Playing songs by {selected_artist}.[/blue]")
            playlist = artist_sort(repo, selected_artist)

        if not playlist:
            console.print("\n[red]No songs available for this mode.[/red]")
            return

        console.print("[blue]Playing songs...[/blue]")
        await play_playlist(playlist)
        console.print("[blue]Playback completed.[/blue]")

if __name__ == "__main__":
    asyncio.run(main())