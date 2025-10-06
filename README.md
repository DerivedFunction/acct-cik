# Hedge and Derivative Analysis Results - Complete Documentation

## Overview

This repository contains the results of an automated sentence-level analysis of corporate SEC filings (10-Ks, 10-Qs, 20-Fs) that identify and classify derivative and hedging activities. A fine-tuned machine learning model analyzes financial disclosures to detect interest rate, foreign exchange, commodity price hedging, as well as derivative liabilities and embedded derivatives.

The analysis compares two methods of identifying derivative users:
1. **Keyword Search Method**: Original approach using pattern matching in financial reports
2. **Machine Learning Model**: Trained classifier that analyzes sentence-level context

---

## Important Limitations and Caveats

⚠️ **File Sizes**: Some Excel files exceed 20 MB (sentence-level data can exceed 100 MB). Excel may be slow to load or fail to load entirely.

⚠️ **Accuracy Level**: Classifications are suitable for research-level analysis but not guaranteed for regulatory or audit-level precision.

⚠️ **Text Filtering**: The model only classifies text filtered for derivative-related keywords. It does not process or contain other filing content.

⚠️ **Missing Data**: Approximately 264,000 results versus 269,000 total rows. Some reports are missing due to automated data collection failures.

⚠️ **Foreign Filers**: 20-F filings for foreign companies may not contain full accounting report content and may be misclassified as having "none."

⚠️ **Duplicate Text**: Companies often repeat disclosure language across years. The analysis includes intentional duplicates and overlapping sentences from surrounding context, which inflates result counts.

⚠️ **Intended Use**: For exploratory and comparative analysis only. Not for financial or legal determinations.

---

## Data Generation and Model Training

### Synthetic Training Data

The model was trained using synthetically generated financial text created by `dv_w-generator.qmd`. This Quarto document generates realistic financial disclosure language using:

**Template-Based Generation**: Pre-defined sentence structures capturing typical financial disclosure patterns
- Placeholder variables populated with financial terminology, company names, dates, and numerical data
- Example template: `"In connection with the {event}, {company} issued warrants to purchase up to {shares} shares..."`
- Placeholders replaced with randomly selected values from predefined lists

**Training Data Categories**:
- Derivatives and hedging instruments (swaps, options, forwards)
- Interest rate, foreign exchange, and commodity price risk management
- Warrants and embedded derivatives
- Fair value measurement methodologies
- Common financial reporting topics (debt, taxes, goodwill, leases, inventory, revenue)

**Known Limitations of Training Data**:
- Not exhaustive of all possible financial disclosure variations
- Simplified context (individual templates, not full report context)
- Cannot generate novel language beyond provided templates
- May produce nonsensical combinations (e.g., unusual valuation models, illogical monetary units)
- Despite limitations, provides valuable syntactic and structural patterns for model generalization

**Output**: Training data saved as `training_data.xlsx` and `training_data.parquet`

---

## Text Extraction Methodology

To avoid processing unrelated text, a strict keyword search filters content before model classification. The filtering uses specific regular expressions:

### Interest Rate Derivatives (IR_REGEX)
- interest rate contract/derivative/instrument/forward/future
- interest rate collar/swap/option/cap/floor/lock
- zero coupon swap, single currency basis swap, swaption

### Foreign Exchange / Currency Derivatives (FX_REGEX)
- forward rate agreement/contract/option
- foreign exchange contract/derivative/instrument/forward/future/swap/option/cap/floor/collar
- currency contract/derivative/instrument/forward/future/swap/option/cap/floor/collar
- cross-currency contract/derivative/instrument/forward/future/swap/option/cap/floor/collar

### Commodity Price Derivatives (CP_REGEX)
- commodity contract/derivative/instrument/forward/future/option/cap/floor/collar/swap
- commodity price contract/derivative/instrument/forward/future/option/cap/floor/collar/swap

**Note**: May miss commodity-specific names like "natural gas future" (though GEN_REGEX may catch them)

### General Derivative & Hedge Terminology (GEN_REGEX)
⚠️ **Key Insight**: The model classified certain general text as derivative liabilities/warrants and embedded derivatives

