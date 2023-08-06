from ..ft_gettext import current_lang
from ..message_parser import get_parser
from ..tb_data import TracebackData  # for type checking only
from ..typing_info import CauseInfo  # for type checking only

parser = get_parser(OSError)
_ = current_lang.translate


@parser._add
def handle_connection_error(_message: OSError, tb_data: TracebackData) -> CauseInfo:
    tb = "\n".join(tb_data.formatted_tb)
    if (
        "socket.gaierror" in tb
        or "urllib.error" in tb
        or "urllib3.exception" in tb
        or "requests.exception" in tb
    ):
        cause = _(
            "I suspect that you are trying to connect to a server and\n"
            "that a connection cannot be made.\n\n"
            "If that is the case, check for typos in the URL\n"
            "and check your internet connectivity.\n"
        )
        return {"cause": cause}
    return {}


@parser._add
def invalid_argument(message: str, tb_data: TracebackData) -> CauseInfo:
    if "Invalid argument:" not in message:
        return {}
    value = tb_data.value
    filename = value.filename
    repr_filename = repr(filename)
    if "\\" not in filename and "\\" in repr_filename:
        hint = _("Perhaps you need to double the backslash characters.\n")
        cause = _(
            "I suspect that you wrote a filename or path that contains\n"
            "at least one backslash character, `\\`.\n"
            "Python likely interpreted this as indicating the beginning of\n"
            "what is known as an escape sequence.\n"
            "To solve the problem, either write a so-called 'raw string'\n"
            "by adding the letter `r` as a prefix in\n"
            "front of the filename or path, or replace all single backslash\n"
            "characters, `\\`, by double ones: `\\\\`.\n"
        )
        return {"cause": cause, "suggest": hint}
    return {}
