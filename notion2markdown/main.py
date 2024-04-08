"""main"""

import json
from pathlib import Path

from notion2markdownrkdown.constant import NOTION_TOKEN
from notion2markdownrkdown.exporter.block import (
    MarkdownExporter,
    StringExporter,
)
from notion_client import Client

# https://www.notion.so/Blendle-s-Employee-Handbook-9d5008c2630c4694b1f611c5bd35d774?pvs=4#84cc0a483c81467ab63f140f6965258b


def main() -> None:
    notion = Client(auth=NOTION_TOKEN)

    result = notion.search()

    user_list = notion.users.list()
    # print(user_list)

    notion.search()

    with Path("result.json").open(mode="w") as f:
        json.dump(result, f)

    for block in result["results"]:
        page = notion.pages.retrieve(block["id"])
        # print(page)
        if (
            page["properties"]["title"]["title"][0]["plain_text"]
            != "Package Delivery"
        ):
            continue

        print(page["properties"]["title"])
        print("*" * 100)
        block = notion.blocks.children.list(block["id"])
        for b in block["results"]:
            type_ = b["type"]
            print(b)
            print("-" * 100)

            if b["has_children"]:
                block = notion.blocks.children.list(block["id"])

        print("=" * 100)


if __name__ == "__main__":
    main()


# https://www.notion.so/8ecad96c21da4ab0bc731a4c88344ab1?pvs=4
