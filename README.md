# Largest Number in a PDF

Finds the largest number in a PDF, two ways:

- **Raw**: the greatest numerical value as printed.
- **Adjusted**: the greatest value after applying the document's own scale language. A table headed `(Dollars in Millions)` means `30,704.1` is really `30,704,100,000`.


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
Largest adjusted value:       30,704,100,000
```

## How it works

Three small functions in `main.py`:

1. `read_pages` pulls the text from every page with PyMuPDF.
2. `detect_scale` reads a multiplier from headers like `(Dollars in Millions)`.
3. `find_largest` walks each page top to bottom, carries the most recent header's scale, and tracks the largest raw and adjusted values.