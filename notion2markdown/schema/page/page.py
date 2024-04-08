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
    def load(cls, response: dict[str, Any]) -> "Page":
        icon_param = response["icon"]
        icon_obj: Optional[Union[Emoji, FileObject]] = None
        if icon_param is not None:
            icon_obj = (
                Emoji.load(icon_param)
                if icon_param["type"] == "emoji"
                else FileObject.load(icon_param)
            )
        cover_param = response["cover"]
        cover_obj = (
            None if cover_param is None else FileObject.load(cover_param)
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
            created_by=User.load(response["created_by"]),
            last_edited_by=User.load(response["last_edited_by"]),
            archived=response["archived"],
            icon=icon_obj,
            cover=cover_obj,
            properties=PageProperty.load(response["properties"]),
            parent=Parent.load(response["parent"]),
            url=response["url"],
            public_url=response["public_url"],
        )

    @classmethod
    def retrieve_page(cls, notion_client: Client, page_id: str) -> "Page":
        page = notion_client.pages.retrieve(page_id=page_id)
        return Page.load(page)  # type: ignore
