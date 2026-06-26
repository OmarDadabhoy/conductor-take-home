"""Find the largest number in a PDF, both raw and scale-adjusted."""

import re
import fitz  # PyMuPDF

# If we see a word like thousand million billion or trillion this tells us how much to multiply that number by.
SCALE = {
    "thousand": 1_000,
    "million": 1_000_000,
    "billion": 1_000_000_000,
    "trillion": 1_000_000_000_000,
    "quadrillion": 1_000_000_000_000_000,
    "quintillion": 1_000_000_000_000_000_000,
}

# REGEX to capture all the words that could come after a number to signify the number.
_SCALE_PHRASE = re.compile(r"\bin\s+(thousand|million|billion|trillion|quadrillion|quintillion)s?\b", re.IGNORECASE)

# REGEX to capture numbers in the text along with decimals and all that.
_NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?|\.\d+")


def read_pages(pdf_path):
    """
    Input: pdf_path

    Uses PyMuPDF (fitz) to read the PDF and extract text from each page.

    Return a list of page texts, one string per page.
    """
    with fitz.open(pdf_path) as doc:
        return [page.get_text() for page in doc]


def detect_scale(text):
    """
    Input: a line of text.

    Output: the multiplier that the line declares, e.g. "(Dollars in Millions)" -> 1_000_000.

    Returns 1 when the line names no scale.
    """
    match = _SCALE_PHRASE.search(text)
    return SCALE[match.group(1).lower()] if match else 1


def find_largest(pages):
    """
    Input: list of page texts.

    Output: The largest raw value and the largest scale-adjusted value in the document.

    Walking each page top to bottom, we carry the scale from the most recent header and
    apply it to the numbers below it. Only decimal numbers are scaled, so bare integers
    like headcounts and years are never mistaken for abbreviated dollar figures.

    Each result is a (value, page_number, line_index) tuple.
    """
    raw_best = (0.0, 0, 0)
    adjusted_best = (0.0, 0, 0)
    for page_number, text in enumerate(pages, start=1):
        scale = 1
        for line_index, line in enumerate(text.splitlines()):
            declared = detect_scale(line)
            if declared != 1:
                scale = declared
            for token in _NUMBER.findall(line):
                value = float(token.replace(",", ""))
                adjusted = value * scale if "." in token else value
                raw_best = max(raw_best, (value, page_number, line_index))
                adjusted_best = max(adjusted_best, (adjusted, page_number, line_index))
    return raw_best, adjusted_best


if __name__ == "__main__":
    pages = read_pages("FY25_Air_Force_Working_Capital_Fund.pdf")
    (raw_value, raw_page, raw_line), (adj_value, adj_page, adj_line) = find_largest(pages)

    print(f"Largest raw value:      {raw_value:>20,.0f}")
    print(f"Largest adjusted value: {adj_value:>20,.0f}")
