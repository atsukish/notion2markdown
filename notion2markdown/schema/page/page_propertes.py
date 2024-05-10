"""page propertyes"""

from typing import Any

from pydantic import BaseModel

from notion2markdown.schema.block.rich_text import RichText


class Title(BaseModel):
    """Title Object"""

    id: str
    """title id"""
    type: str
    """tutle type"""
    title: list[RichText]
    """title object"""

    @classmethod
    def from_notion(cls, params: dict[str, Any]) -> "Title":
        """Load title object

        Args:
            params (dict[str, Any]): params

        Returns:
            Title: title object
        """
        return cls(
            id=params["id"],
            type=params["type"],
            title=[RichText.from_notion(text) for text in params["title"]],
        )


class PageProperty(BaseModel):
    """Page property"""

    title: Title
    """title object"""

    @classmethod
    def from_notion(cls, params: dict[str, Any]) -> "PageProperty":
        """From notion response

        Args:
            params (dict[str, Any]): response params

        Returns:
            PageProperty: page property object
        """
        title_params = (
            params["title"] if "title" in params.keys() else params["Name"]
        )
        return cls(
            title=Title.from_notion(title_params),
        )
