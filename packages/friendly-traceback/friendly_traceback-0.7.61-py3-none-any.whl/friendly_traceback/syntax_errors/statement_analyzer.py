# type: ignore
"""This module contains functions that are used to
   analyze a single statement which has been identified
   as containing a syntax error with the message "invalid syntax".
"""
import keyword
import sys

from .. import debug_helper, token_utils, utils
from ..ft_gettext import current_lang, internal_error
from . import error_in_def, fixers
from . import syntax_utils as su

STATEMENT_ANALYZERS = []
_ = current_lang.translate


def more_errors():

    return "\n" + _(
        "However, making such a change would still not correct\n"
        "all the syntax errors in the code you wrote.\n"
    )


def _possibly_inside_dict(statement):
    if statement.statement_brackets:
        return False
    for bracket in reversed(statement.begin_brackets):
        if bracket == "{":
            break
    else:
        return False
    between_brackets = False
    found_colon = False
    for token in statement.tokens:
        if token == bracket:
            between_brackets = True
        if between_brackets:
            if token == ":":
                found_colon = True
            elif token.is_keyword():
                return False
            if token == "}":
                return found_colon
    return False


def add_statement_analyzer(func):
    """A simple decorator that adds a function to the list
    of all functions that analyze a single statement."""
    STATEMENT_ANALYZERS.append(func)

    # The following is needed if we wish to call explicitly
    # one of the functions below from another file.
    # We sometimes do this for consistency when later version of
    # Python give us a specific message instead of just 'invalid syntax'.
    def wrapper(statement):
        return func(statement)

    return wrapper


# ========================================================
# Main calling function
# ========================================================


def analyze_statement(statement):
    """Analyzes the statement as identified by Python as that
    on which the error occurred."""
    if not statement.tokens:  # pragma: no cover
        debug_helper.log("Statement with no tokens in statement_analyser.py")
        return {"cause": internal_error(Exception("No tokens"))}

    if statement.first_token == "def" or (
        statement.first_token == "async" and statement.tokens[1] == "def"
    ):
        cause = error_in_def.analyze_def_statement(statement)
        if cause:
            return cause

    for analyzer in STATEMENT_ANALYZERS:
        cause = analyzer(statement)
        if cause:
            return cause
    return {}


# ==================
# IMPORTANT: causes are looked at in the same order as they appear below.
# Changing the order could possibly yield incorrect results
# ==================


@add_statement_analyzer
def invalid_non_printable_character(statement=None):
    # new message for Python 3.11
    # invalid non-printable character ...
    char = statement.bad_token.string
    if (
        statement.bad_token.name() == "ERRORTOKEN"
        and len(char) == 1
        and su.is_invisible_control_character(char) == char
    ):
        return {
            "cause": _(
                "Your code contains the invalid non-printable character {char}.\n"
            ).format(char=repr(char))
        }
    return {}


@add_statement_analyzer
def missing_index(statement=None):
    if not (statement.bad_token == "]" and statement.prev_token == "["):
        return {}
    new_tokens = []
    for tok in statement.tokens:
        if (
            tok is statement.bad_token
        ):  # Check for identity as other brackets might be present
            new_tokens.append("0")
        new_tokens.append(tok)

    new_line = token_utils.untokenize(new_tokens)
    if not fixers.check_statement(new_line):
        return {}
    hint = _("Did you forget to add an index?\n")
    cause = _(
        "It looks like you forgot to add an index.\n"
        "Perhaps you meant to write something like:\n\n"
        "    {new_line}"
    ).format(new_line=new_line)
    return {"cause": cause, "suggest": hint}


@add_statement_analyzer
def mismatched_brackets(statement):
    """Detecting code that ends with an unmatched closing bracket"""
    if not (statement.end_bracket and statement.bad_token == statement.last_token):
        return {}

    if not statement.statement_brackets:
        lineno = statement.end_bracket.start_row
        source = f"\n    {lineno}: {statement.source_lines[lineno - 1]}"
        shift = len(str(lineno)) + statement.end_bracket.start_col + 6
        source += " " * shift + "^\n"

        cause = (
            _(
                "The closing {bracket} on line {linenumber}"
                " does not match anything.\n"
            ).format(
                bracket=su.name_bracket(statement.end_bracket),
                linenumber=statement.end_bracket.start_row,
            )
            + source
        )

        return {"cause": cause}

    open_bracket = statement.begin_brackets[-1]
    open_lineno = open_bracket.start_row
    end_bracket = statement.end_bracket
    end_lineno = end_bracket.start_row

    source = f"\n    {open_lineno}: {statement.source_lines[open_lineno - 1]}"
    shift = len(str(open_lineno)) + open_bracket.start_col + 6
    statement.location_markers = {}
    if open_lineno == end_lineno:
        source += " " * shift + "^"
        statement.location_markers[open_lineno] = " " * open_bracket.start_col + "^"
        shift = end_bracket.start_col - open_bracket.start_col - 1
        source += " " * shift + "^\n"
        statement.location_markers[open_lineno] += " " * shift + "^"
    else:
        source += " " * shift + "^\n"
        statement.location_markers[open_lineno] = " " * open_bracket.start_col + "^"
        source += f"    {end_lineno}: {statement.source_lines[end_lineno - 1]}"
        shift = len(str(end_lineno)) + end_bracket.start_col + 6
        source += " " * shift + "^\n"
        statement.location_markers[end_lineno] = " " * end_bracket.start_col + "^"

    cause = (
        _(
            "The closing {bracket} on line {close_lineno} does not match "
            "the opening {open_bracket} on line {open_lineno}.\n"
        ).format(
            bracket=su.name_bracket(statement.end_bracket),
            close_lineno=statement.end_bracket.start_row,
            open_bracket=su.name_bracket(open_bracket),
            open_lineno=open_bracket.start_row,
        )
        + source
    )
    return {"cause": cause}


@add_statement_analyzer
def copy_pasted_code(statement):
    """Detecting code that starts with a Python prompt"""
    first_token = statement.first_token
    if first_token not in [">>", "..."]:
        return {}

    if statement.bad_line.strip() == "....":
        hint = _("Did you mean to write `...`?\n")
        cause = _(
            "It looks like you meant to write `...` but added an extra `.` by mistake.\n"
        )
        return {"cause": cause, "suggest": hint}

    hint = _("Did you use copy-paste?\n")
    if (
        first_token == ">>"
        and first_token == statement.bad_token
        and statement.next_token == ">"
    ):
        statement.location_markers = su.highlight_two_tokens(
            first_token, statement.next_token
        )
        cause = _(
            "It looks like you copy-pasted code from an interactive interpreter.\n"
            "The Python prompt, `>>>`, should not be included in your code.\n"
        )
        return {"cause": cause, "suggest": hint}
    elif (
        statement.first_token == statement.bad_token
        or statement.prev_token == statement.first_token
    ):
        statement.location_markers = su.highlight_single_token(statement.first_token)
        cause = _(
            "It looks like you copy-pasted code from an interactive interpreter.\n"
            "The Python prompt, `...`, should not be included in your code.\n"
        )
        return {"cause": cause, "suggest": hint}
    return {}  # pragma: no cover


@add_statement_analyzer
def detect_backquote(statement):
    """Detecting if the error is due to using `x` which was allowed
    in Python 2.
    """
    if statement.bad_token == "`":
        hint = _("You should not use the backquote character.\n")
        cause = _(
            "You are using the backquote character.\n"
            "Either you meant to write a single quote, ', "
            "or copied Python 2 code;\n"
            "in this latter case, use the function `repr(x)`."
        )
        return {"cause": cause, "suggest": hint}
    return {}


