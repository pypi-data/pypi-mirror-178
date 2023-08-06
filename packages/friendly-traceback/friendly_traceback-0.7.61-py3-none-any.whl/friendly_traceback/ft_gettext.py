"""ft_gettext.py

The usual pattern when using gettext is to surround strings to be translated
by a call to a function named _, as in

    _("This string should be translated.")

This is done when having gettext "install" a given language: it adds a function
named _ to the global builtins. However, this can fail if some other program,
such as the Python REPL, also modifies the builtins and define _ in its own
ways.

To avoid such problems, we use a custom class that keep track of the language
preferred for the translation.  Inside any namespace, when we need to
provide a translation, we define locally _ to be

    _ = current_lang.translate

where current_lang.translate means gettext.translation().gettext where
gettext.translation() is the class-based API for gettext.
"""

import gettext
import os
from typing import Optional

from . import debug_helper
from .typing_info import Translator


class LangState:
    def __init__(self) -> None:
        self._translate: Translator = lambda text: text
        self.lang = "en"

    def install(self, lang: Optional[str] = None) -> None:
        """Sets the language to be used for translations"""
        if lang is None:
            lang = "en"
        try:
            # We first look for the exact language requested.
            _lang = gettext.translation(
                f"friendly_tb_{lang}",
                localedir=os.path.normpath(
                    os.path.join(os.path.dirname(__file__), "locales")
                ),
                languages=[lang],
                fallback=False,
            )
        except FileNotFoundError:
            # If it is not available, we make it possible to replace a
            # language specific to a region, as in fr_CA, by a more
            # generic version, such as fr, defined by a two-letter code.
            lang = lang[:2]
            _lang = gettext.translation(
                f"friendly_tb_{lang}",
                localedir=os.path.normpath(
                    os.path.join(os.path.dirname(__file__), "locales")
                ),
                languages=[lang],
                fallback=True,  # This means that the hard-coded strings in
                # the source file will be used if the requested language
                # is not available.
            )

        self.lang = lang
        self._translate = _lang.gettext

    def translate(self, text: str) -> str:
        translation = self._translate(text)
        if translation == text and self.lang == "fr":  # pragma: no cover
            debug_helper.log(f"Potentially untranslated text for {self.lang}:")
            debug_helper.log(text)
        return translation


current_lang = LangState()  # noqa
_ = current_lang.translate


def please_report() -> str:
    return _(
        "Please report this example to\n"
        "https://github.com/friendly-traceback/friendly-traceback/issues/new\n"
        "If you are using a REPL, use `www('bug')` to do so.\n\n"
    )


def unknown_case() -> str:
    return _("Friendly-traceback does not know the cause of this error.\n")


def no_information() -> str:
    debug_helper.log("New case to consider.")
    return (
        _("No information is known about this exception.\n")
        + please_report()
        + _(
            "If you are using the Friendly console, use `www()` to\n"
            "do an Internet search for this particular case.\n"
        )
    )


def internal_error(e: Optional[BaseException]) -> str:
    debug_helper.log(f"--> Internal error: {repr(e)}")
    return _("Internal error for Friendly.\n") + please_report()
