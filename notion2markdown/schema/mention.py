"""mention https://developers.notion.com/reference/rich-text#mention"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class BaseMention(BaseModel):
    """Base mention model"""

    pass


class DatabaseMention(BaseMention):
    """Database mention"""

    id: str


class DateMention(BaseMention):
    """Date mention"""

    start: Optional[datetime] = None
    end: Optional[datetime] = None
    time_zone: Optional[str] = None


class LinkPreviewMention(BaseMention):
    """Link preview mention"""

    url: str


class PageMention(DatabaseMention):
    """Page mention"""

    pass


class TemplateMention(BaseMention):
    """Template mention"""

    type: str
    template_mention_date: Optional[str]
    template_mention_user: Optional[str]

    @classmethod
    def from_notion(cls, params: dict[str, Any]) -> "TemplateMention":
        """From notion response

        Args:
            params (dict[str, Any]): response params

        Raises:
            ValueError: TemplateMention is invalid

        Returns:
            TemplateMention: TemplateMention object
        """
        _type = params["type"]
        if _type == "template_mention_date":
            return cls(
                type=_type,
                template_mention_date=params["template_mention_date"],
                template_mention_user=None,
            )
        elif _type == "template_mention_user":
            return cls(
                type=_type,
                template_mention_date=None,
                template_mention_user=params["template_mention_user"],
            )
        else:
            raise ValueError("TemplateMention is invalid")


class UserMention(BaseMention):
    """User mention"""

    object: str
    id: str
