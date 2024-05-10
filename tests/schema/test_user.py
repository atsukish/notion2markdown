"""test parent.py"""

from notion2markdown.schema.user import User


def test_parent() -> None:
    """Test Parent"""
    user_params = {
        "object": "user",
        "id": "e79a0b74-3aba-4149-9f74-0bb5791a6ee6",
        "type": "person",
        "name": "Avocado Lovelace",
        "avatar_url": "https://secure.notion-static.com/e6a352a8-8381-44d0-a1dc-9ed80e62b53d.jpg",
    }
    user = User(**user_params)
    assert user.object == "user"
    assert user.id == "e79a0b74-3aba-4149-9f74-0bb5791a6ee6"
    assert user.type == "person"
    assert user.name == "Avocado Lovelace"
    assert (
        user.avatar_url
        == "https://secure.notion-static.com/e6a352a8-8381-44d0-a1dc-9ed80e62b53d.jpg"
    )
