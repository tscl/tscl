"""
Preprocess tscl source before lexing.
"""
from preprocess import markdown


def preprocess(source) -> str:
    return markdown.preprocess(source)
