from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union

from pydantic import BaseModel

from notion2markdown.schema.block.rich_text import RichText


class Title(BaseModel):
    id_: str
    type: str
    title: list[RichText]

    @classmethod
    def load(cls, params: dict[str, Any]) -> "Title":
        return cls(
            id_=params["id"],
            type=params["type"],
            title=[RichText.load(text) for text in params["title"]],
        )


class PageProperty(BaseModel):
    title: Title

    @classmethod
    def load(cls, params: dict[str, Any]) -> "PageProperty":
        title_params = (
            params["title"] if "title" in params.keys() else params["Name"]
        )
        return cls(
            title=Title.load(title_params),
        )
