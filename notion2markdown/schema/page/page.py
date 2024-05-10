"""https://developers.notion.com/reference/page"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union

from notion_client import Client
from pydantic import BaseModel

from notion2markdown.schema.emoji import Emoji
from notion2markdown.schema.file import FileObject
from notion2markdown.schema.page.page_propertes import PageProperty
from notion2markdown.schema.parent import Parent
from notion2markdown.schema.user import User


class PageObject(str, Enum):
    """page object"""

    page = "page"


class Page(BaseModel):
    """Page Object"""

    object: PageObject
    id: str
    create_time: datetime
    last_edited_time: datetime
    created_by: User
    last_edited_by: User
    archived: bool
    icon: Optional[Union[Emoji, FileObject]] = None
    cover: Optional[FileObject] = None
    properties: PageProperty
    parent: Parent
    url: str
    public_url: Optional[str] = None

    @classmethod
    def from_notion(cls, response: dict[str, Any]) -> "Page":
        """Load page object

        Args:
            response (dict[str, Any]): params

        Returns:
            Page: page object
        """
        icon_param = response["icon"]
        icon_obj: Optional[Union[Emoji, FileObject]] = None
        if icon_param is not None:
            icon_obj = (
                Emoji(**icon_param)
                if icon_param["type"] == "emoji"
                else FileObject.from_notion(icon_param)
            )
        cover_param = response["cover"]
        cover_obj = (
            None
            if cover_param is None
            else FileObject.from_notion(cover_param)
        )

        return cls(
            object=response["object"],
            id=response["id"],
            create_time=datetime.strptime(
                response["created_time"],
                "%Y-%m-%dT%H:%M:%S.%fZ",
            ),
            last_edited_time=datetime.strptime(
                response["last_edited_time"],
                "%Y-%m-%dT%H:%M:%S.%fZ",
            ),
            created_by=User(**response["created_by"]),
            last_edited_by=User(**response["last_edited_by"]),
            archived=response["archived"],
            icon=icon_obj,
            cover=cover_obj,
            properties=PageProperty.from_notion(response["properties"]),
            parent=Parent.from_notion(response["parent"]),
            url=response["url"],
            public_url=response["public_url"],
        )

    @classmethod
    def retrieve_page(cls, notion_client: Client, page_id: str) -> "Page":
        """From retrieve page

        Args:
            notion_client (Client): notion client
            page_id (str): page id

        Returns:
            Page: Page object
        """
        page = notion_client.pages.retrieve(page_id=page_id)
        return Page.from_notion(page)  # type: ignore
