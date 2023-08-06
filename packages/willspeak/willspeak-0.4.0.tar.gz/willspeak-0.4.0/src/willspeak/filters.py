"""
This module contains filter functions that should filter out and/or manipulate the text it's processing.

There are 3 different types of filters.
    * Decider: Function that checks if given text should be processed or not. Returning None if not.
    * Filter: Simple function that takes a given text and filters out any unwanted text before returning it.
    * Processor: This function takes a given text and splits it up into more manageable parts. Faster when
                 dealing with larger chunks of text.
"""

# Standard lib
from .dataobjects import TextFilter
import functools
import re

# Third party
import nltk

text_filters: list[TextFilter] = []
regex_cache = {}


def prepare():
    """Initialize NLTK library."""
    nltk.download("punkt", quiet=True)


def process_text(text: str) -> str | None:
    """Run all filters & processors on given text string."""
    # Ignore any unwanted text patterns
    for func in filter(lambda x: x.is_decider and x.enabled, text_filters):
        if not (text := func(text)):
            return

    # If the length of text is greater than 500 characters
    # Then we should split the text up into smaller chunks
    if len(text) > 500:
        text = nltk.sent_tokenize(text)
    else:
        text = [text]

    filter_funcs = filter(lambda x: x.is_filter and x.enabled, text_filters)
    for text in text:
        for func in filter_funcs:
            text = func(text)
        yield text


def text_filter(func=None, filter_type="filter", **kwargs) -> TextFilter | functools.partial:
    """
    Function decorator to register a text filter.

    A text filter takes a string and strips out unwanted text patterns.
    """
    # When func is none then we have been called directly
    # So return the decorator again with any passed parameters
    if func is None:
        kwargs["filter_type"] = filter_type
        return functools.partial(text_filter, **kwargs)

    # noinspection PyTypeChecker
    kwargs["filter_type"] = filter_type
    wrapper = TextFilter(func, **kwargs)
    text_filters.append(wrapper)
    return wrapper


def text_decider(func=None, **kwargs) -> TextFilter | functools.partial:
    """
    Function decorator to register a decider filter.

    A text decider takes a string and decides if the text should be processed or not.
    It should return 'None' if text should not be processed, returning the given text otherwise.
    """
    return text_filter(func, filter_type="decider", **kwargs)


def re_cache(regex: str):
    """Takes regex string, compile it, and cache it for later use."""
    if regex in regex_cache:
        return regex_cache[regex]
    else:
        compiled = re.compile(regex)
        regex_cache[regex] = compiled
        return compiled


# Deciders
################################################################################

@text_decider(enabled=False)
def ignore_only_urls(text: str) -> str | None:
    """
    Ignore text that is just an url.
    """
    re_filter = re_cache(r"^(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])$")
    # Returns text only if match is not found
    if not re.match(re_filter, text):
        return text


# Filters
################################################################################

@text_filter
def filter_read_more_at(text: str) -> str:
    """
    Strip out any 'Read more at.' text that a lot
    of sites like to add when any text is copied.
    """
    re_filter = re_cache(r"([Rr]ead more\s*[at]*:*\s+http\S+|[Ss]ee more at:*\s+http\S+)")
    return re.sub(re_filter, "", text).strip()


@text_filter
def replace_urls(text: str) -> str:
    """
    Replace urls with the domain name instead.
    """
    def _replacement(string: re.Match) -> str:
        return string.group(2)

    re_filter = re_cache(r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])")
    return re.sub(re_filter, _replacement, text).strip()
