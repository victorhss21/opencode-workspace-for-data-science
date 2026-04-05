from pathlib import Path


def validate_input_path(path: Path) -> bool:
    return path.exists() and path.is_file()
