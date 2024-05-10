"""Rich Text"""

from typing import Any, Optional, Union

from pydantic import BaseModel, ConfigDict

from notion2markdown.schema.mention import (
    DatabaseMention,
    DateMention,
    LinkPreviewMention,
    PageMention,
    TemplateMention,
    UserMention,
)


class Annotations(BaseModel):
    """Annotations"""

    bold: bool = False
    """bold"""
    italic: bool = False
    """italic"""
    strikethrough: bool = False
    """strikethrough"""
    underline: bool = False
    """underline"""
    code: bool = False
    """code"""
    color: str = "default"
    """color"""


class BaseText(BaseModel):
    """Base Text"""

    pass


class Equation(BaseText):
    """Equation"""

    expression: str
    """expression"""

    # @classmethod
    # def from_notion(cls, params: dict[str, Any]) -> "Equation":
    #     return cls(expression=params["expression"])


class Mention(BaseText):
    """Mention"""

    type: str
    """type"""
    obj: Union[
        DatabaseMention,
        DateMention,
        LinkPreviewMention,
        PageMention,
        TemplateMention,
        UserMention,
    ]
    """mention object"""

    @classmethod
    def from_notion(cls, params: dict[str, Any]) -> "Mention":
        """Load Mention object

        Args:
            params (dict[str, Any]): params

        Returns:
            Mention: Mention object
        """
        _type = params["type"]

        if _type == "database":
            return cls(
                type=_type,
                obj=DatabaseMention(**params[_type]),
            )
        elif _type == "date":
            return cls(
                type=_type,
                obj=DateMention(**params[_type]),
            )
        elif _type == "link_preview":
            return cls(
                type=_type,
                obj=LinkPreviewMention(**params[_type]),
            )
        elif _type == "page":
            return cls(
                type=_type,
                obj=PageMention(**params[_type]),
            )
        # elif _type == "template_mention":
        #    pass
        elif _type == "user":
            return cls(
                type=_type,
                obj=UserMention(**params[_type]),
            )
        else:
            return cls(
                type=_type,
                obj=TemplateMention.from_notion(params[_type]),
            )


class Text(BaseText):
    """Text Object"""

    content: str
    """text content"""
    link: Optional[dict] = None
    """link url"""

    # @classmethod
    # def from_notion(cls, params: dict[str, Any]) -> "Text":
    #     return cls(
    #         content=params["content"],
    #         link=params.get("link"),
    #     )


class RichText(BaseModel):
    """Rich text object"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    type: str
    """object type"""
    text_obj: Union[BaseText, Text, Equation, Mention]
    """text object"""
    annotations: Annotations
    """text annotations"""
    plain_text: str
    """plain text"""
    href: Optional[str] = None
    """href"""

    @classmethod
    def from_notion(cls, params: dict[str, Any]) -> "RichText":
        """Load Rich text object

        Args:
            params (dict[str, Any]): params

        Returns:
            RichText: rich text object
        """
        _type = params["type"]
        text_obj: BaseText

        if _type == "text":
            text_obj = Text(**params[_type])
        elif _type == "equation":
            text_obj = Equation(**params[_type])
        else:
            text_obj = Mention.from_notion(params[_type])

        return cls(
            type=_type,
            text_obj=text_obj,
            annotations=Annotations(**params["annotations"]),
            plain_text=params["plain_text"],
            href=params["href"],
        )

    @classmethod
    def default_text(cls) -> "RichText":
        """Default text

        Returns:
            RichText: Default text
        """
        return cls(
            type="text",
            text_obj=Text(content="", link=None),
            annotations=Annotations(),
            plain_text="",
            href=None,
        )

    def get_content(self) -> str:
        """Get text content

        Returns:
            str: text content
        """
        if isinstance(self.text_obj, Text):
            return self.text_obj.content
        if isinstance(self.text_obj, Equation):
            return self.text_obj.expression
        else:
            return self.plain_text