@add_statement_analyzer
def wrong_code_block(statement):
    if not (
        statement.bad_token == ":"
        and statement.nb_tokens == 2
        and statement.prev_token.string in ("if", "for", "while", "class")
    ):
        return {}

    word = statement.prev_token.string
    if word in ("if", "while"):
        hint = _("You forgot to add a condition.\n")
        if word == "if":
            cause = _(
                "An `if` statement requires a condition:\n\n"
                "    if condition:\n"
                "        ...\n\n"
            )
        else:
            cause = _(
                "A `while` loop requires a condition:\n\n"
                "    while condition:\n"
                "        ...\n\n"
            )
    elif word == "for":
        hint = _("A `for` loop requires at least 3 more terms.\n")
        cause = _(
            "A `for` loop is an iteration over a sequence:\n\n"
            "    for element in sequence:\n"
            "        ...\n\n"
        )
    else:
        hint = _("A class needs a name.\n")
        cause = _(
            "A `class` statement requires a name:\n\n"
            "    class SomeName:\n"
            "        ...\n\n"
        )

    return {"cause": cause, "suggest": hint}


@add_statement_analyzer
def keyword_as_attribute(statement):
    """Will identify something like  obj.True ..."""
    if statement.prev_token != ".":
        return {}

    word = statement.bad_token
    if word.is_keyword():
        cause = _(
            "You cannot use the Python keyword `{word}` as an attribute.\n\n"
        ).format(word=word)
    else:
        return {}

    hint = _("`{word}` cannot be used as an attribute.\n").format(word=word)
    return {"cause": cause, "suggest": hint}


@add_statement_analyzer
def confused_elif(statement):
    name = None
    # skipcq: PYL-R1714
    if statement.bad_token == "elseif" or statement.prev_token == "elseif":
        name = "elseif"
        if statement.first_token == "elseif":
            statement.location_markers = su.highlight_single_token(
                statement.first_token
            )
        else:
            debug_helper.log("problem in confused_elif")
    elif statement.bad_token == "if" and statement.prev_token == "else":
        name = "else if"
        statement.location_markers = su.highlight_two_tokens(
            statement.prev_token, statement.bad_token, between="^"
        )
    if name:
        hint = _("Perhaps you meant to write `elif`.\n")
        cause = _(
            "You likely meant to use Python's `elif` keyword\n"
            "but wrote `{name}` instead.\n"
            "\n"
        ).format(name=name)
        return {"cause": cause, "suggest": hint}
    return {}


@add_statement_analyzer
def import_from(statement):
    if statement.bad_token != "from" or statement.tokens[0] != "import":
        return {}

    statement.location_markers = su.highlight_two_tokens(
        statement.tokens[0], statement.bad_token
    )
    bad_line = statement.bad_line.replace("import ", "").strip()
    function, module = bad_line.split(" from ")
    new_line = f"from {module} import {function}"
    if not fixers.check_statement(new_line):
        function = module = "(...)"

    hint = _("Did you mean `from {module} import {function}`?\n").format(
        module=module.strip(), function=function.strip()
    )
    cause = _(
        "You wrote something like\n\n"
        "    import {function} from {module}\n\n"
        "instead of\n\n"
        "    from {module} import {function}\n\n"
    ).format(module=module.strip(), function=function.strip())
    return {"cause": cause, "suggest": hint}


@add_statement_analyzer
def misplaced_quote(statement):
    """This looks for a single misplaced quote, something like
       info = 'I don't mind.'

    The clue we are looking for is a STRING token ('don')
    followed by something else than a string.
    """
    if not statement.prev_token.is_string():
        return {}

    # Create a new line escaping an inner quote for the entire line.
    new_tokens = []
    for tok in statement.tokens:
        if tok == statement.prev_token:
            s = tok.string[:-1] + tok.string[-1].replace("'", "\\'").replace('"', '\\"')
            tok_copy = statement.prev_token.copy()
            tok_copy.string = s
            new_tokens.append(tok_copy)
        else:
            new_tokens.append(tok)

    new_line = token_utils.untokenize(new_tokens)
    if not fixers.check_statement(new_line):
        return {}

    quote_position = statement.prev_token.end_col
    indent = len(statement.bad_line) - len(statement.bad_line.lstrip())
    quote_position -= indent
    mark = " " * (quote_position - 1) + "^^"

    hint = _("Perhaps you forgot to escape a quote character.\n")
    cause = _(
        "I suspect that you were trying to use a quote character inside a string\n"
        "that was enclosed in quotes of the same kind.\n"
        "Perhaps you should have escaped the inner quote character:\n\n"
        "    {new_line}\n"
        "    {mark}\n"
    ).format(new_line=new_line, mark=mark)
    return {"cause": cause, "suggest": hint}


@add_statement_analyzer
def detect_walrus(statement):
    """Detecting if code uses named assignment operator := with an
    older version of Python.
    """
    if sys.version_info >= (3, 8):
        return {}

    # Normally, the token identified as the bad token should be
    # '='; however, in some test cases where a named assignment
    # is not allowed, it is ':' that is identified as the
    # bad token.

    bad = statement.bad_token
    prev = statement.prev_token
    next_token = statement.next_token

    if (prev == ":" and bad == "=" and bad.immediately_after(prev)) or (
        bad == ":" and next_token == "=" and bad.immediately_before(next_token)
    ):
        hint = _(
            "The augmented assignment operator is not allowed in Python version {version}.\n"
        ).format(version=f"{sys.version_info.major}.{sys.version_info.minor}")
        cause = _(
            "You appear to be using the operator `:=`, sometimes called\n"
            "the walrus operator. This operator requires the use of\n"
            "Python 3.8 or newer. You are using version {version}.\n"
        ).format(version=f"{sys.version_info.major}.{sys.version_info.minor}")
        return {"cause": cause, "suggest": hint}

    return {}


@add_statement_analyzer
def inverted_operators(statement):
    """Detect if operators might have been inverted"""
    is_op = token_utils.is_operator
    if not is_op(statement.bad_token):
        return {}

    prev = statement.prev_token
    bad = statement.bad_token
    next_ = statement.next_token

    if is_op(prev) and is_op(bad.string + prev.string) and prev.immediately_before(bad):
        first = prev
        second = bad
    elif (
        is_op(next_)
        and is_op(next_.string + bad.string)
        and bad.immediately_before(next_)
    ):  # pragma: no cover
        # I cannot think of a situation where Python would highlight the first
        # of two consecutive operators as being the incorrect one.
        debug_helper.log("inverted_operators: new case")
        first = bad
        second = next_
    else:
        return {}

    # Before we make any attempt at modifying the original code,
    # we make sure that our statement checker can properly identify that
    # the original code is invalid. See #205
    if fixers.check_statement(statement.bad_line):
        return {}

    correct = second.string + first.string
    hint = _("Did you write operators in an incorrect order?\n")
    cause = _(
        "It looks like you wrote two operators (`{first}` and `{second}`)\n"
        "in the wrong order: `{wrong}` instead of `{correct}`.\n"
    ).format(
        first=first.string,
        second=second.string,
        correct=correct,
        wrong=first.string + second.string,
    )
    statement.location_markers = su.highlight_two_tokens(first, second)

    new_statement = fixers.replace_two_tokens(
        statement.statement_tokens,
        first,
        first_string=correct,
        second_token=second,
        second_string="",
    )
    if fixers.check_statement(new_statement):
        return {"cause": cause, "suggest": hint}

    return {"cause": cause + more_errors(), "suggest": hint}


