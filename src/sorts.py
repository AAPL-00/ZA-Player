import random

def random_sort(repo: dict) -> list[str]:
    paths = list(repo.keys())
    random.shuffle(paths)
    return paths
