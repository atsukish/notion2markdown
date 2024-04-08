"""Notion reader."""

import os
from pathlib import Path
from typing import Any, Optional, Union

import click
from notion_client import Client

from notion2markdown import md
from notion2markdown.constant import NOTION_TOKEN
from notion2markdown.schema.block.block import (
    PDF,
    BaseTextObject,
    Block,
    Bookmark,
    BulletedListItem,
    Callout,
    ChildDatabase,
    ChildPage,
    Code,
    Embed,
    File,
    Heading,
    Image,
    RichText,
    TableRows,
    ToDo,
    Video,
)
from notion2markdown.schema.block.rich_text import Annotations
from notion2markdown.schema.emoji import Emoji
from notion2markdown.schema.page.page import Page
from notion2markdown.utils import get_page_tag


class NotionPageMarkdownReader:
    """Notion Page Reader"""

    def __init__(self, token: Optional[str] = None) -> None:
        """Initialize with parameters."""
        if token is None:
            token = os.getenv("NOTION_TOKEN")
            if token is None:
                raise ValueError(
                    "Must specify `integration_token` or set environment "
                    "variable `NOTION_INTEGRATION_TOKEN`.",
                )
        self.token = token

    @property
    def client(self) -> Client:
        return Client(auth=self.token)

    def add_block_style(
        self,
        block_type: str,
        block_obj: BaseTextObject,
        text: str,
    ) -> str:
        """ブロックスタイル適用

        Args:
            block_obj (dict[str, Any]): _description_

        Returns:
            str: _description_
        """
        if block_type == "heading_1":
            return md.heading1(text)
        if block_type == "heading_2":
            return md.heading2(text)
        if block_type == "heading_3":
            return md.heading3(text)
        if block_type == "bulleted_list_item":
            return md.bullet(text)
        if block_type == "numbered_list_item":
            return md.bullet(text, count=1)
        if block_type == "code":
            code_obj: Code = block_obj  # type:ignore
            return md.code_block(text, language=code_obj.language)
        if block_type == "quote":
            return md.quote(text)
        if block_type == "to_do":
            todo_obj: ToDo = block_obj  # type:ignore
            return md.todo(text, checked=todo_obj.checked or False)
        if block_type == "callout":
            callout_obj: Callout = block_obj  # type:ignore
            icon = (
                callout_obj.icon.emoji
                if isinstance(callout_obj.icon, Emoji)
                else ""
            )
            return md.callout(text, icon=icon)
        if block_type == "toggle":
            return md.bullet(text)

        return text

    def add_text_annotation(
        self,
        text: str,
        annotations: Annotations,
    ) -> str:
        """テキストスタイルを適用

        Args:
            text (str): テキスト
            annotations (dict[str, bool]): テキストスタイル

        Returns:
            str: テキスト
        """
        if annotations.bold:
            text = md.bold(text)
        if annotations.italic:
            text = md.italic(text)
        if annotations.strikethrough:
            text = md.strikethrough(text)
        if annotations.underline:
            text = md.underline(text)
        if annotations.code:
            text = md.inline_code(text)
        return text

    def add_link(self, text: str, href: Optional[str] = None) -> str:
        """リンク付与

        Args:
            text (str): テキスト
            href (Optional[str], optional): リンクURL. Defaults to None.

        Returns:
            str: リンク付与後のテキスト
        """
        if href:
            return md.link(text, href=href)
        return text

    def add_block_text_style(self, rich_texts: list[RichText]) -> str:
        """ブロック文字列スタイル適用

        Args:
            rich_texts (list[RichText]): ブロック内のRichTextリスト

        Returns:
            str: スタイル適用後の文字列
        """
        block_text = ""
        for text in rich_texts:
            tmp_text = self.add_text_annotation(
                text=text.get_content(),
                annotations=text.annotations,
            )
            block_text += self.add_link(
                text=tmp_text,
                href=text.href,
            )
        return block_text

    def add_indent_space(
        self,
        text: str,
        indent: int = 0,
        indent_spaces: int = 2,
    ) -> str:
        """インデントスペースを付与

        Args:
            text (str): テキスト
            indent (int, optional): インデントサイズ. Defaults to 0.
            indent_spaces (int, optional): インデントスペース数. Defaults to 2.

        Returns:
            str: インデント付与後のテキスト
        """
        tab = " " * indent_spaces
        if "\n" in text:
            return tab * indent + ("\n" + tab * indent).join(text.split("\n"))
        else:
            return tab * indent + text

    def block_to_markdown(self, block_id: str, indent: int = 0) -> str:
        blocks = Block.retrieve_children_blocks(
            notion_client=self.client,
            block_id=block_id,
        )

        blocks_text_list = []

        for block in blocks:

            block_text = ""

            if block.type_ == "image":
                image_obj: Image = block.obj  # type:ignore
                caption = (
                    self.add_block_text_style(image_obj.caption)
                    if len(image_obj.caption) > 0
                    else "image"
                )
                block_text += md.image(alt=caption, href=image_obj.file.url)

            elif block.type_ == "pdf":
                pdf_obj: PDF = block.obj  # type:ignore
                caption = (
                    self.add_block_text_style(pdf_obj.caption)
                    if len(pdf_obj.caption) > 0
                    else "file"
                )
                block_text += md.link(text=caption, href=pdf_obj.file.url)

            elif block.type_ == "divider":
                block_text += md.divider()

            elif block.type_ == "file":
                file_obj: File = block.obj  # type:ignore
                block_text += md.link(
                    text=file_obj.name,
                    href=file_obj.file.url,
                )

            elif block.type_ == "video":
                video_obj: Video = block.obj  # type:ignore
                title = get_page_tag(video_obj.url, html_tag="title")
                block_text += md.link(
                    text=title,
                    href=video_obj.url,
                )

            elif block.type_ in [
                "bookmark",
                "embed",
                # "link_preview",
                # "link_to_page",
            ]:
                link_obj: Union[Bookmark, Embed] = block.obj  # type:ignore
                title = get_page_tag(video_obj.url, html_tag="title")
                block_text += md.link(text=title, href=link_obj.url)

            elif block.type_ == "child_page":
                child_page_obj: ChildPage = block.obj  # type:ignore
                child_page = Page.retrieve_page(
                    notion_client=self.client,
                    page_id=block.id_,
                )
                block_text += md.link(
                    text=child_page_obj.title,
                    href=child_page.url,
                )

            elif block.type_ == "table":
                table_rows = Block.retrieve_children_blocks(
                    notion_client=self.client,
                    block_id=block.id_,
                )
                table_list = []

                for row in table_rows:
                    table_row_obj: TableRows = row.obj  # type:ignore

                    rows = [
                        self.add_block_text_style(cell)
                        for cell in table_row_obj.cells
                    ]
                    table_list.append(rows)

                block_text += md.table(
                    data=table_list[1:],
                    headers=table_list[0],
                )

            elif block.type_ in [
                "paragraph",
                "heading_1",
                "heading_2",
                "heading_3",
                "bulleted_list_item",
                "numbered_list_item",
                "code",
                "quote",
                "to_do",
                "callout",
                "toggle",
            ]:

                text_obj: BaseTextObject = block.obj  # type:ignore

                block_text = self.add_block_text_style(text_obj.rich_text)
                block_text = self.add_block_style(
                    block.type_,
                    text_obj,
                    block_text,
                )
            else:
                print(block)
                continue

            block_text = self.add_indent_space(block_text, indent=indent)
            blocks_text_list.append(block_text)

            if block.has_children and block.type_ != "child_page":
                blocks_text_list.append(
                    self.block_to_markdown(
                        block_id=block.id_,
                        indent=indent + 1,
                    ),
                )

        return "\n".join(blocks_text_list)

    def page_to_markdown(self, page_id: str) -> str:
        """Read a page."""
        page = Page.retrieve_page(self.client, page_id=page_id)

        text = self.block_to_markdown(block_id=page_id)

        # print(page.properties.title)
        print(self.add_block_text_style(page.properties.title.title))
        return text


@click.command()
@click.option("--page_id", type=str, required=True, help="notion page id")
def main(page_id: str) -> None:
    """Main

    Args:
        page_id (str): Notion page id
    """
    reader = NotionPageMarkdownReader(token=NOTION_TOKEN)

    page = reader.page_to_markdown(page_id=page_id)

    filename = Path("test.md")
    filename.write_text(page)


if __name__ == "__main__":
    main()
