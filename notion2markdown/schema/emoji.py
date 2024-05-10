"""emoji https://developers.notion.com/reference/emoji-object"""

from pydantic import BaseModel


class Emoji(BaseModel):
    """Emoji object"""

    type: str
    """type"""
    emoji: str
    """emoji"""
