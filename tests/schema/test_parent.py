"""test parent.py"""

from notion2markdown.schema.parent import Parent


def test_parent() -> None:
    """Test Parent"""
    workspace_parent_params = {
        "type": "workspace",
        "workspace": True,
    }
    workspace_parent = Parent.from_notion(workspace_parent_params)
    assert workspace_parent.type == "workspace"
    assert workspace_parent.workspace

    database_parent_params = {
        "type": "database_id",
        "database_id": "d9824bdc-8445-4327-be8b-5b47500af6ce",
    }
    database_parent = Parent.from_notion(database_parent_params)
    assert database_parent.type == "database_id"
    assert database_parent.id == "d9824bdc-8445-4327-be8b-5b47500af6ce"