@add_statement_analyzer
def consecutive_operators(statement):
    is_op = token_utils.is_operator

    if not (is_op(statement.bad_token) and is_op(statement.prev_token)):
        return {}

    statement.location_markers = su.highlight_two_tokens(
        statement.prev_token, statement.bad_token
    )

    if statement.bad_token == "=" and statement.prev_token == "==":
        cause = _(
            "You wrote three equal signs in a row which is allowed in some\n"
            "programming languages, but not in Python. To check if two objects\n"
            "are equal, use two equal signs, `==`; to see if two names represent\n"
            "the exact same object, use the operator `is`.\n"
        )
        hint = _("Did you mean to use `is` instead of `===`?\n")
        return {"cause": cause, "suggest": hint}

    if statement.bad_token == statement.prev_token:
        cause = _(
            "You cannot have write the same operator, `{op}`, twice in a row.\n"
            "Perhaps you wrote one of them by mistake\n"
            "or forgot to write something between them.\n"
        ).format(op=statement.prev_token)
    else:
        if (
            statement.prev_token == ":"
            and statement.bad_token == "*"
            and _possibly_inside_dict(statement)
        ):
            cause = _(
                "You cannot have these two operators, `{first}` and `{second}`,\n"
                "following each other.\n"
                "It looks like you tried to use a starred expression as a dict value;\n"
                "this is not allowed.\n"
            ).format(first=statement.prev_token, second=statement.bad_token)
            new_statement = fixers.replace_token(
                statement.statement_tokens, statement.bad_token, ""
            )
            # See issue 205
            if fixers.check_statement(new_statement) and not fixers.check_statement(
                statement.bad_line
            ):
                cause += "\n" + _(
                    "The following statement has no syntax error:\n\n    {statement}\n"
                ).format(statement=new_statement)
            return {"cause": cause}
        cause = _(
            "You cannot have these two operators, `{first}` and `{second}`,\n"
            "following each other. Perhaps you wrote one of them by mistake\n"
            "or forgot to write something between them.\n"
        ).format(first=statement.prev_token, second=statement.bad_token)

    if is_op(statement.prev_token.string + statement.bad_token.string):
        cause += _(
            "Or perhaps you included a space by mistake between the two operators\n"
            "and meant to write `{oper}` as a single operator.\n"
        ).format(oper=statement.prev_token.string + statement.bad_token.string)
    return {"cause": cause}


def _walrus_instead_of_equal_39(statement):
    # Python version 3.9 identifies a token beyond :=
    for tok in statement.statement_tokens[: statement.bad_token_index + 1]:
        if tok == ":=":
            return tok
    return None


@add_statement_analyzer
def walrus_instead_of_equal(statement):
    # TODO: check this
    if (3, 8) < sys.version_info < (3, 10):
        bad_token = _walrus_instead_of_equal_39(statement)
        if bad_token is None:
            return {}
    elif statement.bad_token != ":=":
        return {}
    else:
        bad_token = statement.bad_token

    # Before we make any attempt at modifying the original code,
    # we make sure that our statement checker can properly identify that
    # the original code is invalid. See #205
    if fixers.check_statement(statement.bad_line):
        return {}

    new_statement = fixers.replace_token(statement.statement_tokens, bad_token, "=")
    if fixers.check_statement(new_statement):
        hint = _("Did you mean to use `=`?\n")
        cause = _(
            "You use the augmented assignment operator `:=` where\n"
            "the normal assignment operator `=` was required.\n"
        )
        return {"cause": cause, "suggest": hint}
    return {}


@add_statement_analyzer
def assign_instead_of_equal(statement):
    """Checks to see if an assignment sign, '=', has been used instead of
    an equal sign, '==', in an if, elif or while statement."""
    if statement.filename == "<fstring>":
        return {}
    if statement.highlighted_tokens:  # Python 3.10
        bad_token = statement.next_token
    else:
        bad_token = statement.bad_token

    if bad_token != "=":
        return {}

    # Before we make any attempt at modifying the original code,
    # we make sure that our statement checker can properly identify that
    # the original code is invalid. See #205
    if fixers.check_statement(statement.bad_line):
        return {}

    new_statement = fixers.replace_token(statement.statement_tokens, bad_token, "==")
    if not fixers.check_statement(new_statement):
        return {}

    new_statement = fixers.replace_token(statement.statement_tokens, bad_token, ":=")
    walrus = fixers.check_statement(new_statement)

    if not walrus:
        hint = _("Perhaps you needed `==` instead of `=`.\n")
        cause = _(
            "You likely used an assignment operator `=` instead of an equality operator `==`.\n"
        )
        for tok in statement.tokens[statement.bad_token_index :]:
            if tok == "=":
                new_statement = fixers.replace_token(
                    statement.statement_tokens, tok, "=="
                )
                if fixers.check_statement(new_statement):
                    cause += _(
                        "The following statement would not contain a syntax error:\n\n"
                        "    {new_statement}"
                    ).format(new_statement=new_statement)
        return {"cause": cause, "suggest": hint}

    hint = _("Perhaps you needed `==` or `:=` instead of `=`.\n")
    cause = _(
        "You used an assignment operator `=`; perhaps you meant to use \n"
        "an equality operator, `==`, or the walrus operator `:=`.\n"
    )
    return {"cause": cause, "suggest": hint}


@add_statement_analyzer
def print_as_statement(statement):
    # example: print len('hello')
    if not (
        (  # Python 3.10+
            statement.bad_token == statement.first_token == "print"
            and statement.highlighted_tokens is not None
        )
        or (  # Python < 3.10
            statement.prev_token == statement.first_token == "print"
            and statement.bad_token != "("
        )
    ):
        return {}
    # Before we make any attempt at modifying the original code,
    # we make sure that our statement checker can properly identify that
    # the original code is invalid. See #205
    if fixers.check_statement(statement.bad_line):
        return {}

    content = statement.entire_statement.replace("print", "", 1).strip()
    possible_statement = f"print({content})"
    valid = fixers.check_statement(possible_statement)
    if "\n" in content or len(content) > 40 or not valid:
        message = "..."
    else:
        message = content
    cause = _(
        "Perhaps you need to type\n\n"
        "     print({message})\n\n"
        "In older version of Python, `print` was a keyword.\n"
        "Now, `print` is a function; you need to use parentheses to call it.\n"
    ).format(message=message)
    if not valid:
        cause += _("Note that arguments of `print` must be separated by commas.\n")
    hint = _("Did you mean `print({message})`?\n").format(message=message)
    return {"cause": cause, "suggest": hint}


@add_statement_analyzer
def calling_python_or_pip(statement):
    if statement.first_token.string not in ("pip", "python", "python3"):
        return {}
    # A single token statement with 'python' or 'pip' should not have
    # caused a SyntaxError
    second = statement.tokens[1]
    # python followed by an operator is likely a valid statement.
    # One exception is something like python -im friendly  :)
    if second.is_operator() and second != "-":
        return {}

    cause = _(
        "It looks as if you are attempting to use pip to install a module.\n"
        "`pip` is a command that needs to run in a terminal,\n"
        "not from a Python interpreter.\n"
    )

    for tok in statement.tokens:
        if tok == "pip":
            hint = _("Pip cannot be used in a Python interpreter.\n")
            return {"cause": cause, "suggest": hint}

    cause = _(
        "I am guessing that you are attempting to use Python to run a program.\n"
        "You must do so from a terminal and not from a Python interpreter.\n"
    )
    return {"cause": cause}


