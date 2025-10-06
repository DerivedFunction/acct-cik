# Keyword vs Model Analysis Workbooks - User Guide

## Overview

This analysis compares two methods of identifying companies that use derivatives:
1. **Keyword Search Method**: The original approach using keyword matching in 10-K filings
2. **Machine Learning Model**: A trained classifier that analyzes sentence-level context

Four Excel workbooks are generated to help you understand how well the model performs and where it differs from the keyword approach.

---

## The Four Workbooks

### 1. `keywords_comparison_HEDGES_CURRENT.xlsx`
**Focus**: Current-year hedging activities only (IR, FX, CP)

Compares the model's detection of current hedging against keyword-based results.

### 2. `keywords_comparison_HEDGES_ALL.xlsx`
**Focus**: Current + historic hedging activities (IR, FX, CP)

Shows how including historical hedge mentions improves detection accuracy.

### 3. `keywords_comp_ALL_DERIVATIVES_CURRENT.xlsx`
**Focus**: All current derivatives (hedges + liabilities + embedded derivatives)

Broader view that includes derivative liabilities and embedded derivatives beyond just hedges.

### 4. `keywords_comp_ALL_DERIVATIVES_FULL.xlsx`
**Focus**: All derivatives, current + historic

The most comprehensive view, including all derivative types across time periods.

---

## Understanding the Sheets

### Sheet 1: KW_Model_Comparison
**What it shows**: High-level performance comparison between current-only and current+historic approaches.

**Key metrics**:
- **Accuracy**: Overall percentage of correct classifications (both agreements and disagreements)
- **Precision**: When the model says "yes," how often is it correct?
- **Recall**: Of all the companies that should be identified, how many did the model find?
- **F1 Score**: Balanced measure combining precision and recall
- **Improvement**: How much better current+historic performs vs. current-only

**How to read it**: Positive improvements indicate that including historic data improves model performance.

---

### Sheet 2: Summary_Current_Only (or Summary_Curr_Historic)
**What it shows**: Detailed performance metrics for each category.

**Categories**:
- **Overall**: Either "Hedges Only" (IR/FX/CP) or "All Derivatives" (including liabilities/embedded)
- **Foreign Exchange (FX)**: Currency hedging
- **Interest Rate (IR)**: Interest rate hedging
- **Commodity Price (CP)**: Commodity price hedging

**Metrics explained**:
- **True Positives (TP)**: Model and keywords both say "yes" (agreement on derivative use)
- **False Positives (FP)**: Model says "yes," keywords say "no" (model found something keywords missed)
- **True Negatives (TN)**: Model and keywords both say "no" (agreement on no derivative use)
- **False Negatives (FN)**: Model says "no," keywords say "yes" (model missed something)
- **Total**: Total number of company-year observations
- **Accuracy**: (TP + TN) / Total × 100
- **Precision**: TP / (TP + FP) × 100
- **Recall**: TP / (TP + FN) × 100
- **F1_Score**: Harmonic mean of precision and recall
- **Agreement_Rate**: Same as accuracy (percentage of times they agree)

**How to interpret**:
- **High accuracy** (>90%): Strong agreement between methods
- **High precision**: Model rarely identifies false positives
- **High recall**: Model catches most of what keywords catch
- **High F1**: Balanced performance

---

### Sheet 3: Detailed_Current_Only (or Detailed_Curr_Historic)
**What it shows**: Row-by-row comparison for every company-year observation.

**Columns**:
- **cik, year**: Company identifier and fiscal year
- **keyword_user, keyword_fx, keyword_ir, keyword_cp**: Did keywords find it? (1=yes, 0=no)
- **model_user_current, model_fx_current, etc.**: Did the model find it? (1=yes, 0=no)
- **overall_agree, fx_agree, ir_agree, cp_agree**: Do they agree? (1=yes, 0=no)
- **overall_classification**: 
  - *True Positive*: Both say derivative user
  - *True Negative*: Both say non-user
  - *False Positive*: Model says user, keywords say non-user
  - *False Negative*: Model says non-user, keywords say user

**Use case**: Drill down into specific disagreements to understand where and why the methods differ.

---

### Sheet 4: Basic_Current_Only (or Basic_Curr_Historic)
**What it shows**: Raw comparison data without additional classification columns.

**Use case**: Export this data for custom analysis or integration with other datasets.

---

### Sheet 5-8: Confusion Matrices
**What it shows**: 2x2 tables showing agreement/disagreement patterns.

