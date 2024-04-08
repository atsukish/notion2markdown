"""Block object https://developers.notion.com/reference/block"""

from datetime import datetime
from typing import Any, Optional, Union

from notion_client import Client
from pydantic import BaseModel

from notion2markdown.schema.block.rich_text import RichText
from notion2markdown.schema.block.type import BlockType
from notion2markdown.schema.color import Color
from notion2markdown.schema.emoji import Emoji
from notion2markdown.schema.file import FileObject
from notion2markdown.schema.parent import Parent
from notion2markdown.schema.user import User


class BaseBlockObject(BaseModel):
    pass


class Block(BaseModel):

    object: str
    id_: str
    parent: Parent
    create_time: datetime
    last_edited_time: datetime
    created_by: User
    last_edited_by: User
    has_children: bool
    archived: bool
    type_: BlockType
    obj: Union[BaseBlockObject, FileObject]

    @classmethod
    def load(cls, response: dict[str, Any]) -> "Block":
        type_ = response["type"]

        block_obj = BlockFactory.create_block(
            type_=type_,
            params=response[type_],
        )

        return cls(
            object=response["object"],
            id_=response["id"],
            parent=Parent.load(response["parent"]),
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
            has_children=response["has_children"],
            archived=response["archived"],
            type_=type_,
            obj=block_obj,
        )

    @classmethod
    def retrieve_block(
        cls,
        notion_client: Client,
        block_id: str,
    ) -> "Block":
        blocks = notion_client.blocks.retrieve(block_id=block_id)
        return cls.load(blocks)  # type: ignore

    @classmethod
    def retrieve_children_blocks(
        cls,
        notion_client: Client,
        block_id: str,
    ) -> list["Block"]:
        blocks = notion_client.blocks.children.list(block_id=block_id)
        return [Block.load(b) for b in blocks["results"]]  # type: ignore


class BaseTextObject(BaseBlockObject):
    rich_text: list[RichText]


class Bookmark(BaseBlockObject):
    caption: list[RichText]
    url: str

    @classmethod
    def load(cls, params: dict[str, Any]) -> "Bookmark":
        return cls(
            caption=[RichText.load(text) for text in params["caption"]],
            url=params["url"],
        )


class BulletedListItem(BaseTextObject):
    color: Color
    # children: list[Block]

    @classmethod
    def load(cls, params: dict[str, Any]) -> "BulletedListItem":
        return cls(
            rich_text=[RichText.load(text) for text in params["rich_text"]],
            color=params["color"],
            # children=[Block.load(child) for child in params["children"]],
        )


class Callout(BaseTextObject):
    icon: Union[Emoji, FileObject]
    color: Color

    @classmethod
    def load(cls, params: dict[str, Any]) -> "Callout":
        return cls(
            rich_text=[RichText.load(text) for text in params["rich_text"]],
            icon=Emoji.load(params["icon"]),
            color=params["color"],
        )


class ChildDatabase(BaseBlockObject):
    title: str

    @classmethod
    def load(cls, params: dict[str, Any]) -> "ChildDatabase":
        return cls(title=params["title"])


class ChildPage(BaseBlockObject):
    title: str

    @classmethod
    def load(cls, params: dict[str, Any]) -> "ChildPage":
        return cls(title=params["title"])


class Code(BaseTextObject):
    caption: list[RichText]
    language: str

    @classmethod
    def load(cls, params: dict[str, Any]) -> "Code":
        return cls(
            caption=[RichText.load(caption) for caption in params["caption"]],
            rich_text=[RichText.load(text) for text in params["rich_text"]],
            language=params["language"],
        )


class ColumnlistColumn(BaseBlockObject):
    pass


class Divider(BaseBlockObject):
    pass


class Embed(BaseBlockObject):
    caption: list[RichText]
    url: str

    @classmethod
    def load(cls, params: dict[str, Any]) -> "Embed":
        return cls(
            caption=[RichText.load(caption) for caption in params["caption"]],
            url=params["url"],
        )


class Equation(BaseBlockObject):
    expression: str

    @classmethod
    def load(cls, params: dict[str, Any]) -> "Equation":
        return cls(expression=params["expression"])


