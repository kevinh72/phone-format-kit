"""Reading candidate phone numbers from a file path, an open file, or stdin.

The one thing worth getting right here: callers shouldn't need a different
code path depending on whether the input is `sys.stdin`, a path string, or
a file object some caller already opened (e.g. from a zip archive or an
`io.StringIO` in a test). All three work the same way through `iter_lines`.
"""

import sys
from pathlib import Path
from typing import Iterable, Iterator, Optional, Tuple, Union

from .core import extract_candidates, normalize

Source = Union[str, Path, Iterable[str], None]


def _iter_stream(stream: Iterable[str]) -> Iterator[str]:
    for line in stream:
        line = line.strip()
        if line:
            yield line


def iter_lines(source: Source = None) -> Iterator[str]:
    """Yield non-empty, stripped lines from `source`.

    `source` may be:
      - None, meaning read from stdin
      - a file path (str or Path), which is opened and closed here
      - anything else iterable line-by-line (an open file object, a list
        of strings, an io.StringIO, ...)
    """
    if source is None:
        yield from _iter_stream(sys.stdin)
        return

    if isinstance(source, (str, Path)):
        with open(source, "r", encoding="utf-8") as handle:
            yield from _iter_stream(handle)
        return

    yield from _iter_stream(source)


def read_numbers(
    source: Source = None, default_country: Optional[str] = None
) -> Iterator[Tuple[str, Optional[str]]]:
    """Scan `source` for phone-number-looking text and normalize each hit.

    Yields (raw, normalized) pairs, one per candidate found. `normalized` is
    the E.164 form, or None if the candidate couldn't be resolved against a
    known format. See `iter_lines` for what `source` accepts.
    """
    for line in iter_lines(source):
        for raw in extract_candidates(line):
            yield raw, normalize(raw, default_country=default_country)