- derivative contract/instrument/financial instrument/position/asset/liability/expense/gain/loss
- change in fair value of derivative
- gain/loss on derivative
- embedded derivative
- hedge/hedging/hedged/hedges of/instrument/contract/derivative/relationship/accounting/program/transaction/activity
- designated as cash flow/fair value/net investment hedge
- instruments/contracts are designated
- ineffective portion (hedge ineffectiveness)
- notional amount/value/principal/contract/exposure
- forward contract, futures contract
- call/put option/contract
- option contract
- swap contract/agreement/transaction (with optional prefixes: interest rate, currency, commodity, equity, credit)
- swaption
- cap/floor/collar/lock agreement

### Special / Accounting References (SPEC_REGEX)
- financial derivative
- may use derivatives
- over-the-counter derivative, OTC derivative
- A.S.C. 815, ASC 815 (accounting standard for derivatives and hedging)

**Future Consideration**: Time permitting, keyword terms could be relaxed to include more derivative liabilities/warrants and embedded derivatives, though this may impact model accuracy if keywords are incorrectly associated with labels.

---

## Excel Files Overview

### 1. SERVER_RESULTS.xlsx
Main sentence-level analysis file containing all classified hedge and derivative sentences.

| Sheet Name | Description |
|------------|-------------|
| all_reports | All extracted sentences with model classifications by hedge/derivative type |
| Current Hedging | Firms currently using hedging instruments (IR, FX, or CP) |
| Hedging Past Year | Firms with historic hedges (expired or undated) |
| Speculation Only | Sentences referring to speculative or trading derivatives |
| Derivative Liabilities Warrants | Mentions of derivative liabilities, warrants, or fair value losses |
| Embedded Derivatives | Embedded or hybrid derivative disclosures |
| unique_per_year | Unique firm counts per hedge type by year |
| label_cooccurrence | Frequency of hedge labels appearing together (e.g., FX + IR) |
| Hedging by Type | Hedge type summaries by firm and year |
| Hedge Type Cross | Cross-tab of firms hedging across multiple categories |

**Use Cases**:
- Filter or pivot by hedge type, firm, or year
- Track firms switching from current to historic hedging
- Examine how companies describe different hedge types

---

### 2. keywords_comparison_HEDGES_CURRENT.xlsx
**Focus**: Current-year hedging only (IR, FX, CP)

Compares model predictions against keyword-based detection for current hedges.

| Sheet Name | Description |
|------------|-------------|
| KW_Model_Comparison | High-level performance metrics and improvements |
| Summary_Current_Only | Summary metrics for current hedge classification |
| Detailed_Current_Only | Firm-year level comparison of keyword vs. model agreement |
| Basic_Current_Only | Simplified current hedge comparison |
| Confusion_Overall_Curr | Overall confusion matrix by hedge type |
| Confusion_FX_Curr | Foreign exchange-specific confusion matrix |
| Confusion_IR_Curr | Interest rate-specific confusion matrix |
| Confusion_CP_Curr | Commodity price-specific confusion matrix |

---

### 3. keywords_comparison_HEDGES_ALL.xlsx
**Focus**: Current + historic hedging (IR, FX, CP)

Shows how including historical hedge mentions improves detection accuracy.

| Sheet Name | Description |
|------------|-------------|
| Summary_Curr_Historic | Combined summary of hedge accuracy across all years |
| Detailed_Curr_Historic | Firm-year breakdown for extended comparison |
| Basic_Curr_Historic | Simplified extended comparison |
| Confusion_Overall_All | Overall confusion matrix across both periods |
| Confusion_FX_All | FX-specific confusion matrix |
| Confusion_IR_All | IR-specific confusion matrix |
| Confusion_CP_All | CP-specific confusion matrix |

---

### 4. keywords_comp_ALL_DERIVATIVES_CURRENT.xlsx
**Focus**: All current derivatives (hedges + liabilities + embedded)

Broader view including derivative types beyond just hedging.

