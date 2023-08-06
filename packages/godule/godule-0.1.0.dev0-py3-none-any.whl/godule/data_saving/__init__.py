def safe_save_filename(filename):
    from pathlib import Path
    filepath = Path(filename)
    parent = filepath.parent
    stem = filepath.stem
    suffix = filepath.suffix
    if not filepath.exists():
        return filepath.absolute().as_posix()
    else:
        idx = 1
        new_filename = Path(parent, stem + f'-{idx}' + suffix)
        while new_filename.exists():
            idx += 1
            new_filename = Path(parent, stem + f'-{idx}' + suffix)
        parent.mkdir(parents=True, exist_ok=True)
        return new_filename.absolute().as_posix()
