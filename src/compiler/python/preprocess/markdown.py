"""
Pre-process markdown with embedded tscl in fenced code blocks.
"""
import re


def preprocess(string) -> str:
    """
    Return the preprocessed string, or the original string if the preprocessed string is empty.
    """
    preprocessed = ranges_only(string, code_ranges(string))
    return preprocessed if preprocessed.strip() else string


def code_ranges(string: str) -> (int, int):
    """
    Return (begin, end) character index tuple for fenced tscl code blocks:

    ```tscl
    ; code here
    ```
    """
    for match in re.finditer(r'(?<=\n```tscl).*?(?=\n```)', string, flags=re.DOTALL):
        yield match.span()


def ranges_only(string, ranges) -> str:
    """
    Return an equal length string with only `ranges` containing non-whitespace characters.
    """
    # only whitespace
    clean_string = re.sub(r'[^\s]', ' ', string)
    # re-insert ranges
    for begin, end in ranges:
        clean_string = clean_string[:begin] + string[begin:end] + clean_string[end:]
    return clean_string
