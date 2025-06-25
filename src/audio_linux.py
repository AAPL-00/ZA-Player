'''
This code is subject to revision, I do not fully understand how the tty and termios libraries work.
It's organized this way because I tried to integrate logic for windows and linux but I wasn't able to, is easier to 
work with msvcrt library in windows an this is windows exclusive, that's the problem
'''

import pygame
import asyncio
import threading
import queue
import sys
import select
import tty
import termios

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
        # Clear the line before printing new information
        print("\r" + " " * 80, end="", flush=True) # Clear up to 80 characters
        pygame.mixer.music.load(track[0])
        pygame.mixer.music.play()
        print(f"\r[INFO] Playing: {track[1]} 🎶", end="", flush=True)
    except Exception as e:
        # Clear the line before printing new information
        print("\r" + " " * 80, end="", flush=True) # Clear up to 80 characters
        print(f"\r[ERROR] Oh no! Couldn't play {track[1]}: {e}", end="", flush=True)

def read_input(q: queue.Queue, stop_event: threading.Event):
    """
    Reads keyboard input in a separate thread and puts it into a queue.

    Args:
        q (queue.Queue): Queue to store input commands.
        stop_event (threading.Event): Event to signal when to stop reading.
    """
    if sys.platform == "win32":
        import msvcrt
        while not stop_event.is_set():
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8', errors='ignore')
                if key.isprintable():  # Solo procesar caracteres imprimibles
                    q.put(key)
            else:
                threading.Event().wait(0.1)
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while not stop_event.is_set():
                rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
                if rlist:
                    key = sys.stdin.read(1)
                    if key.isprintable():  # Solo procesar caracteres imprimibles
                        q.put(key)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

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
    # Clear the line before printing new information
    print("\r" + " " * 80, end="", flush=True) # Clear up to 80 characters
    print("\r🎵 Controls: p (pause), r (resume), s (skip), q (quit)", end="", flush=True)

    try:
        while not stop_event.is_set():
            try:
                command = q.get_nowait()
                command = command.strip().lower()
                if command in commands:
                    # Clear the line before printing new information
                    print("\r" + " " * 80, end="", flush=True) # Clear up to 80 characters
                    print(f"\r[INFO] Command: {commands[command]}", end="", flush=True)
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
                    # Clear the line before printing new information
                    print("\r" + " " * 80, end="", flush=True) # Clear up to 80 characters
                    print("\r[WARNING] Invalid command. Use: p, r, s, q", end="", flush=True)
            except queue.Empty:
                await asyncio.sleep(0.1)
    finally:
        thread_stop_event.set()
        input_thread.join()
        pygame.mixer.music.stop()
        print("\r" + " " * 80, end="", flush=True)  # Clear the line when exiting
        print("\r", end="", flush=True) # Ensure the line is clean upon exit

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