| Sheet Name | Description |
|------------|-------------|
| KW_Model_Comparison | High-level performance metrics and improvements |
| Summary_Current_Only | Current-year derivative comparison summary |
| Detailed_Current_Only | Detailed row-level results for all derivative types |
| Basic_Current_Only | Simplified results view |
| Confusion_Overall_Curr | Overall confusion matrix (all derivatives) |
| Confusion_FX_Curr | FX-specific confusion matrix |
| Confusion_IR_Curr | IR-specific confusion matrix |
| Confusion_CP_Curr | CP-specific confusion matrix |
| ModelOnly_Liab_Embed | Cases detected by model only (no keyword comparison) |

---

### 5. keywords_comp_ALL_DERIVATIVES_FULL.xlsx
**Focus**: All derivatives, current + historic

Most comprehensive view including all derivative types across time periods.

| Sheet Name | Description |
|------------|-------------|
| Summary_Curr_Historic | Full-period summary for all derivative classifications |
| Detailed_Curr_Historic | Extended row-level detail |
| Basic_Curr_Historic | Simplified comparison view |
| Confusion_Overall_All | Overall confusion matrix across all years |
| Confusion_FX_All | FX-specific confusion matrix |
| Confusion_IR_All | IR-specific confusion matrix |
| Confusion_CP_All | CP-specific confusion matrix |
| ModelOnly_Liab_Embed | Model-only detections across full period |

---

### 6. KW_MODEL_COMPARISON.xlsx
Standalone workbook for overall keyword vs. model comparison.

| Sheet Name | Description |
|------------|-------------|
| KW_Model_Comparison | Aggregate metrics comparing current vs. current+historic |
| Model_Performance_Summary | Consolidated accuracy, precision, recall, and F1 scores across all workbooks |

**Use Case**: Quick validation of overall model performance versus keyword-based method.

---

## Key Differences Between Workbooks

| Aspect | Hedges Workbooks | All Derivatives Workbooks |
|--------|------------------|---------------------------|
| **Overall category** | IR + FX + CP hedges only | Hedges + Liabilities + Embedded |
| **Scope** | Focused on hedging activities | Comprehensive derivative coverage |
| **Comparison validity** | Direct comparison to keywords | Partial comparison (hedges only) |
| **Extra insights** | None | ModelOnly_Liab_Embed sheet |

---

## Understanding the Sheets

### Sheet: KW_Model_Comparison
**What it shows**: High-level performance comparison between current-only and current+historic approaches.

**Key Metrics**:
- **Accuracy**: Overall percentage of correct classifications
- **Precision**: When model says "yes," how often is it correct?
- **Recall**: Of all companies that should be identified, how many did model find?
- **F1 Score**: Balanced measure combining precision and recall
- **Improvement**: How much better current+historic performs vs. current-only

**Interpretation**: Positive improvements indicate that including historic data enhances model performance.

---

### Sheet: Summary (Current_Only or Curr_Historic)
**What it shows**: Detailed performance metrics for each category.

**Categories**:
- **Overall**: Either "Hedges Only (IR/FX/CP)" or "All Derivatives (Hedges + Liabilities + Embedded)"
- **Foreign Exchange (FX)**: Currency hedging
- **Interest Rate (IR)**: Interest rate hedging
- **Commodity Price (CP)**: Commodity price hedging

**Metrics Explained**:

| Metric | Formula | Meaning |
|--------|---------|---------|
| **True Positives (TP)** | — | Both model and keywords say "yes" |
| **False Positives (FP)** | — | Model says "yes," keywords say "no" |
| **True Negatives (TN)** | — | Both say "no" |
| **False Negatives (FN)** | — | Model says "no," keywords say "yes" |
| **Total** | — | Total company-year observations |
| **Accuracy** | (TP + TN) / Total × 100 | Overall agreement rate |
| **Precision** | TP / (TP + FP) × 100 | Correctness when model says "yes" |
| **Recall** | TP / (TP + FN) × 100 | Coverage of keyword-identified cases |
| **F1 Score** | 2 × (Precision × Recall) / (Precision + Recall) | Balanced performance measure |
| **Agreement Rate** | (TP + TN) / Total × 100 | Same as Accuracy |

