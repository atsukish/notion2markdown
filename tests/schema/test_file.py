"""test file.py"""

from datetime import datetime, timezone

from notion2markdown.schema.file import FileObject


def test_file_object() -> None:
    """Teest FileObject"""
    base_params = {
        "caption": [],
        "type": "file",
        "file": {
            "url": "https://s3.us-west-2.amazonaws.com/secure.notion-static.com/7b8b0713-dbd4-4962-b38b-955b6c49a573/My_test_image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20221024%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20221024T205211Z&X-Amz-Expires=3600&X-Amz-Signature=208aa971577ff05e75e68354e8a9488697288ff3fb3879c2d599433a7625bf90&X-Amz-SignedHeaders=host&x-id=GetObject",
            "expiry_time": "2022-10-24T22:49:22.765Z",
        },
    }
    base_file = FileObject.from_notion(base_params)

    assert base_file.type == "file"
    assert (
        base_file.url
        == "https://s3.us-west-2.amazonaws.com/secure.notion-static.com/7b8b0713-dbd4-4962-b38b-955b6c49a573/My_test_image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20221024%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20221024T205211Z&X-Amz-Expires=3600&X-Amz-Signature=208aa971577ff05e75e68354e8a9488697288ff3fb3879c2d599433a7625bf90&X-Amz-SignedHeaders=host&x-id=GetObject"
    )
    assert base_file.expiry_time == datetime(
        2022,
        10,
        24,
        22,
        49,
        22,
        765000,
        tzinfo=timezone.utc,
    )
    assert base_file.caption == []

    external_file_params = {
        "type": "external",
        "external": {
            "url": "https://images.unsplash.com/photo-1525310072745-f49212b5ac6d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1065&q=80",
        },
    }
    external_file = FileObject.from_notion(external_file_params)
    assert external_file.type == "external"
    assert (
        external_file.url
        == "https://images.unsplash.com/photo-1525310072745-f49212b5ac6d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1065&q=80"
    )
    assert external_file.caption == []
