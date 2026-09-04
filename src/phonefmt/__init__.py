"""phonefmt: find and normalize phone numbers in text, without a numbering-plan dependency."""

from .core import classify, extract_candidates, format_national, normalize
from .io import iter_lines, read_numbers
from .patterns import COUNTRY_FORMATS, COUNTRY_FORMATS_BY_KEY, CountryFormat

__version__ = "0.1.0"

__all__ = [
    "classify",
    "extract_candidates",
    "format_national",
    "normalize",
    "iter_lines",
    "read_numbers",
    "CountryFormat",
    "COUNTRY_FORMATS",
    "COUNTRY_FORMATS_BY_KEY",
]
