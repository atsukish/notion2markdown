"""test emoji.py"""

from notion2markdown.schema.emoji import Emoji


def test_emoji() -> None:
    """Test Emoji instance"""
    params = {
        "type": "emoji",
        "emoji": "😻",
    }

    emoji = Emoji(**params)

    assert emoji.type == "emoji"
    assert emoji.emoji == "😻"
