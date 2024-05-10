"""test mention.py"""

from datetime import datetime

import pytest

from notion2markdown.schema.mention import (
    DatabaseMention,
    DateMention,
    LinkPreviewMention,
    PageMention,
    TemplateMention,
    UserMention,
)


def test_database_mention() -> None:
    """Test DatabaseMention"""
    params = {
        "id": "a1d8501e-1ac1-43e9-a6bd-ea9fe6c8822b",
    }

    database_mention = DatabaseMention.model_validate(params)
    assert database_mention.id == "a1d8501e-1ac1-43e9-a6bd-ea9fe6c8822b"


def test_date_mention() -> None:
    """Test DateMention"""
    params = {
        "start": "2022-12-16",
        "end": None,
    }
    date_mention = DateMention.model_validate(params)
    assert date_mention.start == datetime(2022, 12, 16)
    assert date_mention.end is None
    assert date_mention.time_zone is None

    params = {
        "start": "2022-12-10",
        "end": "2022-12-20",
        "time_zone": "America/Los_Angeles",
    }
    date_mention = DateMention.model_validate(params)
    assert date_mention.start == datetime(2022, 12, 10)
    assert date_mention.end == datetime(2022, 12, 20)
    assert date_mention.time_zone == "America/Los_Angeles"


def test_link_preview_mention() -> None:
    """Test LinkPreviewMention"""
    params = {
        "url": "https://workspace.slack.com/archives/C04PF0F9QSD/z1671139297838409?thread_ts=1671139274.065079&cid=C03PF0F9QSD",
    }
    link_preview_mention = LinkPreviewMention.model_validate(params)
    assert (
        link_preview_mention.url
        == "https://workspace.slack.com/archives/C04PF0F9QSD/z1671139297838409?thread_ts=1671139274.065079&cid=C03PF0F9QSD"
    )


def test_page_mention() -> None:
    """Test PageMention"""
    params = {
        "id": "3c612f56-fdd0-4a30-a4d6-bda7d7426309",
    }
    page_mention = PageMention.model_validate(params)
    assert page_mention.id == "3c612f56-fdd0-4a30-a4d6-bda7d7426309"


def test_template_mention() -> None:
    """Test TemplateMention"""
    params = {
        "type": "template_mention_date",
        "template_mention_date": "today",
    }
    mention_date = TemplateMention.from_notion(params)
    assert mention_date.type == "template_mention_date"
    assert mention_date.template_mention_date == "today"
    assert mention_date.template_mention_user is None

    params = {
        "type": "template_mention_user",
        "template_mention_user": "me",
    }
    mention_user = TemplateMention.from_notion(params)
    assert mention_user.type == "template_mention_user"
    assert mention_user.template_mention_date is None
    assert mention_user.template_mention_user == "me"

    params = {
        "type": "hogehoge",
        "template_mention_user": "me",
    }
    with pytest.raises(ValueError):
        TemplateMention.from_notion(params)


def test_user_mention() -> None:
    """Test UserMention"""
    params = {
        "object": "user",
        "id": "b2e19928-b427-4aad-9a9d-fde65479b1d9",
    }
    user_mention = UserMention.model_validate(params)
    assert user_mention.object == "user"
    assert user_mention.id == "b2e19928-b427-4aad-9a9d-fde65479b1d9"
