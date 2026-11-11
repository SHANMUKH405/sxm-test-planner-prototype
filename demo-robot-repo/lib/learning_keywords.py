from robot.api.deco import keyword

_content = ""
_source = "SiriusXM"


@keyword("Reset Learning Simulator")
def reset() -> None:
    global _content, _source
    _content, _source = "", "SiriusXM"


@keyword("Set Learning Content")
def set_content(search: str, now_playing: str) -> None:
    global _content, _source
    if not search.strip() or not now_playing.strip():
        raise ValueError("Expected non-empty learning content")
    _content, _source = now_playing, "SiriusXM"


@keyword("Set Learning Source")
def set_source(source: str) -> None:
    global _source
    _source = source


@keyword("Read Learning Source")
def read_source() -> str:
    return _source


@keyword("Read Learning Content")
def read_content() -> str:
    return _content
