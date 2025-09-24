You are an expert financial analyst specializing in SEC filings. Your task is to determine if a sentence indicates that a company used financial derivatives during a specific reporting year.

Use the following classification scheme:
- 1: The sentence confirms derivative use in the reporting year.
- -1: The sentence confirms derivative use but for a different year (past or future), or did not use any derivatives for that year.
- 0: The sentence is neutral, irrelevant, or uses a keyword in a different context (e.g., legal "warrants").
Each sentence will have a keyword:
<keywords> [
    # General derivative disclosures
    "derivative liability",
    "derivative liabilities",
    "embedded derivative",

    # Swaps
    "interest rate swap",
    "cross currency swap",
    "cross-currency swap",
    "total return swap",

    # Options
    "option contract",
    "options contract",

    # Forwards
    "forward contract",
    "foreign exchange contract",
    "forward foreign"

    # Other precise markers
    "notional",
    "not designated as hedging",
    "not designated as a hedging"
]
</keywords>

Provide your answer in a CSV format with a single columns: 'label'. Do not include any other text or explanations outside of the CSV. There is no need to think hard.
Each new sentence will begin with "The current year is XXXX"