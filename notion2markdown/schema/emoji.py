from typing import Any

from pydantic import BaseModel


class Emoji(BaseModel):

    type_: str
    emoji: str

    @classmethod
    def load(cls, params: dict[str, Any]) -> "Emoji":
        return cls(type_=params["type"], emoji=params["emoji"])
