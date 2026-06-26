# Largest Number in a PDF

Finds the largest number in a PDF, two ways:

- **Raw**: the greatest numerical value as printed.
- **Adjusted**: the greatest value after applying the document's own scale language. A table headed `(Dollars in Millions)` means `30,704.1` is really `30,704,100,000`.

Built for ConductorAI's take-home, run against `FY25_Air_Force_Working_Capital_Fund.pdf`.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Output:

```
Largest raw value:                 6,000,000
    page 93: ...costing between | $250,000 and $6,000,000) and are designed...

Largest adjusted value:       30,704,100,000
    page 13: FY 2025 | Total Revenue | T | 28,239.2 | 29,176.6 | 30,704.1
```

Each result prints its page and the surrounding text, so the answer can be eyeballed rather than trusted blindly.

## How it works

Four small functions in `main.py`:

1. `read_pages` pulls the text from every page with PyMuPDF.
2. `detect_scale` reads a multiplier from headers like `(Dollars in Millions)`.
3. `find_largest` walks each page top to bottom, carries the most recent header's scale, and tracks the largest raw and adjusted values.
4. `snippet` returns the lines around a hit so the result is verifiable.

### The one decision worth explaining

A `(Dollars in Millions)` header governs a whole table, but those tables also hold numbers that are not dollars: headcounts (`Military End Strength: 35,110`), years, percentages. Scaling those by a million invents nonsense. In fact the naive approach reports the largest value as `$35 billion`, which is really a headcount of 35,110 people.

In this document every dollar figure is printed with a decimal (`30,704.1`, `400.000`) while headcounts and years are bare integers (`35,110`, `2025`). So the scale is applied only to numbers that carry a decimal point. That single rule turns the adjusted answer from a bogus $35B headcount into the real $30.7B Total Revenue.

## Assumptions and limitations

- Extracted text is trusted as-is (no OCR-error correction).
- Scale carries within a page and resets at each new page, so a header never silently governs pages far below it.
- The decimal rule is a formatting convention that fits federal budget tables. A document that printed whole-dollar millions without decimals would need a different rule.
- Inline prose mentions (`9.6 billion`) and the `($M)` shorthand both appear in the document but stay below the $30.7B answer, so they are not specially handled.
