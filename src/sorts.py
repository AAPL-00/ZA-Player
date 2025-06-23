import random

def random_sort(repo: dict) -> list[tuple[str, str]]:
    """
    Generates a randomly shuffled playlist from the repository.

    Args:
        repo (dict): Dictionary with paths as keys and (title, album, artist, duration) as values.

    Returns:
        list[tuple[str, str]]: List of (path, title) tuples in random order.
    """
    path_title_pairs = [(path, metadata[0]) for path, metadata in repo.items()]
    random.shuffle(path_title_pairs)
    return path_title_pairs


def album_sort(repo: dict, album: str) -> list[tuple[str, str]]:
    """
    Generates a randomly shuffled playlist of songs from a specific album.

    Args:
        repo (dict): Dictionary with paths as keys and (title, album, artist, duration) as values.
        album (str): Name of the album to filter by.

    Returns:
        list[tuple[str, str]]: List of (path, title) tuples for the album, in random order.
    """
    path_title_pairs = [
        (path, metadata[0])
        for path, metadata in repo.items()
        if metadata[1] == album or (metadata[1] is None and album == "No album")
    ]
    random.shuffle(path_title_pairs)
    return path_title_pairs


def artist_sort(repo: dict, artist: str) -> list[tuple[str, str]]:
    """
    Generates a randomly shuffled playlist of songs by a specific artist.

    Args:
        repo (dict): Dictionary with paths as keys and (title, album, artist, duration) as values.
        artist (str): Name of the artist to filter by.

    Returns:
        list[tuple[str, str]]: List of (path, title) tuples for the artist, in random order.
    """
    path_title_pairs = [
        (path, metadata[0])
        for path, metadata in repo.items()
        if metadata[2] == artist or (metadata[2] is None and artist == "Unknown artist")
    ]
    random.shuffle(path_title_pairs)
    return path_title_pairs
