# phonefmt

Free text tends to have phone numbers scattered through it in whatever shape
whoever typed it happened to use: `(415) 555-0100`, `+44 20 7946 0958`,
`0033 1 42 68 53 00`, `91-98765-43210`. There's no standard-library way to
pull those out and turn them into something comparable.

Full validation against real-world numbering plans (area code ranges, mobile
vs. landline prefixes, and so on) needs a maintained database — that's what
libphonenumber is for, and it's out of scope for a dependency-free library.
`phonefmt` does something smaller: it recognizes a short, explicit list of
country formats (see `phonefmt/patterns.py`) and normalizes what it
recognizes to E.164. Anything outside that list comes back as `None` rather
than a guess.

## Install

Not published anywhere yet. Clone it and install in editable mode, or just
copy `src/phonefmt` into your project.

## Usage

Normalize a single string once you know where it's from:

```python
from phonefmt import normalize

normalize("+1 (415) 555-0100")        # "+14155550100"
normalize("020 7946 0958", "GB")      # "+442079460958"
normalize("not a phone number")       # None
```

Render a number in a readable local style instead of E.164:

```python
from phonefmt import format_national

format_national("+442079460958")       # "020 7946 0958"
format_national("415-555-0100", "US")  # "415 555 0100"
```

The grouping is an approximation - a handful of countries (US, GB, France,
Australia, Spain, Mexico) get a shape matching real convention, everything
else falls back to grouping digits in 3s. It's meant for skimmable output,
not for reproducing exactly what a phone company would print.

Pull every phone-number-looking substring out of a blob of text:

```python
from phonefmt import extract_candidates

extract_candidates("call 415-555-0100 or +44 20 7946 0958 for support")
# ["415-555-0100", "+44 20 7946 0958"]
```

Scan a whole file, one candidate per hit:

```python
from phonefmt import read_numbers

for raw, normalized in read_numbers("contacts.txt", default_country="US"):
    print(raw, "->", normalized or "unrecognized")
```

Or scan stdin the same way, so the same function works whether the input is
a saved file or piped in:

```python
# scan.py
import sys
from phonefmt import read_numbers

for raw, normalized in read_numbers(sys.stdin, default_country="US"):
    print(raw, "->", normalized or "unrecognized")
```

```
cat contacts.txt | python scan.py
grep phone support-tickets.log | python scan.py
```

`read_numbers` (and the lower-level `iter_lines`) accept a file path, an
already-open file object, or `None` for stdin — the caller doesn't need to
branch on which one it's dealing with.

Save the results instead of printing them:

```python
from phonefmt import read_numbers, write_csv, write_json

hits = list(read_numbers("contacts.txt", default_country="US"))
write_csv(hits, "contacts.csv")
write_json(hits, "contacts.json")
```

Both accept a path or an already-open writable file, matching the input
side. Numbers that couldn't be resolved are kept in the output (empty field
in CSV, `null` in JSON) rather than silently dropped.

## Supported formats

Currently: US/Canada (NANP), UK, Germany, France, Australia, India, Japan,
Netherlands, Italy, Spain, Mexico. Add more by appending a `CountryFormat`
to `COUNTRY_FORMATS` in `patterns.py`.

## License

MIT, see LICENSE.