@add_statement_analyzer
def dot_followed_by_bracket(statement):
    if statement.bad_token.string in "()[]{}" and statement.prev_token == ".":
        cause = _("You cannot have a dot `.` followed by `{bracket}`.\n").format(
            bracket=statement.bad_token
        )
    else:
        return {}

    # Before we make any attempt at modifying the original code,
    # we make sure that our statement checker can properly identify that
    # the original code is invalid. See #205
    if fixers.check_statement(statement.bad_line):
        return {}

    new_statement = fixers.replace_token(
        statement.statement_tokens, statement.prev_token, ","
    )
    if fixers.check_statement(new_statement):
        cause += _("Perhaps you need to replace the dot by a comma.\n")

    return {"cause": cause}


@add_statement_analyzer
def raise_single_exception(statement):
    if statement.first_token != "raise":
        return {}

    if statement.bad_token == "," and statement.prev_token.is_identifier():
        cause = _(
            "It looks like you are trying to raise an exception using Python 2 syntax.\n"
        )
        return {"cause": cause}
    return {}


@add_statement_analyzer
def invalid_double_star_operator(statement):
    if statement.bad_token == "**":
        cause = _(
            "The double star operator `**` is likely interpreted to mean that\n"
            "dict unpacking is to be used which is not allowed or does not make sense here.\n"
        )
        return {"cause": cause}

    return {}


@add_statement_analyzer
def missing_colon(statement):
    """look for missing colon at the end of statement"""
    # TODO: check all keywords listed here, with single keyword missing colon, like:
    # if

    if statement.last_token == ":" or statement.bad_token != statement.last_token:
        return {}

    name = statement.first_token
    if name.string not in (
        "async",
        "class",
        "def",
        "if",
        "elif",
        "else",
        "for",
        "while",
        "try",
        "except",
        "finally",
        "with",
    ):
        return {}

    # Before we make any attempt at modifying the original code,
    # we make sure that our statement checker can properly identify that
    # the original code is invalid. See #205
    if fixers.check_statement(statement.bad_line):
        return {}

    new_statement = fixers.replace_token(
        statement.statement_tokens,
        statement.bad_token,
        statement.bad_token.string + ":",
    )
    if not fixers.check_statement(new_statement):
        return {}

    name = statement.first_token

    hint = _("Did you forget a colon `:`?\n")
    statement.location_markers = su.highlight_added_token(statement.bad_token, ":")

    if name.string in ("for", "while"):
        cause = _(
            "You wrote a `{for_while}` loop but\n"
            "forgot to add a colon `:` at the end\n"
            "\n"
        ).format(for_while=name)
        return {"cause": cause, "suggest": hint}

    cause = _(
        "You wrote a statement beginning with\n"
        "`{name}` but forgot to add a colon `:` at the end.\n"
        "\n"
    ).format(name=name)
    return {"cause": cause, "suggest": hint}


@add_statement_analyzer
def semi_colon_instead_of_comma(statement):
    """Writing a semicolon as a typo"""
    if statement.bad_token != ";":
        return {}

    # Before we make any attempt at modifying the original code,
    # we make sure that our statement checker can properly identify that
    # the original code is invalid. See #205
    if fixers.check_statement(statement.bad_line):
        return {}

    new_statement = fixers.replace_token(
        statement.statement_tokens, statement.bad_token, ","
    )
    if fixers.check_statement(new_statement):
        cause = _("You wrote a semicolon, `;`, where a comma was expected.\n")
        hint = _("Did you mean to write a comma?\n")
        return {"cause": cause, "suggest": hint}

    # perhaps used multiple semicolons instead of comma
    if statement.last_token == ";":
        new_statement = fixers.replace_token(
            statement.statement_tokens, statement.last_token, ""
        )
    else:
        new_statement = statement.entire_statement
    while True:
        tokens = token_utils.tokenize(new_statement)
        for tok in tokens:
            if tok == ";":
                break
        else:
            break
        new_statement = fixers.replace_token(tokens, tok, ",")
    if fixers.check_statement(new_statement):
        cause = _("You wrote semicolons, `;`, where commas were expected.\n")
        hint = _("Did you mean to write commas?\n")
        return {"cause": cause, "suggest": hint}

    return {}  # pragma: no cover


@add_statement_analyzer
def semi_colon_instead_of_colon(statement):
    """Writing a semicolon as a typo"""
    if statement.bad_token != ";":
        return {}
    # Before we make any attempt at modifying the original code,
    # we make sure that our statement checker can properly identify that
    # the original code is invalid. See #205
    if fixers.check_statement(statement.bad_line):
        return {}
    new_statement = fixers.replace_token(
        statement.statement_tokens, statement.bad_token, ":"
    )
    if fixers.check_statement(new_statement):
        cause = _("You wrote a semicolon, `;`, where a colon was expected.\n")
        hint = _("Did you mean to write a colon?\n")
        return {"cause": cause, "suggest": hint}

    return {}  # pragma: no cover


@add_statement_analyzer
def invalid_hexadecimal(statement):
    """Identifies problem caused by invalid character in an hexadecimal number."""
    if statement.highlighted_tokens:  # Python 3.10
        prev = statement.bad_token
        wrong = statement.next_token
    else:
        prev = statement.prev_token
        wrong = statement.bad_token
    if not (prev.immediately_before(wrong) and prev.string.lower().startswith("0x")):
        return {}

    hint = _("Did you made a mistake in writing an hexadecimal integer?\n")
    cause = _(
        "It looks like you used an invalid character (`{character}`) in an hexadecimal number.\n\n"
        "Hexadecimal numbers are base 16 integers that use the symbols `0` to `9`\n"
        "to represent values 0 to 9, and the letters `a` to `f` (or `A` to `F`)\n"
        "to represent values 10 to 15.\n"
        "In Python, hexadecimal numbers start with either `0x` or `0X`,\n"
        "followed by the characters used to represent the value of that integer.\n"
    ).format(character=wrong.string[0])
    return {"cause": cause, "suggest": hint}


@add_statement_analyzer
def invalid_octal(statement):
    """Identifies problem caused by invalid character in an octal number."""
    prev = statement.prev_token
    wrong = statement.bad_token
    if not (prev.immediately_before(wrong) and prev.string.lower().startswith("0o")):
        return {}

    hint = _("Did you made a mistake in writing an octal integer?\n")
    cause = _(
        "It looks like you used an invalid character (`{character}`) in an octal number.\n\n"
        "Octal numbers are base 8 integers that only use the symbols `0` to `7`\n"
        "to represent values.\n"
        "In Python, octal numbers start with either `0o` or `0O`,\n"
        "(the digit zero followed by the letter `o`)\n"
        "followed by the characters used to represent the value of that integer.\n"
    ).format(character=wrong.string[0])
    return {"cause": cause, "suggest": hint}


