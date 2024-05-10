"""test md.py"""

from notion2markdown.md import (
    bold,
    bullet,
    callout,
    code_block,
    divider,
    equation,
    heading1,
    heading2,
    heading3,
    image,
    inline_code,
    inline_equation,
    italic,
    link,
    quote,
    strikethrough,
    table,
    todo,
    toggle,
    underline,
)


def test_md() -> None:
    """Test md"""
    assert inline_code("inline-code") == "`inline-code`"
    assert inline_equation("inline-equation") == "$inline-equation$"
    assert bold("太字だよー") == "**太字だよー**"
    assert italic("イタリック") == "_イタリック_"
    assert strikethrough("取り消し線ですよ") == "~~取り消し線ですよ~~"
    assert underline("下線を引きましょう") == "<u>下線を引きましょう</u>"
    assert (
        link(text="Github", href="https://github.com")
        == "[Github](https://github.com)"
    )
    assert (
        code_block(text="print('Hello, World!')", language="python")
        == "```python\nprint('Hello, World!')\n```"
    )
    assert code_block(text="this is a pen.") == "```\nthis is a pen.\n```"
    assert (
        code_block(text="this is simple text.", language="plain text")
        == "```text\nthis is simple text.\n```"
    )
    assert equation("E=mc^2") == "$$\nE=mc^2\n$$"
    assert heading1("title") == "# title"
    assert heading2("chapter1") == "## chapter1"
    assert heading3("section2") == "### section2"
    assert (
        quote("のびのび\nいきいき\nぴちぴち")
        == "> のびのび  \n> いきいき  \n> ぴちぴち"
    )
    assert (
        callout(text="のびのび\nいきいき\nぴちぴち", icon="🥺")
        == "<aside>\n🥺 のびのび\nいきいき\nぴちぴち\n</aside>"
    )
    assert (
        bullet(text="If you can dream it, you can do it.")
        == "- If you can dream it, you can do it."
    )
    assert (
        bullet(text="Every day is a new day", count=3)
        == "3. Every day is a new day"
    )
    assert todo(text="done", checked=True) == "- [x] done"
    assert todo(text="todo", checked=False) == "- [ ] todo"
    assert (
        image(
            alt="amazon logo",
            href="https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
        )
        == "![amazon logo](https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg)"
    )
    assert divider() == "\n---\n"
    assert toggle(summary="summary", children="children") == (
        "<details>\n<summary>summary</summary>\nchildren\n</details>\n\n"
    )
    assert toggle(children="children") == "children"
    assert table(
        data=[["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]],
        headers=["c1", "c2", "c3"],
    ) == (
        "|   c1 |   c2 |   c3 |\n"
        "|------|------|------|\n"
        "|    1 |    2 |    3 |\n"
        "|    4 |    5 |    6 |\n"
        "|    7 |    8 |    9 |"
    )
