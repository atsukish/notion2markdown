from typing import Any, Optional, Union

from pydantic import BaseModel


class BaseMention(BaseModel):
    pass


class DatabaseMention(BaseMention):
    id_: str

    @classmethod
    def load(cls, params: dict[str, Any]) -> "DatabaseMention":
        return cls(id_=params["id"])


class DateMention(BaseMention):
    start: Optional[str]
    end: Optional[str]
    time_zone: Optional[str]

    @classmethod
    def load(cls, params: dict[str, Any]) -> "DateMention":
        return cls(
            start=params.get("start"),
            end=params.get("end"),
            time_zone=params.get("time_zone"),
        )


class LinkPreviewMention(BaseMention):
    url: str

    @classmethod
    def load(cls, params: dict[str, Any]) -> "LinkPreviewMention":
        return cls(url=params["url"])


class PageMention(BaseMention):
    id_: str

    @classmethod
    def load(cls, params: dict[str, Any]) -> "PageMention":
        return cls(id_=params["id"])


class TemplateMention(BaseMention):
    type_: str
    template_mention_date: Optional[str]
    template_mention_user: Optional[str]

    @classmethod
    def load(cls, params: dict[str, Any]) -> "TemplateMention":
        type_ = params["type"]
        if type_ == "template_mention_date":
            return cls(
                type_=params["type"],
                template_mention_date=params["template_mention_date"],
                template_mention_user=None,
            )
        elif type_ == "template_mention_user":
            return cls(
                type_=params["type"],
                template_mention_date=None,
                template_mention_user=params["template_mention_user"],
            )
        else:
            raise ValueError("TemplateMention is invalid")


class UserMention(BaseMention):
    object: str
    id_: str

    @classmethod
    def load(cls, params: dict[str, Any]) -> "UserMention":
        return cls(object=params["object"], id_=params["id"])
