# 🌸 ZA-Player 🎵

A minimalist yet powerful audio player built in Python, designed to manage and play your music collection with a touch of cuteness! ZA-Player supports asynchronous playback, metadata extraction, and a user-friendly console interface powered by `rich`. Whether you're shuffling your entire library or enjoying a specific album, ZA-Player has you covered! >w<

## ✨ Features

- **Music Library Management**: Scan directories for audio files (`mp3`, `flac`, `wav`, etc.) and store metadata (title, artist, album, duration) in a JSON repository.
- **Playback Modes**: Play songs randomly, by album, or by artist with a simple command-line interface.
- **Interactive Controls**: Pause (`p`), resume (`r`), skip (`s`), or quit (`q`) playback in real-time.
- **Asynchronous I/O**: Efficiently handles file operations and playback using `asyncio` and `aiofiles`.
- **Rich Console UI**: Beautiful and intuitive interface with tables, progress bars, and cute ASCII art (in `alt_main.py`).
- **Cross-Platform Support**: Works on Windows, Linux, and macOS (with minor adjustments for input handling).

## 🎶 Usage

1. **Launch the Player**: Run `main.py` or `alt_main.py`.
2. **Add Songs**: When prompted, enter a directory path to scan for audio files. Metadata is extracted and saved to `za_repository.json`.
3. **View Library**: See a table of your songs with titles, artists, albums, and durations.
4. **Play Music**:
   - Choose a playback mode: random (`r`), by album (`a`), or by artist (`t`).
   - Use `p` (pause), `r` (resume), `s` (skip), or `q` (quit) during playback.
5. **Enjoy!**: Let ZA-Player fill your world with music! 🌼✨


## 🐛 Known Issues

- Linux/macOS input handling may require `audio_linux.py` for better performance.
- Some audio formats may fail to load if `pygame` or `mutagen` lack codec support.
- Windows-specific input handling in `audio.py` uses `msvcrt`, which is not portable.

🎵 *Happy listening with ZA-Player!* ✨