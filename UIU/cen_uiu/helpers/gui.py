from cen_uiu.gui import images
from pathlib import Path


def get_image(file_name: str) -> str:
    p = Path(images.__path__[0]) / file_name
    return p.as_posix()
