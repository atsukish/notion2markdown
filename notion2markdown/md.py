"""to markdown"""

from base64 import b64encode
from typing import Optional

import requests
from tabulate import tabulate

IMAGE_REQUEST_TIMEOUT = 10


def inline_code(text: str) -> str:
    """Inline code

    Args:
        text (str): text

    Returns:
        str: Inline code
    """
    return f"`{text}`"


def inline_equation(text: str) -> str:
    """Inline equation

    Args:
        text (str): text

    Returns:
        str: Inline equation
    """
    return f"${text}$"


def bold(text: str) -> str:
    """bold

    Args:
        text (str): text

    Returns:
        str: bold
    """
    return f"**{text}**"


def italic(text: str) -> str:
    """italic

    Args:
        text (str): text

    Returns:
        str: italic
    """
    return f"_{text}_"


def strikethrough(text: str) -> str:
    """strikethrough

    Args:
        text (str): text

    Returns:
        str: strikethrough
    """
    return f"~~{text}~~"


def underline(text: str) -> str:
    """underline

    Args:
        text (str): text

    Returns:
        str: underline
    """
    return f"<u>{text}</u>"


def link(text: str, href: str) -> str:
    """link

    Args:
        text (str): text
        href (str): href

    Returns:
        str: link
    """
    return f"[{text}]({href})"


def code_block(text: str, language: Optional[str] = None) -> str:
    """Code block

    Args:
        text (str): text
        language (str, optional): language. Defaults to "".

    Returns:
        str: code block
    """
    if language is None:
        language = ""
    elif language == "plain text":
        language = "text"
    return f"```{language}\n{text}\n```"


def equation(text: str) -> str:
    """equation

    Args:
        text (str): text

    Returns:
        str: equation
    """
    return f"$$\n{text}\n$$"


def heading1(text: str) -> str:
    """heading1

    Args:
        text (str): text

    Returns:
        str: heading1
    """
    return f"# {text}"


def heading2(text: str) -> str:
    """heading2

    Args:
        text (str): text

    Returns:
        str: heading2
    """
    return f"## {text}"


def heading3(text: str) -> str:
    """heading3

    Args:
        text (str): text

    Returns:
        str: heading3
    """
    return f"### {text}"


def quote(text: str) -> str:
    """quote

    Args:
        text (str): text

    Returns:
        str: quote
    """
    return "> " + "  \n> ".join(text.split("\n"))


def callout(text: str, icon: str = "") -> str:
    """callout

    Args:
        text (str): text
        icon (str): icon

    Returns:
        str: callout
    """
    emoji = icon if icon else ""
    return (
        "<aside>\n" + f"{emoji} " + "\n".join(text.split("\n")) + "\n</aside>"
    )


def bullet(text: str, count: Optional[int] = None) -> str:
    """bullet

    Args:
        text (str): text
        count (Optional[int], optional): count. Defaults to None.

    Returns:
        str: bullet
    """
    render_text = text.strip()
    return f"{count}. {render_text}" if count else f"- {render_text}"


def todo(text: str, checked: bool) -> str:
    """todo

    Args:
        text (str): text
        checked (bool): checked

    Returns:
        str: todo
    """
    return f"- [{'x' if checked else ' '}] {text}"


def image(alt: str, href: str, convert_to_base64: bool = False) -> str:
    """image

    Args:
        alt (str): alt
        href (str): href
        convert_to_base64 (bool, optional): convert base64. Defaults to False.

    Returns:
        str: image
    """
    if not convert_to_base64 or href.startswith("data:"):
        return f"![{alt}]({href})"
    else:
        response = requests.get(href, timeout=IMAGE_REQUEST_TIMEOUT)
        base64 = b64encode(response.content).decode("utf-8")
        return f"![{alt}](data:image/png;base64,{base64})"


def divider() -> str:
    """divider

    Returns:
        str: divider
    """
    return "\n---\n"


def toggle(summary: str = "", children: str = "") -> str:
    """toggle

    Args:
        summary (str, optional): summary. Defaults to "".
        children (str, optional): children. Defaults to "".

    Returns:
        str: toggle
    """
    if not summary:
        return children
    return (
        f"<details>\n<summary>{summary}</summary>\n{children}\n</details>\n\n"
    )


def table(data: list[list[str]], headers: list[str]) -> str:
    """table

    Args:
        data (list[list[str]]): cells
        headers (list[str]): header

    Returns:
        str: table
    """
    return tabulate(data, headers=headers, tablefmt="github")
