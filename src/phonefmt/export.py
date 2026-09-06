"""CSV and JSON export for the (raw, normalized) pairs `read_numbers` produces."""

import csv
import json
from pathlib import Path
from typing import Iterable, Optional, TextIO, Tuple, Union

Rows = Iterable[Tuple[str, Optional[str]]]
Destination = Union[str, Path, TextIO]


def write_csv(rows: Rows, dest: Destination) -> None:
    """Write (raw, normalized) pairs to `dest` as CSV with a header row.

    `dest` may be a path (str/Path) or an already-open writable text file,
    same flexibility as `iter_lines` on the input side. A candidate that
    couldn't be resolved is written with an empty `normalized` field.
    """
    if isinstance(dest, (str, Path)):
        with open(dest, "w", encoding="utf-8", newline="") as handle:
            _write_csv_rows(rows, handle)
    else:
        _write_csv_rows(rows, dest)


def _write_csv_rows(rows: Rows, handle: TextIO) -> None:
    writer = csv.writer(handle)
    writer.writerow(["raw", "normalized"])
    for raw, normalized in rows:
        writer.writerow([raw, normalized or ""])


def write_json(rows: Rows, dest: Destination) -> None:
    """Write (raw, normalized) pairs to `dest` as a JSON array of objects.

    `dest` may be a path (str/Path) or an already-open writable text file.
    Unlike `write_csv`, an unresolved candidate keeps `normalized` as JSON
    `null` rather than an empty string, since JSON has a way to say that
    directly.
    """
    objects = [{"raw": raw, "normalized": normalized} for raw, normalized in rows]
    if isinstance(dest, (str, Path)):
        with open(dest, "w", encoding="utf-8") as handle:
            json.dump(objects, handle, indent=2)
    else:
        json.dump(objects, dest, indent=2)
