"""https://developers.notion.com/reference/user"""

from typing import Any, Optional

from pydantic import BaseModel


class User(BaseModel):
    object: str
    id_: str
    type_: Optional[str] = None
    name: Optional[str] = None
    avatar_url: Optional[str] = None

    @classmethod
    def load(cls, params: dict[str, Any]) -> "User":
        return cls(
            object=params["object"],
            id_=params["id"],
            type_=params.get("type"),
            name=params.get("name"),
            avatar_url=params.get("avatar_url"),
        )
