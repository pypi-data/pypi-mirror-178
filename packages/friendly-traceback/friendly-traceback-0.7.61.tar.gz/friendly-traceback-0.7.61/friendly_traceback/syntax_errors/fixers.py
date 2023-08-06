# type: ignore
"""Various functions used to find fixes to SyntaxErrors"""

import warnings

from .. import debug_helper, token_utils


def replace_token(tokens, original_token, new_token_string=" "):
    """Replaces a single token string to produce a new source.
    More specifically, given::

        * tokens: a list of tokens
        * original_token: single token to be replaced
        * replace: new string to replace original_token.string

    It creates a new list of tokens with the replacement having been done,
    untokenize it to produce a modified source which is stripped of
    leading and ending spaces so that it could be inserted in a
    code sample at the beginning of a line with no indentation.
    """
    if not tokens:  # pragma: no cover
        debug_helper.log("Problem in fixers.replace_token().")
        debug_helper.log("Empty token list was received")
        debug_helper.log_error()
        return "?"

    # In some instances, the token immediately before or immediately after the
    # bad token will be set as a meaningless space token. It would not make sense
    # to modify this token, and we thus return an invalid statement.
    if not original_token.string.strip():  # When prev or next token is
        return "?"

    try:
        new_tokens = []
        for tok in tokens:
            if tok is original_token:
                new_token = original_token.copy()
                new_token.string = new_token_string
                new_tokens.append(new_token)
            else:
                new_tokens.append(tok)
        source = token_utils.untokenize(new_tokens)
        return source.strip()
    except Exception as e:  # pragma: no cover
        debug_helper.log("Problem in fixers._modify_source().")
        debug_helper.log_error(e)
        return token_utils.untokenize(tokens)


def replace_two_tokens(
    tokens, first_token, first_string="", second_token=None, second_string=""
):
    """Replace two tokens at once by their new string value"""
    if second_token is None:  # pragma: no cover
        debug_helper.log("Problem in fixers.replace_two_tokens()")
        debug_helper.log("second_token should not be None")
        return token_utils.untokenize(tokens)
    try:
        new_tokens = []
        for tok in tokens:
            if tok is first_token:
                new_token = first_token.copy()
                new_token.string = first_string
                new_tokens.append(new_token)
            elif tok is second_token:
                new_token = second_token.copy()
                new_token.string = second_string
                new_tokens.append(new_token)
            else:
                new_tokens.append(tok)

        source = token_utils.untokenize(new_tokens)
        return source.strip()
    except Exception as e:  # pragma: no cover
        debug_helper.log("Problem in fixers.replace_two_tokens().")
        debug_helper.log_error(e)
        return token_utils.untokenize(tokens)


def check_statement(statement):
    """Given a single line of code expected to be a valid 'statement',
    that is a line which could be part of a larger source of code and
    contains no unmatched brackets and would not end with the continuation
    character, it is potentially modified to include some required
    'environment' and compiled to see if it raises any SyntaxErrors.

    Returns True if no SyntaxError is raised, False otherwise.
    """
    if not statement:  # If an empty string has been the result of modifying the code.
        return False

    statement = token_utils.strip_comment(statement)
    try:
        # The statement might have been indented in the original Python file,
        # so we remove the indentation of that first line
        statement = statement.lstrip()
        if statement.rstrip().endswith(":"):
            statement += " pass"

        if statement.startswith("elif") or statement.startswith("else"):
            statement = if_block % statement
        elif statement.startswith("return") or statement.startswith("yield"):
            statement = def_block % statement
        elif statement.startswith("except") or statement.startswith("finally"):
            statement = try_block % statement

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            try:
                compile(statement, "fake-file", "exec")
                return True
            except SyntaxError:
                return False

    except Exception as e:  # pragma: no cover
        debug_helper.log("Problem in token_utils.check_statement().")
        debug_helper.log_error(e)
        return False


if_block = """
if True:
    pass
%s
"""

def_block = """
def test():
    %s
"""

try_block = """
try:
    pass
%s
"""
