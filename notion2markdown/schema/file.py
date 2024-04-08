from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel

from notion2markdown.schema.block.rich_text import RichText


class FileObject(BaseModel):
    caption: list[RichText]
    type_: str
    url: str
    expiry_time: Optional[str]

    @classmethod
    def load(cls, params: dict[str, Any]) -> "FileObject":
        type_ = params["type"]
        caption = (
            []
            if "caption" not in params.keys()
            else [RichText.load(text) for text in params["caption"]]
        )
        return cls(
            caption=caption,
            type_=type_,
            url=params[type_]["url"],
            expiry_time=params[type_].get("url"),
        )