class File(BaseBlockObject):
    caption: list[RichText]
    type: str
    file: FileObject
    name: str

    @classmethod
    def load(cls, params: dict[str, Any]) -> "File":
        return cls(
            caption=[RichText.load(text) for text in params["caption"]],
            type=params["type"],
            file=FileObject.load(params),
            name=params["name"],
        )


class Heading(BaseTextObject):
    color: Color
    is_toggleable: bool

    @classmethod
    def load(cls, params: dict[str, Any]) -> "Heading":
        return cls(
            rich_text=[RichText.load(text) for text in params["rich_text"]],
            color=params["color"],
            is_toggleable=params["is_toggleable"],
        )


class Image(BaseBlockObject):
    caption: list[RichText]
    type: str
    file: FileObject

    @classmethod
    def load(cls, params: dict[str, Any]) -> "Image":
        return cls(
            caption=[RichText.load(text) for text in params["caption"]],
            type=params["type"],
            file=FileObject.load(params),
        )


class NumberedListItem(BulletedListItem):
    pass


class Paragraph(BulletedListItem):
    pass


class PDF(Image):
    pass


class Quote(BulletedListItem):
    pass


class SyncedBlock(BaseBlockObject):
    # synced_from
    children: list[Block]

    @classmethod
    def load(cls, params: dict[str, Any]) -> "SyncedBlock":
        return cls(
            children=[Block.load(child) for child in params["children"]],
        )


class Table(BaseBlockObject):
    table_width: int
    has_column_header: bool
    has_row_header: bool

    @classmethod
    def load(cls, params: dict[str, Any]) -> "Table":
        return cls(
            table_width=params["table_width"],
            has_column_header=params["has_column_header"],
            has_row_header=params["has_row_header"],
        )


class TableRows(BaseBlockObject):
    cells: list[list[RichText]]

    @classmethod
    def load(cls, params: dict[str, Any]) -> "TableRows":
        cells = []
        for cell in params["cells"]:
            rows = []
            if len(cell) == 0:
                rows.append(RichText.default_text())
            for text in cell:
                rows.append(RichText.load(text))
            cells.append(rows)
        return cls(cells=cells)


class TableContents(BaseBlockObject):
    color: Color

    @classmethod
    def load(cls, params: dict[str, Any]) -> "TableContents":
        return cls(color=params["color"])


class ToDo(BaseTextObject):
    checked: Optional[bool] = False
    color: Color

    @classmethod
    def load(cls, params: dict[str, Any]) -> "ToDo":
        return cls(
            rich_text=[RichText.load(text) for text in params["rich_text"]],
            checked=params.get("checked"),
            color=params["color"],
        )


class ToggleBlocks(BulletedListItem):
    pass


class Video(FileObject):
    pass


class BlockFactory:
    block_classes = {
        "bookmark": Bookmark,
        "bulleted_list_item": BulletedListItem,
        "callout": Callout,
        "child_page": ChildPage,
        "column": BaseBlockObject,
        "column_list": BaseBlockObject,
        "code": Code,
        "divider": BaseBlockObject,
        "embed": Embed,
        "equation": Equation,
        "file": File,
        "heading_1": Heading,
        "heading_2": Heading,
        "heading_3": Heading,
        "image": Image,
        "link_preview": BaseBlockObject,
        "link_to_page": BaseBlockObject,
        "numbered_list_item": NumberedListItem,
        "paragraph": Paragraph,
        "pdf": PDF,
        "quote": Quote,
        "synced_block": SyncedBlock,
        "table": Table,
        "table_of_contents": TableContents,
        "table_row": TableRows,
        "template": BaseBlockObject,
        "to_do": ToDo,
        "toggle": ToggleBlocks,
        "video": Video,
    }

    @staticmethod
    def create_block(type_: str, params: dict[str, Any]):
        block_class = BlockFactory.block_classes.get(type_, BaseBlockObject)
        return (
            block_class.load(params)
            if hasattr(block_class, "load")
            else block_class()
        )
