"""utils"""

from pathlib import Path

import requests
from bs4 import BeautifulSoup


def get_page_tag(url: str, html_tag: str) -> str:
    """Get html page tag

    Args:
        url (str): url
        html_tag (str): html tag

    Returns:
        str: tag
    """
    req = requests.get(url, timeout=10)
    tag = BeautifulSoup(req.text, "html.parser").find(html_tag).get_text()
    return str(tag)


def download_image(
    url: str,
    dirpath: Path,
    filename: str = "Untitled",
) -> None:
    """Download image file

    Args:
        url (str): image url
        dirpath (Path): download dir path
        filename (str, optional): filename. Defaults to "Untitled".
    """
    dirpath.mkdir(exist_ok=True, parents=True)

    response = requests.get(url, timeout=10)
    image = response.content
    image_ext = response.headers["Content-Type"].split("/")[-1]

    filepath = dirpath.joinpath(f"{filename}.{image_ext}")

    if filepath.exists():
        pattern = f"{filename}_*.{image_ext}"
        existing_files = list(dirpath.glob(pattern))

        if not existing_files:
            filepath = dirpath.joinpath(f"{filename}_01.{image_ext}")
        else:
            max_sequence = max(
                int(f.stem.split("_")[-1]) for f in existing_files
            )
            sequence = max_sequence + 1
            filepath = dirpath.joinpath(
                f"{filename}_{sequence:02d}.{image_ext}",
            )

    filepath.write_bytes(image)