**How to Interpret**:
- **High accuracy (>90%)**: Strong agreement between methods
- **High precision**: Model rarely identifies false positives
- **High recall**: Model catches most of what keywords catch
- **High F1**: Balanced performance

---

### Sheet: Detailed (Current_Only or Curr_Historic)
**What it shows**: Row-by-row comparison for every company-year observation.

**Key Columns**:
- **cik, year**: Company identifier and fiscal year
- **keyword_user, keyword_fx, keyword_ir, keyword_cp**: Keyword results (1=yes, 0=no)
- **model_user_current/all, model_fx_current/all, etc.**: Model results (1=yes, 0=no)
- **overall_agree, fx_agree, ir_agree, cp_agree**: Agreement flags (1=agree, 0=disagree)
- **overall_classification**:
  - *True Positive*: Both say derivative user
  - *True Negative*: Both say non-user
  - *False Positive*: Model says user, keywords say non-user
  - *False Negative*: Model says non-user, keywords say user

**Use Case**: Drill down into specific disagreements to understand where and why methods differ.

---

### Sheet: Basic (Current_Only or Curr_Historic)
**What it shows**: Raw comparison data without additional classification columns.

**Use Case**: Export for custom analysis or integration with other datasets.

---

### Sheets: Confusion Matrices
**What it shows**: 2×2 tables showing agreement/disagreement patterns.

**Structure**:
```
                    Model_No    Model_Yes
Keyword_No          TN          FP
Keyword_Yes         FN          TP
```

**Interpretation**:
- **Top-left (TN)**: Both methods agree there's no derivative use
- **Top-right (FP)**: Model found it, keywords didn't (possible improvement or false alarm)
- **Bottom-left (FN)**: Keywords found it, model didn't (potential miss)
- **Bottom-right (TP)**: Both methods agree on derivative use

**Four Matrices Provided**:
1. **Confusion_Overall**: Overall hedge or derivative use
2. **Confusion_FX**: Foreign exchange hedging
3. **Confusion_IR**: Interest rate hedging
4. **Confusion_CP**: Commodity price hedging

**Reading the Matrix**:
- Large **TP and TN** values = Strong agreement
- Large **FP** values = Model is more sensitive (finds more cases)
- Large **FN** values = Keywords are more sensitive (or model missing cases)

---

### Sheet: ModelOnly_Liab_Embed (All Derivatives workbooks only)
**What it shows**: Statistics for derivative types not covered by keyword search.

**Categories**:
- **Derivative Liabilities/Warrants**: Financial obligations and warrants
- **Embedded Derivatives**: Derivatives embedded in other contracts

**Metrics**:
- **Total**: Number of company-year observations
- **Model_Positive**: Number identified by model
- **Model_Negative**: Number not identified
- **Positive_Rate**: Percentage identified

**Important**: These categories have no keyword comparison because the original keyword search didn't target them. This demonstrates additional value the model provides beyond keyword matching.

---

## Ground Truth and Validation

### What is "Ground Truth"?

For this analysis, **keyword-based search results serve as the ground truth** (baseline for comparison). This means:
- When keywords identify a company as a derivative user, we treat that as the "correct" answer
- Model predictions are evaluated against these keyword results
- Accuracy measures how often the model agrees with keyword search

### Important Caveat

This does NOT mean keywords are perfect. It means we use them as our validation baseline since they represent the original, established methodology. 

**The model may actually identify cases that keywords miss** (shown as "False Positives"), which could represent genuine improvements rather than errors. Manual review of disagreements is recommended to distinguish between:
- Model improvements (catching cases keywords missed)
- Model errors (incorrect classifications)

---

## How Scores Are Calculated

### Accuracy
Percentage of correct predictions (agreements):
```
Accuracy = (True Positives + True Negatives) / Total Observations × 100
```

**Example**: If we analyzed 1,000 company-years:
- 850 agreements (700 TN + 150 TP)
- 150 disagreements (100 FP + 50 FN)
- Accuracy = (150 + 700) / 1,000 × 100 = **85%**

### Precision
When model predicts "derivative user," how often is it correct (agrees with keywords)?
```
Precision = True Positives / (True Positives + False Positives) × 100
```

