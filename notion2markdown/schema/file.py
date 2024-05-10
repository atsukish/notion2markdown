"""file object https://developers.notion.com/reference/file-object"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel

from notion2markdown.schema.block.rich_text import RichText


class FileObject(BaseModel):
    """File"""

    caption: list[RichText]
    """file caption"""
    type: str
    """object type"""
    url: str
    """object url"""
    expiry_time: Optional[datetime]
    """object expiry time"""

    @classmethod
    def from_notion(cls, params: dict[str, Any]) -> "FileObject":
        """From Notion response

        Args:
            params (dict[str, Any]): response params

        Returns:
            FileObject: file object
        """
        _type = params["type"]
        caption = (
            []
            if params.get("caption") is None
            else [RichText.from_notion(text) for text in params["caption"]]
        )
        return cls(
            caption=caption,
            type=_type,
            url=params[_type]["url"],
            expiry_time=params[_type].get("expiry_time"),
        )
