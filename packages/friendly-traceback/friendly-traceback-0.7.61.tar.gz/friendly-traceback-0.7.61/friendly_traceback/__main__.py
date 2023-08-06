"""
main.py
---------------

Sets up the various options when Friendly is invoked from the
command line. You can find more details by doing::

    python -m friendly -h

"""

import argparse
import platform
import runpy
import sys
import warnings
from importlib import import_module
from pathlib import Path

from . import (
    __version__,
    debug_helper,
    exclude_file_from_traceback,
    explain_traceback,
    ft_console,
    install,
    set_formatter,
)
from .ft_gettext import current_lang

versions = f"Friendly-traceback version {__version__}. [Python version: {platform.python_version()}]\n"


def import_function(dotted_path: str) -> type:
    """Import a function from a module, given its dotted path.

    This is a utility function currently used when a custom formatter
    is selected using a command line argument::

        python -m friendly --formatter custom_formatter
    """
    # Used by HackInScience.org
    try:
        module_path, function_name = dotted_path.rsplit(".", 1)
    except ValueError as err:  # pragma: no cover
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, function_name)
    except AttributeError as err:  # pragma: no cover
        raise ImportError(
            'Module "%s" does not define a "%s" function' % (module_path, function_name)
        ) from err


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=(
        """Friendly-traceback makes Python tracebacks easier to understand.

    {versions}

    If no source is given Friendly-traceback will start an interactive console.
        """.format(
            versions=versions
        )
    ),
)

parser.add_argument(
    "source",
    nargs="?",
    help="""Name of the Python script (path/to/my_program.py)
    to be run as though it was the main module, so that its
    __name__ does equal '__main__'.
    """,
)

parser.add_argument(
    "args",
    nargs="*",
    help="""Optional arguments to give to the script specified by source.
         """,
)

parser.add_argument(
    "--lang",
    default="en",
    help="""This sets the language used by Friendly-traceback.
            Usually this is a two-letter code such as 'fr' for French.
         """,
)

parser.add_argument(
    "--version",
    help="""Only displays the current version.
         """,
    action="store_true",
)

parser.add_argument(
    "-f",
    "--formatter",
    help="""Specifies an output format ('bw' or 'docs')
    or a custom formatter function, as a dotted path.
    By default, the console will use 'bw' if it is available.
    """,
)

parser.add_argument("--debug", help="""For developer use.""", action="store_true")
parser.add_argument("--no_debug", help="""For developer use.""", action="store_true")

parser.add_argument(
    "--include",
    help="""Specifies what content to include by default in the traceback.
    The defaults are 'friendly_tb' if the friendly-console is going to be shown,
    otherwise it is 'explain'.
    """,
)


parser.add_argument(
    "--python_prompt",
    help="""Specifies that the console prompt must the standard python prompt.""",
    action="store_true",
)


def main() -> None:
    _ = current_lang.translate
    args = parser.parse_args()
    if args.version:  # pragma: no cover
        print(f"\nFriendly-Traceback version {__version__}")
        sys.exit()

    include = "friendly_tb"
    if args.include:  # pragma: no cover
        include = args.include
    elif args.source and not sys.flags.interactive:
        include = "explain"
    if args.debug:  # pragma: no cover
        debug_helper.DEBUG = True
        include = "debug_tb"
    elif args.no_debug:  # pragma: no cover
        debug_helper.DEBUG = False

    install(lang=args.lang, include=include)

    if args.formatter:
        formatter = args.formatter  # noqa
        if formatter in ["repl", "docs"]:
            set_formatter(formatter)  # pragma: no cover
        else:
            set_formatter(import_function(args.formatter))
            formatter = "repl"  # for the console - should not be needed
    else:
        set_formatter("repl")
        formatter = "repl"

    if sys.flags.interactive:
        warnings.simplefilter("always")

    console_defaults = {}
    if args.source is not None:
        filename = Path(args.source)
        if not filename.exists():  # pragma: no cover
            print(
                "\n",
                _("The file {filename} does not exist.").format(filename=args.source),
            )
            return

        exclude_file_from_traceback(runpy.__file__)
        sys.argv = [args.source, *args.args]
        try:
            module_dict = runpy.run_path(args.source, run_name="__main__")
            console_defaults.update(module_dict)
        except Exception:  # noqa
            explain_traceback()
        if sys.flags.interactive:  # pragma: no cover
            ft_console.start_console(
                local_vars=console_defaults,
                formatter=formatter,
                lang=args.lang,
                ipython_prompt=not args.python_prompt,
            )

    else:  # pragma: no cover
        ft_console.start_console(
            local_vars=console_defaults,
            formatter=formatter,
            lang=args.lang,
            ipython_prompt=not args.python_prompt,
        )


main()