@add_statement_analyzer
def invalid_name(statement):
    """Identifies invalid identifiers when a name begins with a number"""
    first = statement.prev_token
    second = statement.bad_token
    # New in Python 3.10
    if (
        statement.highlighted_tokens is not None
        and len(statement.highlighted_tokens) > 1
    ):
        first = statement.highlighted_tokens[0]
        second = statement.highlighted_tokens[1]

    if not (first.is_number() and second.is_name() and first.end == second.start):
        return {}

    cause = _("Valid names cannot begin with a number.\n")
    if first == statement.first_token:  # statement begins with this invalid identifier
        for token in statement.tokens:
            if token == "=":  # Trying to assign a value to an invalid name
                return {"cause": cause, "suggest": cause}

    if second == "i" and not first.is_complex():
        hint = _("Did you mean `{number}j`?\n").format(number=first)
        cause = _(
            "Perhaps you thought that `i` could be used to represent\n"
            "the square root of `-1`. In Python, the symbol used for this is `j`\n"
            "and the complex part is written as `some_number` immediately\n"
            "followed by `j`, with no spaces in between.\n"
            "Perhaps you meant to write `{number}j`.\n"
        ).format(number=first)
        return {"cause": cause, "suggest": hint}

    if second.string in ["e", "E"] and not first.is_complex():
        hint = _("Did you mean `{number}{second}0`?\n").format(
            number=first, second=second
        )
        cause = _(
            "Perhaps you meant to write `{number}{second}0` in scientific notation\n"
            "and forgot the numerical value for the exponent.\n"
        ).format(number=first, second=second)
        return {"cause": hint + cause, "suggest": hint}

    if first.is_complex():
        note = _(
            "[Note: `{first} * {second}` would also be valid\n"
            "since `{first}` is a complex number.]\n"
        ).format(first=first, second=second)
        # Do not modify the token themselves; reuse names and create pure strings
        # otherwise the location shown by where() will be incorrect.
        second = first.string[-1] + second.string
        first = first.string[:-1]
    else:
        note = ""

    hint = _(
        "Perhaps you forgot a multiplication operator, `{first} * {second}`.\n"
    ).format(first=first, second=second)

    return {"cause": cause + hint + "\n" + note, "suggest": hint}


@add_statement_analyzer
def debug_fstring(statement):
    """Detect debug feature of f-string introduced in Python 3.8"""
    if sys.version_info >= (3, 8) or not statement.fstring_error:
        return {}

    if statement.bad_token == "=" and statement.prev_token.is_identifier():
        if statement.next_token == ")":
            hint = _("Your Python version does not support this f-string feature.\n")
            cause = _(
                "You are likely using a 'debug' syntax of f-strings introduced\n"
                "in Python version 3.8. You are using version {version}.\n"
            ).format(version=f"{sys.version_info.major}.{sys.version_info.minor}")
            return {"cause": cause, "suggest": hint}

        cause = _(
            "You are likely trying to assign a value within an f-string.\n"
            "This is not allowed.\n"
        )
        return {"cause": cause}

    return {}  # pragma: no cover


@add_statement_analyzer
def general_fstring_problem(statement):  # pragma: no cover
    # General f-string problems are outside of our main priorities.
    if not statement.fstring_error:
        return {}

    cause = _(
        "The content of your f-string is invalid. Please consult the documentation:\n"
        "https://docs.python.org/3/reference/lexical_analysis.html#f-strings\n"
    )
    return {"cause": cause}


@add_statement_analyzer
def assign_to_a_keyword(statement):
    """Checks to see if line is of the form 'keyword = ...'"""
    hint = _("Python keywords cannot be used as identifiers (variable names).\n")
    possible_cause = _(
        "You were trying to assign a value to the Python keyword `{keyword}`.\n"
        "This is not allowed.\n"
        "\n"
    )
    if statement.bad_token == "=" and statement.prev_token.is_keyword():
        cause = possible_cause.format(keyword=statement.prev_token)
        bad_token = statement.prev_token
    elif statement.bad_token.is_keyword() and statement.next_token == "=":
        bad_token = statement.bad_token
        cause = possible_cause.format(keyword=statement.bad_token)
    else:
        return {}
    statement.location_markers = su.highlight_single_token(bad_token)
    return {"cause": cause, "suggest": hint}


@add_statement_analyzer
def lambda_with_paren(statement):
    if statement.bad_token != "(":
        return {}

    if statement.prev_token == "lambda":
        cause = _(
            "`lambda` does not allow parentheses around its arguments.\n"
            "This was allowed in Python 2 but it not allowed in Python 3.\n"
        )
        return {"cause": cause}

    tokens = list(statement.tokens[: statement.bad_token_index])
    tokens.reverse()
    for tok in tokens:
        if tok == "lambda":
            break

        if tok.is_identifier() or tok == ",":
            continue

        return {}  # pragma: no cover

    cause = _(
        "You cannot have explicit tuples as arguments.\n"
        "Assign any tuple to a parameter and unpack it\n"
        "within the body of the function.\n"
    )
    return {"cause": cause}


@add_statement_analyzer
def wrong_type_declaration(statement):
    if statement.highlighted_tokens and len(statement.highlighted_tokens) > 1:
        bad_token = statement.next_token
        prev_token = statement.bad_token
    else:
        bad_token = statement.bad_token
        prev_token = statement.prev_token

    if not bad_token.is_identifier():
        return {}
    if prev_token.string not in (
        "int",
        "float",
        "double",
        "var",
        "let",
        "str",
        "string",
        "complex",
    ):
        return {}
    # Before we make any attempt at modifying the original code,
    # we make sure that our statement checker can properly identify that
    # the original code is invalid. See #205
    if fixers.check_statement(statement.bad_line):
        return {}

    new_statement = fixers.replace_token(statement.statement_tokens, prev_token, "")
    if fixers.check_statement(new_statement):
        additional = _(
            "If you remove `{type_decl}`, you will have a valid Python statement.\n"
        )
    else:
        additional = _(
            "However, even if you remove `{type_decl}`, there would still be some\n"
            "some syntax errors.\n"
        )

    hint = _("You do not need to declare variables in Python.\n")
    cause = _(
        "It looks like you were trying to declare that `{var}` was\n"
        "a variable using the word `{type_decl}`.\n"
    ).format(var=statement.bad_token, type_decl=prev_token) + additional.format(
        type_decl=prev_token
    )
    return {"cause": cause, "suggest": hint}


@add_statement_analyzer
def missing_comma_before_string_in_dict(statement):
    """Special case where keys and values in a dict are strings which are
    not separated by commas."""

    # This is a bit of an unusual case as the error occurred due to
    # a forgotten comma two tokens before the token flagged by Python.
    if not (
        statement.begin_brackets
        and statement.begin_brackets[-1] == "{"
        and statement.bad_token == ":"
        and statement.prev_token.is_string()
        and statement.tokens[statement.bad_token_index - 1].is_string()
    ):
        return {}
    # Before we make any attempt at modifying the original code,
    # we make sure that our statement checker can properly identify that
    # the original code is invalid. See #205
    if fixers.check_statement(statement.bad_line):
        return {}
    before_prev = statement.tokens[statement.bad_token_index - 2]

    new_statement = fixers.replace_token(
        statement.statement_tokens, before_prev, before_prev.string + ","
    )
    if not fixers.check_statement(new_statement):
        return {}

    cause = _(
        "I am guessing that you forgot a comma between two strings\n"
        "when defining a dict.\n\n"
    ).format(kwd=statement.bad_token)
    mark = su.highlight_added_token(before_prev, ",")

    new_statement = fixers.replace_token(
        statement.statement_tokens, before_prev, before_prev.string + ","
    )
    new_statement = su.add_mark_to_new_statement(
        statement, new_statement, mark[before_prev.start_row]
    )
    cause += "```\n" + new_statement + "\n```"
    hint = _("Did you forget a comma?\n")

    return {"cause": cause, "suggest": hint}


