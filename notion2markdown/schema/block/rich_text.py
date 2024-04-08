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
    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    underline: bool = False
    code: bool = False
    color: str = "default"


class BaseText(BaseModel):
    pass


class Equation(BaseText):
    expression: str

    @classmethod
    def load(cls, params: dict[str, Any]) -> "Equation":
        return cls(expression=params["expression"])


class Mention(BaseText):
    type: str
    obj: Union[
        DatabaseMention,
        DateMention,
        LinkPreviewMention,
        PageMention,
        TemplateMention,
        UserMention,
    ]

    @classmethod
    def load(cls, params: dict[str, Any]) -> "Mention":
        type_ = params["type"]

        if type_ == "database":
            return cls(
                type=type_,
                obj=DatabaseMention.load(params[type_]),
            )
        elif type_ == "date":
            return cls(
                type=type_,
                obj=DateMention.load(params[type_]),
            )
        elif type_ == "link_preview":
            return cls(
                type=type_,
                obj=LinkPreviewMention.load(params[type_]),
            )
        elif type_ == "page":
            return cls(
                type=type_,
                obj=PageMention.load(params[type_]),
            )
        # elif type_ == "template_mention":
        #    pass
        elif type_ == "user":
            return cls(
                type=type_,
                obj=UserMention.load(params[type_]),
            )
        else:
            return cls(
                type=type_,
                obj=TemplateMention.load(params[type_]),
            )


class Text(BaseText):
    content: str
    link: Optional[dict] = None

    @classmethod
    def load(cls, params: dict[str, Any]) -> "Text":
        return cls(
            content=params["content"],
            link=params.get("link"),
        )


class RichText(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    type_: str
    text_obj: Union[BaseText, Text, Equation, Mention]
    annotations: Annotations
    plain_text: str
    href: Optional[str] = None

    @classmethod
    def load(cls, params: dict[str, Any]) -> "RichText":

        type_ = params["type"]
        text_obj: BaseText

        if type_ == "text":
            text_obj = Text.load(params[type_])
        elif type_ == "equation":
            text_obj = Equation.load(params[type_])
        else:
            text_obj = Mention.load(params[type_])

        return cls(
            type_=type_,
            text_obj=text_obj,
            annotations=Annotations(**params["annotations"]),
            plain_text=params["plain_text"],
            href=params["href"],
        )

    @classmethod
    def default_text(cls) -> "RichText":
        return cls(
            type_="text",
            text_obj=Text(content="", link=None),
            annotations=Annotations(),
            plain_text="",
            href=None,
        )

    def get_content(self) -> str:
        if isinstance(self.text_obj, Text):
            return self.text_obj.content
        if isinstance(self.text_obj, Equation):
            return self.text_obj.expression
        else:
            return self.plain_text
