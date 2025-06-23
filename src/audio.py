import pygame
import asyncio
import threading
import queue
import sys
import msvcrt  # Para Windows; para Linux/MacOS, necesitarás ajustes


def init_mixer():
    """
    Initializes the pygame mixer for audio playback.
    """
    pygame.mixer.init()


def play_audio(track: tuple[str, str]):
    """
    Plays an audio file and displays its title.

    Args:
        track (tuple[str, str]): Tuple of (path, title) for the audio file.
    """
    try:
        pygame.mixer.music.load(track[0])
        pygame.mixer.music.play()
        print(f"[INFO] Playing: {track[1]} 🎶")
    except Exception as e:
        print(f"[ERROR] Oh no! Couldn't play {track[1]}: {e}")


def read_input(q: queue.Queue, stop_event: threading.Event):
    """
    Reads keyboard input in a separate thread and puts it into a queue.

    Args:
        q (queue.Queue): Queue to store input commands.
        stop_event (threading.Event): Event to signal when to stop reading.
    """
    while not stop_event.is_set():
        if sys.platform == "win32":
            if msvcrt.kbhit():
                key = msvcrt.getch().decode()
                q.put(key)
        else:
            # Para Linux/MacOS, usa termios/select
            import select
            import tty
            import termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    key = sys.stdin.read(1)
                    q.put(key)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            asyncio.sleep(0.1)


async def control_playback(stop_event: asyncio.Event):
    """
    Processes terminal commands from a queue to control audio playback.

    Args:
        stop_event (asyncio.Event): Event to signal when to stop playback.

    Commands:
        p: Pause playback
        r: Resume playback
        s: Skip to next track
        q: Quit playback
    """
    q = queue.Queue()
    thread_stop_event = threading.Event()
    input_thread = threading.Thread(target=read_input, args=(q, thread_stop_event), daemon=True)
    input_thread.start()

    commands = {
        'p': "pause",
        'r': "resume",
        's': "skip",
        'q': "quit"
    }
    print("🎵 Controls: p (pause), r (resume), s (skip), q (quit)")

    try:
        while not stop_event.is_set():
            try:
                command = q.get_nowait()
                command = command.strip().lower()
                if command in commands:
                    print(f"[INFO] Command: {commands[command]}")
                    if command == 'p':
                        pygame.mixer.music.pause()
                    elif command == 'r':
                        pygame.mixer.music.unpause()
                    elif command == 's':
                        pygame.mixer.music.stop()
                    elif command == 'q':
                        pygame.mixer.music.stop()
                        stop_event.set()
                else:
                    print("[WARNING] Invalid command. Use: p, r, s, q")
            except queue.Empty:
                await asyncio.sleep(0.1)
    finally:
        thread_stop_event.set()


async def play_playlist(tracks: list[tuple[str, str]]):
    """
    Plays a list of audio tracks asynchronously, displaying their titles,
    with terminal controls for playback.

    Args:
        tracks (list[tuple[str, str]]): List of (path, title) tuples.
    """
    stop_event = asyncio.Event()
    control_task = asyncio.create_task(control_playback(stop_event))
    
    try:
        for track in tracks:
            play_audio(track)
            while (pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() > 0) and not stop_event.is_set():
                await asyncio.sleep(0.1)
            if stop_event.is_set():
                break
    finally:
        stop_event.set()
        await control_task
        pygame.mixer.music.stop()