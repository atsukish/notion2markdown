"""user object https://developers.notion.com/reference/user"""

from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    """User object"""

    object: str
    """object"""
    id: str
    """user id"""
    type: Optional[str] = None
    """user type"""
    name: Optional[str] = None
    """user name"""
    avatar_url: Optional[str] = None
    """avator url"""
