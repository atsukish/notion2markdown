from typing import (
    Awaitable,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    TypedDict,
    Union,
)

from notion_client import Client


class BlockAttributes(TypedDict, total=False):
    numbered_list_item: Optional[Dict[str, int]]


# Simplified for Python; we don't directly translate the "&" operation but rather merge the relevant fields manually
class ListBlockChildrenResponseResult(TypedDict):
    type: str  # Assuming all blocks have a 'type' field
    # Add other common fields from ListBlockChildrenResponse["results"] items here
    numbered_list_item: Optional[
        Dict[str, int]
    ]  # Example of extending with BlockAttributes


TextRequest = str

# Enum-like handling for BlockType in Python
BlockType = Union[
    Literal[
        "image",
        "video",
        "file",
        "pdf",
        "table",
        "bookmark",
        "embed",
        "equation",
        "divider",
        "toggle",
        "to_do",
        "bulleted_list_item",
        "numbered_list_item",
        "synced_block",
        "column_list",
        "column",
        "link_preview",
        "link_to_page",
        "paragraph",
        "heading_1",
        "heading_2",
        "heading_3",
        "quote",
        "template",
        "child_page",
        "child_database",
        "code",
        "callout",
        "breadcrumb",
        "table_of_contents",
        "audio",
        "unsupported",
    ],
    str,  # Allows for extending with custom string types
]


class ConfigurationOptions(TypedDict, total=False):
    separateChildPage: Optional[bool]
    convertImagesToBase64: Optional[bool]
    parseChildPages: Optional[bool]


class NotionToMarkdownOptions(TypedDict):
    notionClient: Client
    config: Optional[ConfigurationOptions]


MdStringObject = Dict[str, str]


class MdBlock(TypedDict):
    type: Optional[str]
    blockId: str
    parent: str
    children: List["MdBlock"]


class Annotations(TypedDict):
    bold: bool
    italic: bool
    strikethrough: bool
    underline: bool
    code: bool
    color: Union[
        Literal[
            "default",
            "gray",
            "brown",
            "orange",
            "yellow",
            "green",
            "blue",
            "purple",
            "pink",
            "red",
            "gray_background",
            "brown_background",
            "orange_background",
            "yellow_background",
            "green_background",
            "blue_background",
            "purple_background",
            "pink_background",
            "red_background",
        ]
    ]


class Text(TypedDict):
    type: Literal["text"]
    text: Dict[str, Union[str, Optional[Dict[str, TextRequest]]]]
    annotations: Annotations
    plain_text: str
    href: Optional[str]


class Equation(TypedDict):
    type: Literal["equation"]
    equation: Dict[str, str]
    annotations: Annotations
    plain_text: str
    href: None


CalloutIcon = Optional[Dict[str, Union[Optional[str], Dict[str, str]]]]

# For custom transformers, using Callable to define a function type hint
CustomTransformer = Callable[
    [ListBlockChildrenResponseResult],
    Union[str, bool, Awaitable[Union[str, bool]]],
]
