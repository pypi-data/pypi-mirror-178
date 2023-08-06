"""
This script sets up self-defined errors.
"""

import sys

from .log import logger


class ParsedNoneError(Exception):
    """Used when bs4 returned None whereas there's target content existing within the document"""

    def __init__(self, response_url):
        self.message = "The word isn't in the Cambridge Dictionary yet. See " + response_url 

    def __str__(self):
        return self.message


class NoResultError(Exception):
    """Used when bs4 returned None because Cambridge dict has no result"""

    def __init__(self):
        self.message = "No result found in Cambridge Dictionary"

    def __str__(self):
        return self.message


def call_on_error(error, url, attempt, op):
    attempt += 1
    logger.debug(f"{op} {url} {attempt} times")
    if attempt == 3:
        print(f"Maximum {op} reached: {error}")
        sys.exit()
    return attempt