### Recall (Sensitivity)
Of all keyword-identified derivative users, what percentage did the model find?
```
Recall = True Positives / (True Positives + False Negatives) × 100
```

### F1 Score
Balanced measure combining precision and recall:
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

**Why it matters**: High F1 means the model is both precise (few false alarms) and comprehensive (catches most cases).

---

## Interpreting Results

### High Agreement (Accuracy > 90%)
The model and keywords largely agree. The model is a reliable alternative to keyword searching.

### High Precision, Lower Recall
Model is conservative. It rarely makes mistakes but might miss some cases. **Action**: Review False Negatives to understand what was missed.

### Lower Precision, High Recall
Model is aggressive. It catches more cases but may have more false alarms. **Action**: Review False Positives to determine if they're genuine improvements or errors.

### Improvement from Current to Current+Historic
Positive improvements show that including historical mentions enhances detection. This is especially valuable for companies that discuss past derivative use.

---

## Keyword vs. Model Classification Scope

### Directly Comparable Categories:
- Interest Rate (IR) hedging
- Foreign Exchange (FX) hedging
- Commodity Price (CP) hedging

### Excluded from Comparison:
- Unknown / general hedge mentions
- Derivative liabilities or warrants
- Embedded derivatives

This keeps evaluation focused on true hedging categories where both methods can be directly compared.

---

## Column Definitions

| Column | Description |
|--------|-------------|
| cik | SEC Central Index Key (company identifier) |
| year | Filing year (e.g., 2024) |
| url | Source link to 10-K, 10-Q, or 20-F filing |
| sentence | Extracted sentence containing derivative/hedging language |
| label | Model-assigned classification (e.g., IR Hedge, FX Hedge, Embedded Derivative) |
| label_id | Internal model ID reference (for debugging) |

---

## Practical Applications

### 1. Research Validation
Validate whether keyword-based findings align with contextual model predictions.

### 2. Identifying Model Strengths
Review False Positives to find cases where the model detected derivatives that keywords missed (potential improvements).

### 3. Understanding Limitations
Review False Negatives to understand where the model struggles and whether keyword search is still needed as a supplement.

### 4. Expanded Coverage
Use All Derivatives workbooks to analyze derivative liabilities and embedded derivatives not captured by original keyword search.

### 5. Longitudinal Analysis
Compare current-only vs. current+historic workbooks to understand the value of including historical context in disclosures.

---

## Questions to Ask When Analyzing Results

1. **Is the model accurate enough for my use case?** Check overall accuracy metrics.
2. **What am I gaining by using the model?** Review False Positives to see new discoveries.
3. **What am I losing?** Review False Negatives to see missed cases.
4. **Should I use current-only or current+historic?** Compare improvement metrics.
5. **Do I need all derivatives or just hedges?** Decide between Hedges and All Derivatives workbooks.

---

## Tips for Use

- Create pivot tables by firm, year, or hedge type
- Compare model vs. keyword results for coverage gaps
- Identify firms transitioning between hedge types or ceasing activity
- Inspect embedded or liability-linked derivatives for risk context
- Review disagreement cases manually to assess whether model found genuine improvements

---

## Technical Notes

- **Data source**: Keyword data from original derivative CSV; Model predictions from sentence-level classification
- **Comparison basis**: Company-year (CIK-year) level aggregation
- **Time scope**: "Current" refers to current-year mentions; "Historic" includes past-year references
- **Missing data**: If a company-year appears in one dataset but not the other, it's treated as "no derivative use" for the missing dataset
- **Model training**: Fine-tuned on synthetically generated financial text (see Data Generation section)
- **Text extraction**: Regex-based filtering before model classification (see Text Extraction Methodology section)

---

## Summary

In simple terms:
- The model reads SEC filings, identifies hedge/derivative mentions, and classifies them
- Results are compiled into multiple structured Excel reports
- You can explore hedge trends, cross-type exposures, and evaluate keyword-based methods versus model accuracy
- The analysis provides both validation of existing methods and discovery of additional derivative disclosures
