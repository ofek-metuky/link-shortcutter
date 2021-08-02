import typing

import pydantic


class LinkItem(pydantic.BaseModel):
    short_name: str
    links: typing.List[str]
