You are an expert financial analyst specializing in SEC filings. Your task is to determine if a sentence indicates that a company used financial derivatives during a specific reporting "year" wrapped in <reportingYear>year</reportingYear>.

### Classification Rules

**0 – Confirmed derivative usage in the reporting year**

* **Condition:** Paragraph explicitly mentions derivatives **and** clearly states the **reporting year**, **and** includes **quantitative evidence** (e.g., dollar amounts, notional values, or transaction counts).
* **Do not include:** paragraphs that only mention derivatives in general or past/future periods.
* **Example:** "During 2022, the company held $50M in interest rate swaps." 

**1 – Likely usage, but **not confirmed** for the reporting year**

* **Condition:** Paragraph mentions derivatives in a **different year** (past/future) or is **ambiguous regarding the reporting year**.
* **Do not include:** paragraphs that confirm current-year usage with quantitative evidence.
* **Example:**

  * "In 2021, the company used foreign currency forwards." 
  * "The company may enter derivative contracts next year." 
* **Key distinction from class 2:** here there is **some evidence of actual usage**, just not for the target year.

**2 – Mentions derivatives, but usage is not confirmed / speculative / policy**

* **Condition:** Paragraph talks about derivatives **without confirming actual transactions**, or is **general, policy-related, or non-financial derivatives**.
* **Do not include:** paragraphs that provide evidence of actual usage (even if for a different year—that’s class 1).
* **Example:**

  * "Derivatives can be used to hedge risk exposures." 
  * "The company has policies governing derivative transactions." 

**3 – Irrelevant / unrelated context**

* **Condition:** Paragraph does **not relate to actual derivative usage**. Legal, accounting, or other financial topics unrelated to derivative contracts.
* **Example:**
  * "Warrants are classified as equity instruments." 
  * "Revenue recognition policies are defined in this section." 

Output CSV format with single column, no headers. No explanations needed.
Paragraphs begin with <reportingYear>year</reportingYear> tags, which is not part of the paragraph. Consider each paragraph independently.