@add_statement_analyzer
def missing_in_with_for(statement):
    """Whenever we have a 'for' keyword, there should be a corresponding
    'in' keyword. Cases where 'in' have been misspelled are taken care below.
    Note that 'in' could be used with 'if' and 'while' as well, but here
    we only consider the simplest cases.
    """
    index = statement.bad_token_index
    bad_token = statement.bad_token
    # Python 3.10 may highlight two tokens
    if statement.highlighted_tokens and len(statement.highlighted_tokens) > 1:
        index += 1
        bad_token = statement.next_token

    nb_for = nb_in = 0
    for tok in statement.tokens[:index]:
        if tok == "for":
            nb_for += 1
        elif tok == "in":
            nb_in += 1
    if nb_for == 0 or nb_in >= nb_for:
        return {}

    # Before we make any attempt at modifying the original code,
    # we make sure that our statement checker can properly identify that
    # the original code is invalid. See #205
    if fixers.check_statement(statement.bad_line):
        return {}

    new_statement = fixers.replace_token(
        statement.statement_tokens, bad_token, f"in {bad_token.string}"
    )

    if fixers.check_statement(new_statement):
        hint = _("Did you forget to write `in`?\n")
        cause = _(
            "It looks as though you forgot to use the keyword `in`\n"
            "as part of a `for` statement. Perhaps you meant:\n\n"
            "    {new_statement}\n\n"
        ).format(new_statement=new_statement)
        return {"cause": cause, "suggest": hint}
    return {}


@add_statement_analyzer
def missing_parens_for_range(statement):
    if statement.prev_token != "range" or statement.last_token != ":":
        return {}

    # Before we make any attempt at modifying the original code,
    # we make sure that our statement checker can properly identify that
    # the original code is invalid. See #205
    if fixers.check_statement(statement.bad_line):
        return {}

    new_statement = fixers.replace_two_tokens(
        statement.tokens,
        statement.prev_token,
        statement.prev_token.string + "(",
        statement.last_token,
        ")" + statement.last_token.string,
    )
    if fixers.check_statement(new_statement):
        hint = _("Did you forget to write parenthesis?\n")
        cause = _(
            "It looks as though you forgot to use to use parenthesis with `range`.\n"
            "Perhaps you meant:\n\n"
            "    {new_statement}\n\n"
        ).format(new_statement=new_statement)
        return {"cause": cause, "suggest": hint}
    return {}


def _perhaps_misspelled_keyword(tokens, wrong):
    kwlist = list(keyword.kwlist)
    if wrong in kwlist:
        kwlist.remove(wrong)
    similar = utils.get_similar_words(wrong.string, kwlist)
    if not similar:
        return []

    results = []
    for word in similar:
        new_statement = fixers.replace_token(tokens, wrong, word)
        if fixers.check_statement(new_statement):
            results.append((word, new_statement))
    return results


def misspelled_python_keyword(tokens, bad_token):
    results = _perhaps_misspelled_keyword(tokens, bad_token)
    if not results:
        return {}

    word, line = results[0]
    hint = _("Did you mean `{line}`?\n").format(line=line)
    cause = _(
        "Perhaps you meant to write `{keyword}` and made a typo.\n"
        "The correct line might be `{line}`\n"
    ).format(keyword=word, line=line)

    return {"cause": cause, "suggest": hint}


@add_statement_analyzer
def comprehension_condition_or_tuple(statement):
    if not statement.begin_brackets:
        return {}

    cause_condition = _(
        "I am guessing that you were writing a comprehension or a generator expression\n"
        "and use the wrong order for a condition.\n"
        "The correct order depends if there is an `else` clause or not.\n"
        "For example, the correct order for a list comprehensions with\n"
        "condition can be either\n\n"
        "    [f(x) if condition else other for x in sequence]  # 'if' before 'for'\n\n"
        "or, if there is no `else`\n\n"
        "    [f(x) for x in sequence if condition]  # 'if' after 'for'\n\n"
    )

    cause_tuple = _(
        "I am guessing that you were writing a comprehension or a generator expression\n"
        "and forgot to include parentheses around tuples.\n"
        "As an example, instead of writing\n\n"
        "    [i, i**2 for i in range(10)]\n\n"
        "you would need to write\n\n"
        "    [(i, i**2) for i in range(10)]\n\n"
    )

    if statement.bad_token == "else":
        for tok in statement.tokens[: statement.bad_token_index]:
            if tok == "for":
                cause = cause_condition
                break
        else:
            return {}
    elif statement.bad_token == "for":
        for tok in statement.tokens[0 : statement.bad_token_index]:
            if tok == "if":
                cause = cause_condition
                break
        else:
            found_bracket = False
            for tok in statement.tokens[0 : statement.bad_token_index]:
                if tok.string in "([{":
                    found_bracket = True
                if tok == "," and found_bracket:
                    cause = cause_tuple
                    hint = _("Did you forget parentheses?\n")
                    return {"cause": cause, "suggest": hint}
            return {}
    else:
        return {}

    return {"cause": cause}


@add_statement_analyzer
def parens_around_exceptions(statement):
    # keep in sync with message_analyzer.parens_around_exceptions
    if statement.bad_token != "," or statement.first_token != "except":
        return {}

    for tok in statement.tokens[1 : statement.bad_token_index]:
        if not tok.is_identifier() and tok != ",":
            return {}

    hint = _("Did you forget parentheses?\n")
    cause = _(
        "I am guessing that you wanted to use an `except` statement\n"
        "with multiple exception types. If that is the case, you must\n"
        "surround them with parentheses.\n"
    )
    return {"cause": cause, "suggest": hint}


@add_statement_analyzer
def current_is_misspelled_python_keyword(statement):
    if not statement.bad_token.is_name():
        return {}
    # Before we make any attempt at modifying the original code,
    # we make sure that our statement checker can properly identify that
    # the original code is invalid. See #205
    if fixers.check_statement(statement.bad_line):
        return {}
    return misspelled_python_keyword(statement.tokens, statement.bad_token)


@add_statement_analyzer
def previous_is_misspelled_python_keyword(statement):
    if not statement.prev_token.is_name():
        return {}
    # Before we make any attempt at modifying the original code,
    # we make sure that our statement checker can properly identify that
    # the original code is invalid. See #205
    if fixers.check_statement(statement.bad_line):
        return {}
    return misspelled_python_keyword(statement.tokens, statement.prev_token)


@add_statement_analyzer
def space_in_variable_name(statement):
    # Looking for spaces in variable name assignments, like
    # my name = André
    bad_token = statement.bad_token
    prev_token = statement.prev_token
    if statement.highlighted_tokens and len(statement.highlighted_tokens) == 2:
        bad_token = statement.next_token
        prev_token = statement.bad_token

    if not (
        bad_token.is_identifier()
        and prev_token.is_identifier()
        and prev_token is statement.first_token
    ):
        return {}

    first_tokens = []
    for tok in statement.tokens:
        if tok == "=":
            # Note: there could be other errors
            cause = _(
                "You cannot have spaces in identifiers (variable names).\n"
                "Perhaps you meant `{name}`?\n"
            ).format(name="_".join(first_tokens))
            hint = _("Did you mean `{name}`?\n").format(name="_".join(first_tokens))
            return {"cause": cause, "suggest": hint}

        if not tok.is_identifier():
            return {}

        first_tokens.append(tok.string)

    return {}


@add_statement_analyzer
def impossible_binary_fstring(statement):
    if (
        statement.bad_token.is_string()
        and statement.prev_token.string in ("bf", "fb")
        and statement.prev_token.immediately_before(statement.bad_token)
    ):
        hint = _("`bf` is an illegal string prefix.\n")
        cause = _(
            "I am guessing that you wanted a binary f-string;\n"
            "this is not allowed.\n"
        )
        return {"cause": cause, "suggest": hint}


def _add_comma_or_operator(tokens, tok, comma_first=True):
    if comma_first:
        operators = ", ", " + ", " - ", " * ", " in "
    else:
        operators = " + ", " - ", " * ", ", ", " in "
    results = []
    for operator in operators:
        if operator == " in " and results:
            break
        new_statement = fixers.replace_token(tokens, tok, tok.string + operator)
        if fixers.check_statement(new_statement):
            results.append((operator.strip(), new_statement))
    return results


