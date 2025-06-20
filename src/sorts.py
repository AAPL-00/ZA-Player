import random

def random_sort(repo: dict) -> list[tuple[str, str]]:
    path_title_pairs = [(path, metadata[0]) for path, metadata in repo.items()]
    random.shuffle(path_title_pairs)
    return path_title_pairs
