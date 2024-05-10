"""https://developers.notion.com/reference/parent-object"""

from typing import Any, Optional

from pydantic import BaseModel


class Parent(BaseModel):
    """Parent Object"""

    type: str
    id: Optional[str] = None
    workspace: Optional[bool] = None

    @classmethod
    def from_notion(cls, params: dict[str, Any]) -> "Parent":
        """From Notion response

        Args:
            params (dict[str, Any]): response params

        Returns:
            Parent: Parent
        """
        _type = params["type"]
        if _type == "workspace":
            return cls(type=_type, workspace=params[_type])
        else:
            return cls(type=_type, id=params[_type])
