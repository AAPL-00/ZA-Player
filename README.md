# ZA-Player

A minimalist, command-line audio player built with Python, designed for music enthusiasts to manage and enjoy their local audio collections with a simple, terminal-based interface.

## Features
- **Asynchronous Audio Playback**: Plays various audio formats (MP3, FLAC, OGG, WAV, AAC, M4A, WMA, ALAC, OPUS) using `pygame` mixer.
- **Metadata Extraction**: Automatically retrieves title, artist, album, and duration from audio files using `mutagen`.
- **Playlist Management**: Supports random playback, album-based, or artist-based playlists with randomized order.
- **Interactive Terminal UI**: Built with `rich` for a visually appealing interface, including tables, panels, and colored prompts.
- **Cross-Platform File Handling**: Uses `pathlib` for robust directory scanning and JSON-based repository management.
- **Asynchronous Control**: Handles keyboard input for pause (`p`), resume (`r`), skip (`s`), and quit (`q`) commands during playback.
- **Repository Persistence**: Stores metadata in a JSON file (`~/.za_player/za_repository.json`) for quick library access and updates.


## Usage
1. **Launch the Player**:
   Run `python main.py` to start the application. You'll see a welcome banner and options to manage your music library.

2. **Add Songs**:
   - Choose `y` when prompted to add songs.
   - Enter the path to your audio files directory. The player will scan for supported formats and update the repository.

3. **View Library**:
   - The song library is displayed in a table showing title, artist, album, and duration.
   - If the library is empty, you'll be notified.

4. **Play Songs**:
   - Choose `y` to start playback.
   - Select a playback mode:
     - `r`: Random shuffle of all songs.
     - `a`: Play songs from a specific album (select from a numbered list).
     - `t`: Play songs by a specific artist (select from a numbered list).
   - Control playback with:
     - `p`: Pause
     - `r`: Resume
     - `s`: Skip to next track
     - `q`: Quit playback


## Limitations
- **Platform-Specific Input**:
  - Keyboard input for playback control is optimized for Windows (`msvcrt`). Linux/MacOS support requires adjustments using `termios` and `select`.
- **File I/O**:
  - The player scans local directories only and does not support streaming or network-based audio.
- **Error Handling**:
  - Metadata extraction may fail for corrupted files, defaulting to "Unknown" values.
- **Pygame Compatibility**:
  - Relies on `pygame.mixer`, which may have issues with certain audio formats or large files on some systems.

## Future Improvements
- Add support for custom playlists.
- Implement sorting by duration or file path.
- Enhance cross-platform input handling for Linux/MacOS.
- Add progress bar or playback time display.
- Support for gapless playback.
- Integrate unit tests for robustness.
