"""https://developers.notion.com/reference/parent-object"""

from typing import Any, Optional

from pydantic import BaseModel


class Parent(BaseModel):
    type_: str
    id_: Optional[str] = None
    workspace: Optional[bool] = None

    @classmethod
    def load(cls, params: dict[str, Any]) -> "Parent":

        type_ = params["type"]
        if type_ == "workspace":
            return cls(type_=type_, workspace=params[type_])
        else:
            return cls(type_=type_, id_=params[type_])