def _comma_first_cause(bracket):
    if bracket == "(":
        return _(
            "It is possible that you "
            "forgot a comma between items in a tuple, \n"
            "or between function arguments, \n"
            "at the position indicated by ^.\n"
        )

    if bracket == "[":
        return _(
            "It is possible that you "
            "forgot a comma between items in a list\n"
            "at the position indicated by ^.\n"
        )

    return _(
        "It is possible that you "
        "forgot a comma between items in a set or dict\n"
        "at the position indicated by ^.\n"
    )


@add_statement_analyzer
def missing_comma_or_operator(statement):
    """Check to see if a comma or other operator
    is possibly missing between identifiers, or numbers, or both.
    """
    bad_token = statement.bad_token
    prev_token = statement.prev_token
    if statement.highlighted_tokens:  # Python 3.10 may highlight two tokens
        bad_token = statement.next_token
        prev_token = statement.bad_token
    if not (
        bad_token.is_identifier() or bad_token.is_number() or bad_token.is_string()
    ) and not (
        prev_token.is_identifier() or prev_token.is_number() or prev_token.is_string()
    ):
        return {}

    # Before we make any attempt at modifying the original code,
    # we make sure that our statement checker can properly identify that
    # the original code is invalid. See #205
    if fixers.check_statement(statement.bad_line):
        return {}

    possible_cause = _(
        "Python indicates that the error is caused by "
        "`{second}` written immediately after `{first}`.\n"
    ).format(first=prev_token, second=bad_token)

    if statement.begin_brackets:
        # likely inside a list, tuple, function def, dict, ...
        # in which case the most likely cause is a missing comma
        comma_first = True
        bracket = statement.begin_brackets[-1]
        comma_first_cause = _comma_first_cause(bracket)
    else:
        comma_first = False
        comma_first_cause = ""

    new_statements = _add_comma_or_operator(
        statement.statement_tokens, prev_token, comma_first=comma_first
    )
    if not new_statements:
        return {}

    if prev_token.start_row == bad_token.start_row:
        statement.location_markers = su.highlight_two_tokens(
            prev_token, bad_token, between="^"
        )
    else:
        statement.location_markers = su.highlight_two_tokens(
            prev_token, bad_token, first_marker="^", between="-->"
        )

    # TODO: fix the cases with def/async/class
    if len(new_statements) == 1 or statement.first_token.string in [
        "def",
        "async",
        "class",
    ]:
        operator, line = new_statements[0]
        if "\n" in line:
            mark = su.highlight_added_token(prev_token, "^")
            line = su.add_mark_to_new_statement(
                statement, line, mark[prev_token.start_row]
            )
            # lines = line.split("\n")
            # lines = ["    " + line_ for line_ in lines]
            # line = "    \n".join(lines)
        else:
            # reducing multiple spaces on single line to single space for nicer display
            temp = line.split(" ")
            temp = [x for x in temp if x]
            line = " ".join(temp)
            mark = su.highlight_added_token(prev_token, "^")
            line = su.add_mark_to_new_statement(
                statement, line, mark[prev_token.start_row]
            )
        if "," in operator:
            hint = _("Did you forget a comma?\n")
            cause = possible_cause + comma_first_cause
            cause += _("Perhaps you meant{line}").format(line=utils.to_code_block(line))
        else:
            hint = _("Did you mean `{line}`?\n").format(line=line)
            cause = possible_cause
    else:
        operators = [operator for operator, line in new_statements]
        lines = [line for operator, line in new_statements]
        hint = _("Did you forget something between `{first}` and `{second}`?\n").format(
            first=prev_token, second=bad_token
        )

        # The list of operators might include a comma; it is better to separate
        # items by semicolons
        if comma_first:
            operators = operators[1:]
            operators = utils.list_to_string(operators)
        else:
            operators = utils.list_to_string(operators, sep="; ")

        cause = (
            possible_cause
            + comma_first_cause
            + _(
                "Perhaps you meant to insert an operator like `{operators}`\n"
                "between `{first}` and `{second}`.\n"
                "The following lines of code would not cause any `SyntaxError`:\n\n"
            ).format(first=prev_token, second=bad_token, operators=operators)
        )
        for line in lines:
            cause += f"    {line}\n"

        cause += _(
            "Note: these are just some of the possible choices and that\n"
            "some of them might raise other types of exceptions.\n"
        )

        possible_cause = bracket_instead_of_paren(statement)
        if possible_cause:
            cause += "\n" + _("There is an additional possibility.\n")
            cause += possible_cause["cause"]

    return {"cause": cause, "suggest": hint}


@add_statement_analyzer
def equal_instead_of_colon_in_dict(statement):
    if not (
        statement.begin_brackets
        and statement.bad_token == "="
        and statement.begin_brackets[-1] == "{"
    ):
        return {}

    cause = _(
        "It is possible that "
        "you used an equal sign `=` instead of a colon `:`\n"
        "to assign values to keys in a dict\n"
        "before or at the position indicated by ^.\n"
    )
    return {"cause": cause}


@add_statement_analyzer
def boolean_instead_of_comma(statement):
    # Example: from math import sin and cos
    # Includes cases where boolean added after comma
    if statement.bad_token.string not in ["and", "or"]:
        return {}
    # Before we make any attempt at modifying the original code,
    # we make sure that our statement checker can properly identify that
    # the original code is invalid. See #205
    if fixers.check_statement(statement.bad_line):
        return {}

    bad_token = statement.bad_token

    possible_cause = _(
        "The Python keyword `{boolean}` can only be used for boolean expressions.\n"
        "Perhaps you meant to write\n\n"
        "`{new_statement}`\n"
    )

    cause = None
    new_statement = fixers.replace_token(statement.statement_tokens, bad_token, ",")
    if fixers.check_statement(new_statement):
        cause = possible_cause.format(new_statement=new_statement, boolean=bad_token)
    else:  # 'and' following a comma
        new_statement = fixers.replace_token(statement.statement_tokens, bad_token, "")
        if fixers.check_statement(new_statement):
            cause = possible_cause.format(
                new_statement=new_statement, boolean=bad_token
            )

    return {"cause": cause} if cause else {}


@add_statement_analyzer
def from_import_as(statement):
    """from module import ... as ..., with 'as' flagged as the bad token"""
    if not (
        statement.bad_token == "as"
        and statement.first_token == "from"
        and statement.tokens[2] == "import"
    ):
        return {}

    cause = _(
        "I am guessing that you are trying to import at least one object\n"
        "from module `{module}` and rename it using the Python keyword `as`;\n"
        "this keyword can only be used to rename one object at a time\n"
        "using a well defined syntax.\n"
        "I suggest that you split up any such import statement with each object\n"
        "renamed on a separate line as follows:\n\n"
        "    from {module} import object_1 as name_1\n"
        "    from {module} import object_2 as name_2  # if needed\n"
    ).format(module=statement.tokens[1])
    return {"cause": cause}


@add_statement_analyzer
def delete_names_or_items(statement):
    if statement.first_token != "del":
        return {}

    cause = _(
        "You can only delete names of objects, or items in mutable containers\n"
        "such as `list`, `set`, or `dict`.\n"
    )
    return {"cause": cause}


@add_statement_analyzer
def duplicate_token(statement):
    if statement.bad_token != statement.prev_token:
        return {}
    bad_token = "`{bad_token}`".format(bad_token=statement.bad_token)
    cause = _(
        "I am guessing that you wrote {bad_token} twice in a row by mistake.\n"
        "If that is the case, you need to remove the second one.\n"
    ).format(bad_token=bad_token)
    hint = _("Did you write {bad_token} twice by mistake?\n").format(
        bad_token=bad_token
    )
    new_statement = fixers.replace_token(
        statement.statement_tokens, statement.bad_token, ""
    )
    # issue 205: check to see if original statement is found to be faulty.
    if fixers.check_statement(new_statement) and not fixers.check_statement(
        statement.bad_line
    ):
        return {"cause": cause, "suggest": hint}
    return {"cause": cause + more_errors(), "suggest": hint}


