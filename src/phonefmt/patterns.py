"""Definitions for the small set of phone number formats this library knows about.

This is intentionally not a copy of a real numbering-plan database (that needs
ongoing maintenance and isn't something to hand-roll). It's a short, explicit
list covering enough countries to be useful, meant to be extended in place.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CountryFormat:
    key: str  # short lookup key, e.g. "US"
    name: str
    calling_code: str  # digits only, no leading '+', e.g. "1"
    national_lengths: Tuple[int, ...]  # valid lengths of the number after the calling code
    trunk_prefix: str = ""  # digit(s) dropped from a locally-dialed number, e.g. "0"


# Ordered by calling code length isn't required here since none of these
# calling codes are a prefix of another, but classify() sorts defensively
# anyway in case that stops being true as more countries are added.
COUNTRY_FORMATS = (
    CountryFormat("US", "United States / Canada (NANP)", "1", (10,)),
    CountryFormat("GB", "United Kingdom", "44", (10,), trunk_prefix="0"),
    CountryFormat("DE", "Germany", "49", (10, 11), trunk_prefix="0"),
    CountryFormat("FR", "France", "33", (9,), trunk_prefix="0"),
    CountryFormat("AU", "Australia", "61", (9,), trunk_prefix="0"),
    CountryFormat("IN", "India", "91", (10,), trunk_prefix="0"),
)

COUNTRY_FORMATS_BY_KEY = {fmt.key: fmt for fmt in COUNTRY_FORMATS}
