from pathlib import Path


def projectRoot():
    return Path(__file__).resolve().parents[2]


def resolvePath(path, rootPath=None):
    if path is None or path == "":
        return None

    path = Path(path)
    if path.is_absolute():
        return path

    if rootPath:
        rootPath = Path(rootPath)
        if not rootPath.is_absolute():
            rootPath = projectRoot() / rootPath
    else:
        rootPath = projectRoot()

    return (rootPath / path).resolve()


def makeDir(path):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def listImages(directory):
    directory = Path(directory)
    extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}

    if not directory.exists():
        return []

    return sorted(
        path for path in directory.rglob("*") if path.suffix.lower() in extensions
    )


def pathForYaml(path):
    if path is None:
        return None

    return str(Path(path)).replace("\\", "/")
