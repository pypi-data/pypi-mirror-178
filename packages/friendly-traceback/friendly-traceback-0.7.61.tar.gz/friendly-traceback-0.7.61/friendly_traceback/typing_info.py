"""Custom type definitions and shortcuts for annotating ``friendly_traceback``."""

import os
import sys
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Tuple, TypeVar, Union

if TYPE_CHECKING:
    from _typeshed import StrPath

    from .tb_data import TracebackData
else:
    StrPath = Union[str, os.PathLike]

# TODO see https://www.daan.fyi/writings/python-protocols and define
# a more general exception that could include all possible fields
# declared as optional
# including new ones for SyntaxError in Python 3.10+
_E = TypeVar("_E", bound=BaseException)


if sys.version_info >= (3, 8):
    from typing import Literal, Protocol, TypedDict

    InclusionChoice = Literal[
        "message",
        "hint",
        "what",
        "why",
        "where",
        "friendly_tb",
        "python_tb",
        "debug_tb",
        "explain",
        "no_tb",
    ]

    class Info(TypedDict, total=False):
        header: str
        message: str
        original_python_traceback: str
        simulated_python_traceback: str
        shortened_traceback: str
        exception_notes_intro: List[str]
        exception_notes: str
        suggest: str
        generic: str
        parsing_error: str
        parsing_error_source: str
        cause: str
        detailed_tb: List[str]
        last_call_header: str
        last_call_source: str
        last_call_variables: str
        exception_raised_header: str
        exception_raised_source: str
        exception_raised_variables: str
        warning_message: str
        warning_location_header: str
        warning_source: str
        warning_variables: str
        additional_variable_warning: str
        lang: str
        _tb_data: "TracebackData"

    class Formatter(Protocol):
        def __call__(self, info: Info, include: InclusionChoice = ...) -> str:
            ...

    class CauseInfo(TypedDict, total=False):
        cause: str
        suggest: str

    Site = Literal["friendly", "python", "bug", "email"]

    ScopeKind = Literal["local", "global", "nonlocal"]

    ObjectsInfo = TypedDict(
        "ObjectsInfo",
        {
            "locals": List[Tuple[str, str, Any]],
            "globals": List[Tuple[str, str, Any]],
            "builtins": List[Tuple[str, str, Any]],
            "expressions": List[Tuple[str, Any]],
            "name, obj": List[Tuple[str, Any]],
        },
    )
    SimilarNamesInfo = TypedDict(
        "SimilarNamesInfo",
        {"locals": List[str], "globals": List[str], "builtins": List[str], "best": str},
    )

else:
    InclusionChoice = str
    Info = Dict[str, str]
    Formatter = Callable[[Info, InclusionChoice], str]
    Site = str
    CauseInfo = Dict[str, str]
    ScopeKind = str
    ObjectsInfo = Dict[str, List[Any]]
    SimilarNamesInfo = Dict[str, List[str]]


GenericExplain = Callable[[], str]
Parser = Union[
    Callable[[str, "TracebackData"], CauseInfo],
    Callable[[_E, "TracebackData"], CauseInfo],
]
Translator = Callable[[str], str]
Writer = Callable[[str], None]
