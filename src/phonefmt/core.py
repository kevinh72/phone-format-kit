"""Extraction and normalization of phone numbers from free text."""

import re
from typing import List, Optional

from .patterns import COUNTRY_FORMATS, COUNTRY_FORMATS_BY_KEY, CountryFormat

# A candidate is a run of digits and typical phone punctuation (spaces,
# dashes, dots, parens) that's long enough to plausibly be a phone number
# and isn't glued to other word characters (so it doesn't match things like
# "invoice-2024-01158899" or part numbers).
_CANDIDATE_RE = re.compile(r"(?<!\w)(\+?\d[\d\s().\-]{5,17}\d)(?!\w)")

_NON_DIGITS_RE = re.compile(r"\D")


def extract_candidates(text: str) -> List[str]:
    """Return substrings of `text` that look like phone numbers, as written."""
    return [match.group(1) for match in _CANDIDATE_RE.finditer(text)]


def _digits_only(raw: str) -> str:
    return _NON_DIGITS_RE.sub("", raw)


def classify(digits: str) -> Optional[CountryFormat]:
    """Match a digit string that already starts with a calling code.

    `digits` should not include a leading '+'. Returns the matching
    CountryFormat, or None if no known format fits.
    """
    for fmt in sorted(COUNTRY_FORMATS, key=lambda f: -len(f.calling_code)):
        if digits.startswith(fmt.calling_code):
            national = digits[len(fmt.calling_code):]
            if len(national) in fmt.national_lengths:
                return fmt
    return None


def normalize(raw: str, default_country: Optional[str] = None) -> Optional[str]:
    """Turn a raw phone-number-looking string into E.164 form (e.g. "+14155550100").

    Returns None if the string can't be resolved against a known format.

    If `raw` has no leading '+', `default_country` (a key from patterns.py,
    e.g. "US" or "GB") is used to interpret it as a locally-dialed number.
    Without a leading '+' and without `default_country`, the string is only
    resolved if it already includes a recognizable calling code.
    """
    raw = raw.strip()
    digits = _digits_only(raw)
    if not digits:
        return None

    if raw.startswith("+"):
        fmt = classify(digits)
        return f"+{digits}" if fmt else None

    if default_country is not None:
        fmt = COUNTRY_FORMATS_BY_KEY.get(default_country.upper())
        if fmt is None:
            return None
        national = digits
        if fmt.trunk_prefix and national.startswith(fmt.trunk_prefix):
            national = national[len(fmt.trunk_prefix):]
        if len(national) in fmt.national_lengths:
            return f"+{fmt.calling_code}{national}"
        return None

    fmt = classify(digits)
    return f"+{digits}" if fmt else None