@add_statement_analyzer
def extra_token(statement):
    # Before we make any attempt at modifying the original code,
    # we make sure that our statement checker can properly identify that
    # the original code is invalid. See #205
    if fixers.check_statement(statement.bad_line):
        return {}
    new_statement = fixers.replace_token(
        statement.statement_tokens, statement.bad_token, ""
    )

    if fixers.check_statement(new_statement):
        bad_token = "`{bad_token}`".format(bad_token=statement.bad_token)
        cause = _(
            "I am guessing that you wrote {bad_token} by mistake.\n"
            "Removing it and writing `{line}` seems to fix the error.\n"
        ).format(bad_token=bad_token, line=new_statement)
        hint = _("Did you write {bad_token} by mistake?\n").format(bad_token=bad_token)
        return {"cause": cause, "suggest": hint}
    return {}


@add_statement_analyzer
def missing_value_in_dict(statement):
    if not _possibly_inside_dict(statement):
        return {}
    if statement.bad_token.string not in [",", "}"]:
        return {}
    if statement.prev_token == ":":
        cause = _(
            "It looks like the error occurred as you were writing a Python dict.\n"
            "Perhaps you forgot to write a value after a colon.\n"
        )
    else:
        cause = _(
            "It looks like the error occurred as you were writing a Python dict.\n"
            "Perhaps wrote a dict key without writing the corresponding value.\n"
        )
    hint = _("Did you forget to write a dict value?\n")
    return {"cause": cause, "suggest": hint}


@add_statement_analyzer
def else_with_no_match(statement):
    if not (
        statement.bad_token == statement.first_token == "else"
        and statement.next_token == statement.last_token == ":"
    ):
        return {}

    cause = _(
        "The `else` keyword does not begin a code block that matches\n"
        "a valid code block, possibly because `else` is not indented correctly.\n"
    )
    return {"cause": cause}


@add_statement_analyzer
def elif_with_no_matching_if(statement):
    if not (statement.bad_token == statement.first_token == "elif"):
        return {}
    if fixers.check_statement(statement.bad_line):
        cause = _(
            "The `elif` keyword does not begin a code block that matches\n"
            "an `if` block, possibly because `elif` is not indented correctly.\n"
        )
        return {"cause": cause}
    return {}


@add_statement_analyzer
def except_with_no_matching_try(statement):
    if not (statement.bad_token == statement.first_token == "except"):
        return {}
    if fixers.check_statement(statement.bad_line):
        cause = _(
            "The `except` keyword does not begin a code block that matches\n"
            "a `try` block, possibly because `except` is not indented correctly.\n"
        )
        return {"cause": cause}
    return {}


@add_statement_analyzer
def finally_with_no_matching_try(statement):
    if not (statement.bad_token == statement.first_token == "finally"):
        return {}
    if fixers.check_statement(statement.bad_line):
        cause = _(
            "The `finally` keyword does not begin a code block that matches\n"
            "a `try` block, possibly because `finally` is not indented correctly.\n"
        )
        return {"cause": cause}
    return {}


@add_statement_analyzer
def bracket_instead_of_paren(statement):
    if statement.statement_brackets:
        return {}

    matching_pairs = []
    square_brackets = []
    for tok in statement.tokens:
        if tok == "[":
            square_brackets.append(tok)
        elif tok == "]":
            open_bracket = square_brackets.pop()
            matching_pairs.append((open_bracket, tok))
    if not matching_pairs:
        return {}

    # Before we make any attempt at modifying the original code,
    # we make sure that our statement checker can properly identify that
    # the original code is invalid. See #205
    if fixers.check_statement(statement.bad_line):
        return {}

    for first, second in matching_pairs:
        new_statement = fixers.replace_two_tokens(
            statement.statement_tokens,
            first,
            first_string="(",
            second_token=second,
            second_string=")",
        )
        if fixers.check_statement(new_statement):
            hint = _("You used square brackets, `[...]` instead of parentheses.\n")
            lines = new_statement.split("\n")
            new_lines = [f"    {line}" for line in lines]
            new_statement = "\n".join(new_lines)
            cause = hint + _("Write the following instead:\n\n{new_statement}").format(
                new_statement=new_statement
            )
            return {"cause": cause, "suggest": hint}
    return {}


# Last resort as it can catch odd cases where an unmatched open
# bracket on one statement matches closing bracket on following
# statement. Typically, the flagged token will be the first token
# on a line, which Python detects as starting a new statement,
# or the last token on the line.
# The method I use to identify a statement can get matching
# brackets from what is another Python statement.
@add_statement_analyzer
def unclosed_bracket(statement):
    if not statement.begin_brackets:
        return {}

    bracket = statement.begin_brackets[-1]
    # not statement_brackets -> all brackets are closed
    # bad_token match open bracket: problem is not with unclosed bracket
    if not statement.statement_brackets and su.matching_brackets(
        bracket, statement.bad_token
    ):
        return {}
    # No unmatched brackets and Python did not identify a bad token as
    # either ending a statement or beginning a new statement
    if (
        not statement.statement_brackets
        and statement.bad_token.start_row == statement.prev_token.start_row
        and statement.bad_token.start_row == statement.next_token.start_row
    ):
        return {}

    linenumber = bracket.start_row
    start_col = bracket.start_col

    bracket_name = su.name_bracket(bracket)
    source = f"\n    {linenumber}: {statement.source_lines[linenumber - 1]}"
    shift = len(str(linenumber)) + start_col + 6
    source += " " * shift + "^\n"

    cause = (
        _("The opening {bracket} on line {linenumber} is not closed.\n").format(
            bracket=bracket_name, linenumber=linenumber
        )
        + source
    )
    if statement.statement_brackets:  # no closing bracket
        return {"cause": cause}

    # assume that the code is properly indented. If we go back to the same
    # level of indentation (or less) than the original statement, then
    # we definitely have an unclosed bracket
    first_column = statement.first_token.start_col
    for tok in statement.tokens[1:-1]:
        if tok.start_col <= first_column:
            cause += "\n" + _("If this is incorrect, please report this case.\n")
            return {"cause": cause}

    # If the line flagged is not a valid statement, then we likely have other
    # problems.
    if not fixers.check_statement(statement.bad_line):
        return {}

    tokens = token_utils.tokenize(statement.bad_line.strip())
    tokens = token_utils.remove_meaningless_tokens(tokens)
    if tokens[0].string in ["for", "if"] and tokens[-1] == ":":
        if bracket == "(":
            cause = _(
                "Perhaps you wrote a statement beginning a code block\n"
                "intended to be part of a generator expression.\n"
                "You cannot have separate code blocks inside generator expressions.\n"
            )
        elif bracket == "[":
            cause = _(
                "Perhaps you wrote a statement beginning a code block\n"
                "intended to be part of a list comprehension.\n"
                "You cannot have separate code blocks inside list comprehensions.\n"
            )
        else:
            cause = _(
                "Perhaps you wrote a statement beginning a code block\n"
                "intended to be part of a dict or set comprehension.\n"
                "You cannot have separate code blocks inside dict or set comprehensions.\n"
            )

    cause += "\n" + _("If this explanation is incorrect, please report this case.\n")
    return {"cause": cause}