**Structure**:
```
                    Model_No    Model_Yes
Keyword_No          TN          FP
Keyword_Yes         FN          TP
```

**Where**:
- **Top-left (TN)**: Both methods agree there's no derivative use
- **Top-right (FP)**: Model found it, keywords didn't (possible improvement)
- **Bottom-left (FN)**: Keywords found it, model didn't (potential miss)
- **Bottom-right (TP)**: Both methods agree on derivative use

**Four matrices provided**:
1. **Confusion_Overall**: Overall hedge or derivative use
2. **Confusion_FX**: Foreign exchange hedging
3. **Confusion_IR**: Interest rate hedging
4. **Confusion_CP**: Commodity price hedging

**How to interpret**:
- Large **TP and TN** values = Strong agreement
- Large **FP** values = Model is more sensitive (finds more cases)
- Large **FN** values = Keywords are more sensitive (or model is missing cases)

---

### Sheet 9: ModelOnly_Liab_Embed (All Derivatives workbooks only)
**What it shows**: Statistics for derivative types not covered by keyword search.

**Categories**:
- **Derivative Liabilities/Warrants**: Financial obligations and warrants
- **Embedded Derivatives**: Derivatives embedded in other contracts

**Metrics**:
- **Total**: Number of company-year observations
- **Model_Positive**: Number identified by model
- **Model_Negative**: Number not identified
- **Positive_Rate**: Percentage identified

**Important**: These categories have no keyword comparison because the original keyword search didn't target them. This shows additional value the model provides.

---

## Key Differences Between Workbooks

| Aspect | Hedges Workbooks | All Derivatives Workbooks |
|--------|------------------|---------------------------|
| **Overall category** | IR + FX + CP hedges only | Hedges + Liabilities + Embedded |
| **Scope** | Focused on hedging activities | Comprehensive derivative coverage |
| **Comparison validity** | Direct comparison to keywords | Partial comparison (hedges only) |
| **Extra insights** | None | ModelOnly_Liab_Embed sheet |

---

## How Scores Are Calculated

### Accuracy
Percentage of correct predictions (agreements):
```
Accuracy = (True Positives + True Negatives) / Total Observations × 100
```

### Precision
When the model predicts "derivative user," how often is it correct?
```
Precision = True Positives / (True Positives + False Positives) × 100
```

### Recall (Sensitivity)
Of all actual derivative users (per keywords), what percentage did the model find?
```
Recall = True Positives / (True Positives + False Negatives) × 100
```

### F1 Score
Balanced measure combining precision and recall:
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

**Why it matters**: High F1 means the model is both precise and comprehensive.

---

## Interpreting Results

### High Agreement (Accuracy > 90%)
The model and keywords largely agree. The model is a reliable alternative to keyword searching.

### High Precision, Lower Recall
Model is conservative. It rarely makes mistakes but might miss some cases. Review False Negatives to understand what was missed.

### Lower Precision, High Recall
Model is aggressive. It catches more cases but may have more false alarms. Review False Positives to see if they're genuine improvements or errors.

### Improvement from Current to Current+Historic
Positive improvements show that including historical mentions enhances detection. This is especially valuable for companies that discuss past derivative use.

---

## Practical Applications

### 1. Research Validation
Use the workbooks to validate whether keyword-based findings align with contextual model predictions.

### 2. Identifying Model Strengths
Review False Positives to find cases where the model detected derivatives that keywords missed (potential improvements).

### 3. Understanding Limitations
Review False Negatives to understand where the model struggles and whether keyword search is still needed.

### 4. Expanded Coverage
Use All Derivatives workbooks to analyze derivative liabilities and embedded derivatives not captured by original keyword search.

### 5. Longitudinal Analysis
Compare current-only vs. current+historic workbooks to understand the value of including historical context.

---

## Questions to Ask

1. **Is the model accurate enough for my use case?** Check overall accuracy metrics.
2. **What am I gaining by using the model?** Review False Positives to see new discoveries.
3. **What am I losing?** Review False Negatives to see missed cases.
4. **Should I use current-only or current+historic?** Compare improvement metrics.
5. **Do I need all derivatives or just hedges?** Decide between Hedges and All Derivatives workbooks.

---

## Technical Notes

- **Data source**: Keyword data from original derivative CSV; Model predictions from sentence-level classification
- **Comparison basis**: Company-year (CIK-year) level aggregation
- **Time scope**: Current refers to current-year mentions; Historic includes past-year references
- **Missing data**: If a company-year appears in one dataset but not the other, it's treated as "no derivative use" for the missing dataset