# Synthetic Financial Text Generation for NLP Model Training

## Project Overview

This project is designed for researchers and developers in the fields of Natural Language Processing (NLP) and computational finance. It provides a sophisticated data generation tool, `dv_w-generator.qmd`, for creating synthetic financial text data. This data mimics the language and structure found in corporate financial disclosures, such as SEC filings (10-K, 10-Q).

The primary purpose of this tool is to generate large, labeled datasets for training and evaluating machine learning models that can understand and classify complex financial narratives.

## Research Focus

The generator focuses on several key areas of financial reporting, which are often challenging for NLP models to interpret correctly:

*   **Derivatives and Hedging:** Generates text describing various derivative instruments (e.g., swaps, options, forwards) and their use in hedging against interest rate, foreign exchange, and commodity price risks.
*   **Warrants and Embedded Derivatives:** Creates examples of disclosures related to equity and liability-classified warrants, as well as complex embedded derivatives within financial instruments.
*   **Fair Value Measurement:** Produces text detailing the valuation methodologies (e.g., Black-Scholes, Monte Carlo) and assumptions used to determine the fair value of financial instruments.
*   **Financial Disclosures:** The generated text includes a wide range of common financial reporting topics, including:
    *   Debt and Credit Facilities
    *   Income Taxes
    *   Goodwill and Intangible Assets
    *   Leases
    *   Inventory
    *   Revenue Recognition

## Methodology

The `dv_w-generator.qmd` file is a Quarto document that combines Python code with narrative text. It uses a template-based approach to generate synthetic data. The core of the generator consists of:

*   **A rich set of templates:** These are pre-defined sentence and paragraph structures that capture the typical language of financial disclosures.
*   **Placeholder variables:** The templates are populated with a wide variety of financial terminology, company names, dates, and numerical data to create diverse and realistic text.
*   **Categorized data generation:** The code is organized to generate text for specific financial topics, allowing for the creation of labeled datasets.

## Placeholder-Based Text Generation

The script generates text by taking a template string and replacing placeholders with randomly selected values. The placeholders are denoted by curly braces `{}`.

For example, a template for a warrant issuance might look like this:

```
"In connection with the {event}, {company} issued warrants to purchase up to {shares} shares of common stock at an exercise price of {currency_code}{price} per share..."
```

The script then replaces the placeholders with values from predefined lists:

*   `{event}` might be replaced with "a debt financing transaction" or "an initial public offering".
*   `{company}` would be a randomly selected company name.
*   `{shares}` would be a number of shares.
*   `{currency_code}` could be "USD", "€", etc.
*   `{price}` would be a stock price.

This process allows for the generation of a vast number of unique sentences, all grammatically correct and contextually relevant to financial disclosures.

### Example of Generated Text

Here are a few examples of text that could be generated from the templates in the script:

**Derivatives:**

> "As of December 31, 2023, the fair value of the swaps was a liability of $12.3 million, the opposite entry for $10.1 million of which was credited to "Other comprehensive income" under the cost of hedging accounting treatment."

**Warrants:**

> "In connection with the series B preferred stock offering, MegaCorp Inc. issued warrants to purchase up to 500,000 shares of common stock at an exercise price of $25.50 per share, in accordance with the guidance contained in FASB ASC 815 "Derivatives and Hedging" whereby under that provision the warrants do not meet the criteria for equity treatment and must be recorded as a liability."

**Hedging:**

> "To mitigate market risks, Global-Tech Ltd. may enter into a combination of derivatives and operational risk management."

## Motivation and Limitations

This synthetic data generator was created to address the need for large, labeled datasets for training NLP models on financial text. While real SEC filings are abundant, they are unlabeled and can be time-consuming to annotate manually. This tool provides a way to quickly generate a large corpus of labeled data that captures the syntactic and semantic patterns of financial disclosures.

The templates used in this generator are based on a qualitative analysis of real SEC filings. They are designed to reflect the common language and structures used in financial reporting. However, it is important to note the following limitations:

*   **Not exhaustive:** The templates do not cover every possible variation of financial disclosure. There will be instances of real-world financial text that are not represented in the generated data.
*   **Simplified context:** The generated text is created from individual templates and does not capture the broader context of a full financial report.
*   **No novel language:** The generator can only produce text based on the templates and placeholders it has been given. It cannot generate truly novel or creative language.
*   **Potentially nonsensical combinations:** Due to the random nature of placeholder replacement, some generated sentences may appear nonsensical from a human perspective. For example, a sentence might mention a valuation model that is not typically used for a specific financial instrument, or combine monetary units in an illogical way. However, for the purpose of training an NLP model, these sentences still provide valuable syntactic and structural information, and help the model to generalize to a wider range of inputs.

Despite these limitations, the generated data provides a valuable resource for training and evaluating NLP models on financial text, especially for tasks like classification and named entity recognition.

## Usage

The generated data is outputted to an Excel file (`training_data.xlsx`) and a Parquet file (`training_data.parquet`). This data can be used to:

*   Train classification models to identify specific types of financial disclosures.
*   Develop named entity recognition (NER) models to extract key information from financial text.
*   Evaluate the performance of existing NLP models on financial language.
*   Conduct research into the linguistic characteristics of financial reporting.

To use the generator, execute the Quarto file `dv_w-generator.qmd`. The output files will be created in the same directory.

**Note:** This tool is for research and development purposes. The generated data is synthetic and should not be used for actual financial analysis or investment decisions.
