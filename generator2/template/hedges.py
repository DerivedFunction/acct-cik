# Derivatives
derivative_template = {
    "IR_PLACEHOLDER": [
        "interest rate",
        "single currency basis",
        "pay-fixed, receive-floating interest rate",
        "pay-floating, receive-fixed interest rate",
        "forward starting interest rate",
        "Eurodollar",
        "SOFR",
        "LIBOR",
    ],
    "IR_STANDALONE": ["treasury rate lock agreement"],
    "IR_TYPES": [
        "swaps",
        "forward",
        "option",
        "forward contract",
        "agreement",
        "forward agreement",
        "swap agreement",
        "swap contract",
        "cap contract",
        "floor contract",
        "hedge agreement",
        "hedge contract",
        "future contract",
        "swaption",
        "cap",
        "floor",
        "collar",
        "future",
    ],
    "FX_STANDALONE": [
        "forward contract",
        "forward agreement",
        "forward rate agreement",
        "collar contract",
        "dollar call option",
    ],
    "FX_PLACEHOLDER": [
        "foreign exchange",
        "foreign currency",
        "foreign exchange currency",
        "currency",
        "forward currency",
        "forward foreign currency",
        "forward foreign exchange currency",
        "forward foreign exchange cross-currency",
        "cross-currency",
        "cross currency",
        "cross currency interest rate",
        "cross-currency interest rate",
        "foreign currency forward",
        "FX",
    ],
    "FX_TYPES": [
        "swap",
        "forward",
        "option",
        "future",
        "agreement",
        "contract",
        "cap",
        "floor",
        "call option",
        "put option",
        "put contract",
        "option contract",
        "futures contract",
        "collar",
        "collar agreement",
        "collar contract",
        "NDF",
    ],
    "CP_PLACEHOLDER": [
        "commodity price",
        "commodity-related",
    ],
    "CP_TYPES": [
        "swap",
        "forward",
        "option",
        "future",
        "agreement",
        "contract",
        "cap",
        "floor",
        "call option",
        "put option",
        "put contract",
        "option contract",
        "futures contract",
    ],
    "GEN_PLACEHOLDER": [
        "",
    ],
    "GEN_TYPES": [
        "equity swap",
        "swap",
        "future",
        "forward",
        "call option",
        "call contract",
        "put option",
        "put contract",
        "option contract",
        "forward contract",
        "futures contract",
        "swaption",
    ],
    "GEN_STANDALONE": [
        "purchased put option contracts",
        "collar strategies",
        "purchased call option contracts",
        "over-the-counter contract",
        "receive-equity return, pay-fixed equity swap",
        "receive-equity return, pay-floating equity swap",
        "equity collar",
        "total return swap",
    ],
}


# Base variables
hedge_types = [
    "cash flow",
    "fair value",
    "net investment",
]
hedge_metrics = [
    "changes in cash flows",
    "changes in fair value",
    "variability",
    "exposure",
]


hedge_mitigation_verbs = [
    "attempt",
    "seek",
    "pursue",
    "undertake",
]
hedge_may_mitigation_verbs = [
    "may attempt",
    "may seek",
    "may pursue",
    "may undertake",
]

hedge_use_verbs = [
    "entered into",
    "executed",
    "utilized",
    "employed",
    "used",
    "had",
    "reported",
    "maintained",
    "committed",
    "implemented",
    "applied",
    "engaged in",
    "pursued",
    "utilizes",
    "employs",
    "uses",
    "maintains",
    "has",
    "have",
    "applies",
    "reports",
]
hedge_may_use_verbs = [
    "may engage in",
    "may commit in",
    "may implement",
    "may enter into",
    "may utilize",
    "may employ",
    "may use",
    "may apply",
    "may have",
    "may pursue",
]

hedge_change_verbs = ["increase", "decrease", "affect", "impact"]

# Base sentence structures
base_structures = [
    "{prefix}, {company} {verb} {amount_swap_order} {hedge_designation}",
    "{prefix}, {amount_swap_order} {hedge_designation}",
    "{company} {verb} {amount_swap_order} {time_phrase} {hedge_designation}",
    "{company}'s {portfolio_term} {time_phrase} {portfolio_verb} {amount_swap_order}",
]

# Time prefix variations (single year)
time_prefixes = [
    "As of {month} {end_day}, {year}",
    "At year-end {year}",
    "As of {month} {year}",
    "At the end of {year}",
    "At the close of {year}",
    "During {month} {year}",
    "In {month} {year}",
    "In the {quarter} quarter of {year}",
    "During the {quarter} quarter of {year}",
]

# Two-year time prefixes
two_year_prefixes = [
    "At {month} {end_day}, {year} and {prev_year}",
    "As of {month} {end_day}, {year} and {prev_year}",
]

# Three-year time prefixes
three_year_prefixes = [
    "At {month} {end_day}, {year}, {prev_year}, and {prev2_year}",
    "As of {month} {end_day}, {year}, {prev_year}, and {prev2_year}",
]

# Amount connectors (words that connect amounts to swap types)
amount_connectors = [
    "with notional amounts totaling",
    "with notional amounts of",
    "with aggregate notional values of",
    "with a notional amount of",
    "totaling",
    "with notional values of",
]

# Amount patterns (order of amount vs swap)
amount_patterns = [
    "{swap_type} {connector} {currency_code}{notional} {money_unit}",
    "{connector} {currency_code}{notional} {money_unit} in {swap_type}",
]

# Two-year amount patterns
two_year_amount_patterns = [
    "{swap_type} {connector} {currency_code}{notional} {money_unit} and {currency_code}{prev_notional} {money_unit}, respectively",
    "{connector} {currency_code}{notional} {money_unit} and {currency_code}{prev_notional} {money_unit}, respectively, in {swap_type}",
]

# Three-year amount patterns
three_year_amount_patterns = [
    "{swap_type} {connector} {currency_code}{notional} {money_unit}, {currency_code}{prev_notional} {money_unit}, and {currency_code}{prev2_notional} {money_unit}, respectively",
    "{connector} {currency_code}{notional} {money_unit}, {currency_code}{prev_notional} {money_unit}, and {currency_code}{prev2_notional} {money_unit}, respectively, in {swap_type}",
]

# Hedge designation phrases (optional endings)
hedge_designations = [
    "",
    "designated as hedges",
    "designated as hedging instruments",
    "designated as {hedge_type} hedges",
    "used for hedging purposes",
    "remaining designated as hedges",
    "as part of its hedging strategy",
    "as part of its risk management strategy",
    "within its hedging program",
]

# Portfolio terms
portfolio_terms = [
    "derivative portfolio",
    "derivative instruments",
    "{swap_type} portfolio",
    "portfolio",
]

# Portfolio state verbs
portfolio_verbs = [
    "consists of",
    "includes",
    "included",
]

# Outstanding/active state descriptors
state_descriptors = [
    "outstanding",
    "active",
    "remaining",
    "",
]

# Special templates for historical/maturity disclosures
historical_templates = [
    "{company}'s {swap_type} contracted in {old_year} remain {state} as of {year}, with a notional balance of {currency_code}{old_notional} {money_unit}, scheduled to mature in {future_year}",
    "{company}'s notional balance of {currency_code}{old_notional} {money_unit} in {swap_type} contracted in {old_year} remains {state} as of {year}, scheduled to mature in {future_year}",
    "To manage exposure, {company} {verb} {swap_type} in {old_year}, with an inception notional of {currency_code}{old_notional} {money_unit} and a stated maturity in {future_year}",
    "To manage exposure, {company} {verb} notional amounts of {currency_code}{old_notional} {money_unit} in {swap_type} during {old_year}, with a stated maturity in {future_year}",
    "In {month} {old_year}, {company} {verb} {swap_type} with notional amounts of {currency_code}{old_notional} {money_unit}, which are set to expire in {month} {future_year}",
    "In {month} {old_year}, {company} {verb} notional amounts of {currency_code}{old_notional} {money_unit} in {swap_type}, which are set to expire in {month} {future_year}",
    "As of {month} {year}, {company} {verb} {swap_type} {verb} in {old_year}, with total notional of {currency_code}{old_notional} {money_unit}, expiring in {future_year}",
    "As of {month} {year}, {company} {verb} notional totals of {currency_code}{old_notional} {money_unit} in {swap_type} initiated in {old_year}, expiring in {future_year}",
    "{swap_type} expires in {future_year}",
]

# Generic accounting reasons (shared across all hedge types)
generic_accounting_reasons = [
    "resulting in {currency_code}{notional} {money_unit} of unrealized losses recorded in accumulated OCI",
    "resulting in fair value losses recorded in equity",
    "resulting in {currency_code}{notional} {money_unit} of unrealized gains recorded in accumulated OCI",
    "resulting in fair value gains recorded in equity",
    "with net unrealized losses of {currency_code}{notional} {money_unit} reflected in accumulated other comprehensive income",
    "with net unrealized gains of {currency_code}{notional} {money_unit} reflected in accumulated other comprehensive income",
    "leading to mark-to-market adjustments recorded in other comprehensive income",
    "with changes in fair value recognized in equity",
    "with changes in fair value recognized in earnings",
]

# Interest Rate (IR) specific accounting reasons
ir_specific_reasons = [
    "resulting in a decrease in interest expense of {currency_code}{notional} {money_unit}",
    "resulting in an increase in interest expense of {currency_code}{notional} {money_unit}",
    "effectively converting fixed-rate debt to floating-rate debt",
    "effectively converting floating-rate debt to fixed-rate debt",
    "designated as hedges of the notes with a notional amount of {currency_code}{notional} {money_unit}, effectively converting portions of fixed-rate debt to floating rates",
    "to modify the interest rate characteristics of outstanding senior notes",
    "designated as fair value hedges of fixed-rate obligations",
    "designated as hedging instruments against changes in the fair value of fixed-rate debt",
    "to hedge interest rate exposure on a portion of its debt portfolio",
    "to convert fixed-rate senior notes to variable rates",
    "to manage interest rate risk on long-term debt",
    "designated as fair value hedges for its outstanding bonds",
    "to adjust the interest rate profile of its debt",
    "to hedge changes in the fair value of fixed-rate liabilities",
    "to manage exposure to interest rate fluctuations",
    "designated to hedge fixed-rate debt obligations",
    "to modify the interest rate structure of its senior notes",
    "to hedge the fair value of outstanding debt",
    "to convert portions of its fixed-rate debt to floating rates",
    "designated as fair value hedges against changes in debt valuation",
    "to manage interest rate exposure on bonds",
    "to adjust the interest rate characteristics of long-term liabilities",
    "designated as hedges of fixed-rate note obligations",
    "to mitigate interest rate risk on debt issuances",
    "effectively convert the hedged portion of debt to floating rates",
    "designated as fair value hedges",
    "to manage debt-related interest rate risk",
    "hedging fixed-rate obligations",
    "designated as fair value hedges",
    "to convert fixed-rate debt to floating rates",
    "to hedge fixed-rate debt obligations",
    "scheduled to expire in {month} {future_year}",
    "to hedge debt obligations, with an initial notional of {currency_code}{old_notional} {money_unit}, maturing in {future_year}",
    "which carry notional amounts of {currency_code}{old_notional} {money_unit} and terminate in {future_year}",
    "with a starting notional value of {currency_code}{old_notional} {money_unit}, declining annually until expiration in {month} {future_year}",
    "to optimize the interest rate profile of its debt portfolio, converting portions of fixed-rate debt to floating-rate instruments",
    "to adjust the effective interest rate composition of outstanding debt",
    "to reduce interest rate volatility on its debt obligations",
    "to transform fixed-rate debt into variable-rate debt where appropriate",
    "to hedge against rising interest rates, modifying the interest rate characteristics of its borrowings",
    "to manage the interest rate exposure of its long-term debt portfolio",
    "to convert portions of debt into instruments with more favorable interest rate terms",
    "to balance fixed and floating rate obligations",
    "to manage cash flow risk",
    "to adjust the effective interest profile",
    "to limit the negative impact of interest rates",
    "to hedge against fluctuations in interest rates",
    "to manage exposure to changes in benchmark interest rates",
    "to reduce cash flow variability from interest-bearing debt",
    "to stabilize the cost of borrowing",
    "to protect against unfavorable changes in long-term debt obligations",
    "to hedge interest rate risk on forecasted debt issuances",
    "designated as {hedge_type} hedges to hedge against changes in interest rates that could impact expected future issuances of debt",
    "designated as {hedge_type} hedges to lock in favorable interest rates prior to anticipated debt issuances",
    "designated as {hedge_type} hedges to hedge interest rate exposure on forecasted debt offerings",
    "to mitigate the risk of rising interest rates on planned fixed-rate debt issuances",
    "as {hedge_type} hedges to secure interest rates for future debt issuances",
    "may designate as {hedge_type} hedges to manage interest rate risk",
    "to protect against interest rate volatility for planned fixed-rate debt issuances",
    "as {hedge_type} hedges to lock in rates for anticipated debt financings",
    "designated as {hedge_type} hedges to stabilize future interest costs",
    "to mitigate interest rate fluctuations on planned debt offerings",
    "designated as {hedge_type} hedges to secure rates for future fixed-rate debt",
    "to manage interest rate exposure for anticipated debt issuances",
    "as {hedge_type} hedges to lock in rates prior to debt financings",
    "to hedge against rising interest rates for planned debt issuances",
    "designates as {hedge_type} hedges in preparation for fixed-rate debt",
    "to stabilize interest rates for forecasted bond issuances",
    "implemented as {hedge_type} hedges to manage risk on future debt offerings",
    "to secure favorable rates for anticipated fixed-rate debt",
    "designates as {hedge_type} hedges to mitigate interest rate risk on planned financings",
    "with quarterly settlements based on the differential between fixed and floating rates on notional amounts",
    "converting floating rate exposure to fixed rates, with quarterly exchange of payment differentials based on notional values",
    "with quarterly net settlements calculated on agreed notional principal amounts",
    "to limit the impact of interest rate changes on earnings and cash flows, and to lower overall borrowing costs",
    "to borrow at fixed rates when it believes it is in its best interests to do so, and may enter into derivative financial instruments, such as {swap_types}, in order to limit its exposure to interest rate fluctuations",
    "to manage variable interest rate exposure over a medium- to long-term period",
    "exposed to interest rate risk associated with fluctuations in interest rates on variable rate debt",
    "recognize the gains and losses on derivative instruments as an adjustment to interest expense in the period the hedged interest payment affects earnings",
    "manage interest costs by using a mix of fixed- and floating-rate debt",
    "to manage variable interest rate exposure",
    "expose to the risk of increased interest expense if short-term interest rates rise",
]

# Foreign Exchange (FX) specific accounting reasons
fx_specific_reasons = [
    "offsetting foreign currency translation adjustments",
    "mitigating exchange rate fluctuations on foreign currency denominated transactions",
    "with translation gains of {currency_code}{notional} {money_unit} recognized in other comprehensive income",
    "with translation losses of {currency_code}{notional} {money_unit} recognized in other comprehensive income",
    "hedging net investment in foreign operations",
]

# Equity (EQ) specific accounting reasons
eq_specific_reasons = [
    "offsetting market value changes in the underlying equity positions",
    "mitigating exposure to equity market volatility",
    "offsetting losses on equity investments",
    "offsetting gains on equity investments",
]

# Commodity Price (CP) specific accounting reasons
cp_specific_reasons = [
    "offsetting commodity price fluctuations",
    "mitigating exposure to volatile commodity prices",
    "stabilizing cost of goods sold despite commodity price movements",
    "hedging against increases in raw material costs",
    "hedging against decreases in commodity sale prices",
]

# Special templates for accounting impact
accounting_impact_templates = [
    "{time_prefix}, {swap_type} were designated as {hedge_type} hedges, {reason}",
    "{time_prefix}, {company} {verb} {swap_type} with a total notional amount of {currency_code}{notional} {money_unit}, {reason}",
    "The net unrealized loss on the {swap_type} was {currency_code}{notional} {money_unit} at {month} {end_day}, {year} and is reflected in accumulated other comprehensive income",
    "The net unrealized gain on the {swap_type} was {currency_code}{notional} {money_unit} at {month} {end_day}, {year} and is reflected in accumulated other comprehensive income",
]

# No-prior-year patterns (two-year)
two_year_no_prior_patterns = [
    "no such instruments were outstanding at {prev_year}",
    "while no comparable {swap_type} existed during {prev_year}",
    "There were no {swap_type} outstanding at the close of {prev_year}",
    "there were no such {swap_type} reported in {prev_year}",
    "with no comparable {swap_type} outstanding in {prev_year}",
    "with no {swap_type} outstanding during {prev_year}",
    "no {swap_type} remained outstanding at the end of {prev_year}",
    "There were no outstanding {swap_type} balances at {prev_year}",
]

# No-prior-year patterns (three-year)
three_year_no_prior_patterns = [
    "no such instruments were outstanding at {prev_year} or {prev2_year}",
    "while no comparable {swap_type} existed during {prev_year} or {prev2_year}",
    "There were no {swap_type} outstanding at the close of {prev_year} or {prev2_year}",
    "there were no such {swap_type} reported in {prev_year} or {prev2_year}",
    "with no comparable {swap_type} outstanding in {prev_year} or {prev2_year}",
    "with no {swap_type} outstanding during {prev_year} or {prev2_year}",
    "no {swap_type} remained outstanding at the end of {prev_year} or {prev2_year}",
    "There were no outstanding {swap_type} balances at {prev_year} or {prev2_year}",
]

# Special templates for no-prior-year disclosures (two-year)
two_year_no_prior_templates = [
    "At {month} {end_day}, {year}, {company} {verb} {swap_type} totaling {currency_code}{notional} {money_unit}; {no_prior_pattern}",
    "As of {month} {end_day}, {year}, {company} {verb} active {swap_type} with a notional value of {currency_code}{notional} {money_unit}, {no_prior_pattern}",
    "At year-end {year}, {company}'s {swap_type} totaled {currency_code}{notional} {money_unit}. {no_prior_pattern}",
    "As of {month} {year}, {company} {verb} {swap_type} with notional amounts of {currency_code}{notional} {money_unit}; {no_prior_pattern}",
    "During {year}, {company} {verb} {swap_type} positions totaling {currency_code}{notional} {money_unit}, {no_prior_pattern}",
    "During {year}, {company} initiated {swap_type} positions totaling {currency_code}{notional} {money_unit}, {no_prior_pattern}",
    "At {month} {end_day}, {year}, {company} {verb} {swap_type} serving as fair value hedges, {no_prior_pattern}",
    "As of {month} {end_day}, {year}, {company} {verb} {swap_type} notional of {currency_code}{notional} {money_unit}; {no_prior_pattern}",
]

# Special templates for no-prior-year disclosures (three-year)
three_year_no_prior_templates = [
    "At {month} {end_day}, {year}, {company} {verb} {swap_type} totaling {currency_code}{notional} {money_unit}; {no_prior_pattern}",
    "As of {month} {end_day}, {year}, {company} had active {swap_type} with a notional value of {currency_code}{notional} {money_unit}, {no_prior_pattern}",
    "At year-end {year}, {company}'s {swap_type} totaled {currency_code}{notional} {money_unit}. {no_prior_pattern}",
    "As of {month} {year}, {company} {verb} {swap_type} with notional amounts of {currency_code}{notional} {money_unit}; {no_prior_pattern}",
    "During {year}, {company} initiated {swap_type} positions totaling {currency_code}{notional} {money_unit}, {no_prior_pattern}",
    "At {month} {end_day}, {year}, {company} {verb} {swap_type} serving as fair value hedges, {no_prior_pattern}",
    "As of {month} {end_day}, {year}, {company} {verb} {swap_type} notional of {currency_code}{notional} {money_unit}; {no_prior_pattern}",
    "At {month} {end_day}, {year}, {company} {verb} {swap_type} totaling {currency_code}{notional} {money_unit}. {no_prior_pattern}",
]

# ==============================================================================
# HEDGE TRANSACTION TEMPLATE SYSTEM
# ==============================================================================

# ------------------------------------------------------------------------------
# OPTIONAL/COMPARATIVE TEMPLATES (Two-Year Comparisons)
# ------------------------------------------------------------------------------

# Comparison verbs/phrases
comparison_phrases = [
    "compared to",
    "versus",
    "down from",
    "reduced from",
]

# Trend descriptors
trend_descriptors = [
    "with notional amounts decreasing from",
    "with notional amounts increasing from",
    "with notional values of",
    "had a notional value of",
]

# Optional hedge purposes
optional_purposes = [
    "to hedge forecasted revenue which were not part of a collar strategy",
    "to hedge forecasted transactions",
    "to hedge revenue streams",
    "for hedging forecasted revenue",
    "for transaction hedging",
    "for revenue hedging",
    "for hedging",
]

# Base optional template patterns
optional_template_patterns = [
    "{{company}} also have {{verb}} {{swap_type}} {purpose}. Such {{swap_type}} had a notional value of {{currency_code}}{{notional1}} {{money_unit}} and {{currency_code}}{{notional2}} {{money_unit}} as of {{month}} {{end_day}}, {{year}} and {{month}} {{end_day}}, {{prev_year}}, respectively",
    "{{company}} {{verb}} {{swap_type}} with notional values of {{currency_code}}{{notional1}} {{money_unit}} as of {{month}} {{end_day}}, {{year}} {comparison} {{currency_code}}{{notional2}} {{money_unit}} as of {{month}} {{end_day}}, {{prev_year}}",
    "As of {{month}} {{end_day}}, {{year}}, {{company}} {{verb}} {{swap_type}} with a notional value of {{currency_code}}{{notional1}} {{money_unit}}, {comparison} {{currency_code}}{{notional2}} {{money_unit}} in the prior year",
    "{{company}} {{verb}} {{swap_type}} {purpose}, {trend} {{currency_code}}{{notional2}} {{money_unit}} as of {{month}} {{end_day}}, {{prev_year}} to {{currency_code}}{{notional1}} {{money_unit}} as of {{month}} {{end_day}}, {{year}}",
    "As of {{month}} {{end_day}}, {{year}}, {{swap_type}} with a notional value of {{currency_code}}{{notional1}} {{money_unit}} were in place, {comparison} {{currency_code}}{{notional2}} {{money_unit}} as of {{month}} {{end_day}}, {{prev_year}}",
    "In {{year}}, {{swap_type}} with a notional value of {{currency_code}}{{notional1}} {{money_unit}} were active, {comparison} {{currency_code}}{{notional2}} {{money_unit}} in {{prev_year}}",
    "As of {{month}} {{end_day}}, {{year}}, {{company}}'s {{swap_type}} portfolio had a notional value of {{currency_code}}{{notional1}} {{money_unit}}, {comparison} {{currency_code}}{{notional2}} {{money_unit}} in {{prev_year}}",
    "At year-end {{year}}, {{swap_type}} with a notional amount of {{currency_code}}{{notional1}} {{money_unit}} were {{verb}} {purpose}, {comparison} {{currency_code}}{{notional2}} {{money_unit}} in {{prev_year}}",
]

# ------------------------------------------------------------------------------
# SHARED TIMING COMPONENTS (Used across all events: termination, expiration, dedesignation, settlement)
# ------------------------------------------------------------------------------

# Time periods
time_periods = [
    "In the {{quarter}} quarter of {{year}}",
    "During the {{quarter}} quarter of {{year}}",
    "In {{month}} {{year}}",
    "During {{month}} {{year}}",
    "In {{year}}",
    "During {{year}}",
    "prior to {{month}} {{end_day}}, {{year}}",
    "prior to year-end {{year}}",
    "As of {{month}} {{end_day}}, {{year}}",
]

# Action verbs (shared across all events)
action_verbs = [
    "terminated",
    "settled",
    "closed out",
    "ended",
    "unwound",
    "expired",
    "matured",
    "reached maturity",
    "reached their expiration date",
    "liquidated",
]

# Settlement frequencies
settlement_frequencies = [
    "quarterly",
    "annually",
    "monthly",
    "semi-annually",
]

# Settlement result phrases
settlement_results = [
    "with all gains and losses recognized upon payment",
    "with the resulting gains and losses fully recorded",
    "and all gains and losses are realized as they occur",
    "with all resulting gains and losses reflected in earnings",
    "ensuring that all gains and losses are recognized at the time of settlement",
    "result in full recognition of realized gains and losses",
    "and all associated gains and losses are recorded when realized",
    "with realized gains and losses recorded accordingly",
]

# Result phrases - no outstanding positions (shared)
no_position_results = [
    "{{company}} {{verb}} no outstanding derivative positions as of year-end {{year}}",
    "resulting in no outstanding hedge positions as of {{month}} {{end_day}}, {{year}}",
    "with no derivative instruments remaining at period end",
    "leaving no active derivative positions at year-end",
    "resulting in no active hedges as of {{month}} {{end_day}}, {{year}}",
    "leaving no derivative instruments outstanding",
    "with no remaining hedge positions at year-end {{year}}",
    "resulting in no active derivative contracts at period end",
    "leaving no outstanding hedges as of {{month}} {{end_day}}, {{year}}",
    "with no derivative positions remaining at year-end",
    "resulting in no active hedges at period end",
    "with no hedges remaining at year-end",
    "resulting in no outstanding derivative instruments",
    "leaving no active derivative positions",
    "with no hedges in place at {{month}} {{end_day}}, {{year}}",
    "with no derivatives outstanding at year-end",
    "resulting in no active hedge positions",
    "leaving no derivative contracts at period end",
    "with no outstanding hedges as of {{month}} {{end_day}}, {{year}}",
    "there were no such {{swap_type}} outstanding",
]

# No-replacement phrases (for expirations specifically)
no_replacement_phrases = [
    "with no new positions {{verb}} during the year",
    "with no replacement hedges executed during the remainder of the fiscal year",
    "and {{company}} elected not to enter into new derivative contracts during the period",
    "and no new hedging instruments were established for the fiscal year",
    "with no new derivative positions initiated",
    "with no new hedges entered during the year",
    "and {{company}} did not execute new derivative contracts",
    "with no replacement hedges established",
    "and no new derivative instruments were {{verb}} during the fiscal year",
    "with no new positions taken",
    "and {{company}} chose not to initiate new hedges",
    "with no new derivative contracts executed",
    "leaving no active hedges for the remainder of the year",
    "with no new hedges established",
    "with no new positions entered",
    "and {{company}} did not replace them with new hedges",
    "with no new derivative contracts initiated",
    "and no further hedging instruments were established",
    "with no new hedges entered into",
    "with no new contracts {{verb}}",
]

# De-designation specific actions
dedesignation_actions = [
    "de-designated",
    "discontinued hedge accounting for",
    "removed hedge designation from",
    "ceased hedge accounting for",
    "ended hedge accounting for",
    "removed hedge accounting from",
    "ceased applying hedge accounting to",
]

# De-designation results (in addition to shared no_position_results)
dedesignation_specific_results = [
    "removing hedge accounting treatment for these instruments",
    "discontinuing hedge accounting",
    "with no hedge accounting applied at year-end",
    "removing their hedge accounting status",
    "ending their hedge accounting status",
]

# All event results (combined settlement_results, no_position_results, dedesignation_specific_results)
all_event_results = settlement_results + no_position_results + dedesignation_specific_results

# Merged event template patterns (termination, expiration, dedesignation, settlement)
merged_event_patterns = [
    # Termination patterns
    "{time_period}, {{company}} {action_verb} all remaining {{swap_type}} agreements. {result}",
    "{time_period}, all previously designated {{swap_type}} were {action_verb}, {result}",
    "{{company}} {action_verb} all {{swap_type}} positions {time_period}, {result}",
    "All outstanding {{swap_type}} matured or were {action_verb} {time_period}, {result}",
    "{time_period}, {{company}} {action_verb} all {{swap_type}} agreements, {result}",
    "{time_period}, {{company}} {action_verb} {{swap_type}} positions, {result}",
    "{time_period}, all {{swap_type}} were {action_verb}, {result}",
    "{{company}} {action_verb} all outstanding {{swap_type}} {time_period}, {result}",
    "{time_period}, {{company}} {action_verb} its {{swap_type}} portfolio, {result}",
    "{time_period}, all {{swap_type}} agreements were {action_verb}, {result}",
    "As of {{month}} {{end_day}}, {{year}}, there were no such {{swap_type}} outstanding",
    # Expiration patterns
    "All previously outstanding derivatives {action_verb} {time_period}, {no_replacement}",
    "{{company}}'s derivative portfolio was fully {action_verb} {time_period} {no_replacement}",
    "Outstanding hedge positions {action_verb} throughout {{year}}, {no_replacement}",
    "{time_period}, all existing {{swap_type}} {action_verb}, {no_replacement}",
    "{time_period}, all {{swap_type}} contracts {action_verb}, {no_replacement}",
    "{{company}}'s {{swap_type}} portfolio fully {action_verb} {time_period}, {no_replacement}",
    "{time_period}, all outstanding {{swap_type}} {action_verb}, {no_replacement}",
    "{time_period}, {{company}}'s {{swap_type}} positions {action_verb}, {no_replacement}",
    "All {{swap_type}} {action_verb} {time_period}, {no_replacement}",
    "{time_period}, {{company}}'s derivative portfolio of {{swap_type}} was fully settled, {no_replacement}",
    # De-designation patterns
    "{{company}} {dedesignation_action} all of our {{swap_type}} {time_period}",
    "{{company}} {dedesignation_action} {{swap_type}} {time_period}, {result}",
    "All {{swap_type}} were {dedesignation_action} as hedging instruments {time_period}",
    "{time_period}, {{company}} {dedesignation_action} all outstanding {{swap_type}}",
    "{time_period}, all {{swap_type}} were {dedesignation_action}, {result}",
    "All {{swap_type}} were {dedesignation_action} {time_period}, {result}",
    "{time_period}, all {{swap_type}} lost their hedge designation status",
    # Settlement patterns (merged)
    "Under each {{swap_type}}, settlements occur {frequency} for {{currency_code}}{{notional}} {{money_unit}}, {result}",
    "Each {{swap_type}} settles {frequency} for {{currency_code}}{{notional}} {{money_unit}}, {result}",
    "{frequency_cap} payments of {{currency_code}}{{notional}} {{money_unit}} are required under each {{swap_type}}, {result}",
    "For every {{swap_type}}, {frequency} payments of {{currency_code}}{{notional}} {{money_unit}} are made, {result}",
    "Each {{swap_type}} involves {frequency} settlements of {{currency_code}}{{notional}} {{money_unit}}, {result}",
    "{frequency_cap} settlements under each {{swap_type}} for {{currency_code}}{{notional}} {{money_unit}} {result}",
    "Each {{swap_type}} calls for {frequency} payments of {{currency_code}}{{notional}} {{money_unit}}, {result}",
    "Each {{swap_type}} entails {frequency} settlement of {{currency_code}}{{notional}} {{money_unit}}, {result}",
    # Quarterly termination with settlement patterns
    "{time_period}, {{company}} {action_verb} {{swap_type}} with {frequency} settlements, {result}",
    "{time_period}, all {{swap_type}} were {action_verb} {frequency}, {result}",
    "{{company}} conducted {frequency} {action_verb} of {{swap_type}} {time_period}, {result}",
]



# ==============================================================================
# TEMPLATE GENERATION FUNCTIONS
# ==============================================================================


def to_sentence_case(text):
    """Convert text to sentence case."""
    if not text.strip():
        return text
    result = []
    prev_non_space = None
    for char in text:
        if char.isspace():
            result.append(char)
            continue
        if char.isalpha():
            if prev_non_space == "." or prev_non_space is None:
                result.append(char.upper())
            else:
                result.append(char.lower())
        else:
            result.append(char)
        prev_non_space = char
    return "".join(result)


def generate_optional_templates():
    """Generate all optional/comparative templates."""
    templates = []
    for pattern in optional_template_patterns:
        if "{comparison}" in pattern:
            for comparison in comparison_phrases:
                temp = pattern.replace("{comparison}", comparison)
                templates.append(to_sentence_case(temp))
        elif "{trend}" in pattern:
            for trend in trend_descriptors:
                temp = pattern.replace("{trend}", trend)
                templates.append(to_sentence_case(temp))
        elif "{purpose}" in pattern:
            for purpose in optional_purposes:
                temp = pattern.replace("{purpose}", purpose)
                templates.append(to_sentence_case(temp))
        else:
            templates.append(to_sentence_case(pattern))
    return templates


def generate_event_templates():
    """Generate all merged event templates (termination, expiration, dedesignation, settlement)."""
    templates = []
    for pattern in merged_event_patterns:
        # Common replacements
        if "{time_period}" in pattern:
            for time in time_periods:
                temp = pattern.replace("{time_period}", time)
                expanded = _expand_pattern(temp)
                templates.extend([to_sentence_case(t) for t in expanded])
        elif "{action_verb}" in pattern:
            for action in action_verbs:
                temp = pattern.replace("{action_verb}", action)
                expanded = _expand_pattern(temp)
                templates.extend([to_sentence_case(t) for t in expanded])
        elif "{no_replacement}" in pattern:
            for no_rep in no_replacement_phrases:
                temp = pattern.replace("{no_replacement}", no_rep)
                expanded = _expand_pattern(temp)
                templates.extend([to_sentence_case(t) for t in expanded])
        elif "{dedesignation_action}" in pattern:
            for ded_act in dedesignation_actions:
                temp = pattern.replace("{dedesignation_action}", ded_act)
                expanded = _expand_pattern(temp)
                templates.extend([to_sentence_case(t) for t in expanded])
        elif "{frequency}" in pattern:
            for freq in settlement_frequencies:
                temp = pattern.replace("{frequency}", freq)
                temp = temp.replace("{frequency_cap}", freq.capitalize())
                expanded = _expand_pattern(temp)
                templates.extend([to_sentence_case(t) for t in expanded])
        else:
            expanded = _expand_pattern(pattern)
            templates.extend([to_sentence_case(t) for t in expanded])
    return templates


def _expand_pattern(pattern):
    """Helper to expand common placeholders like {result}."""
    expanded = []
    if "{result}" in pattern:
        for result in all_event_results:
            expanded.append(pattern.replace("{result}", result))
    else:
        expanded.append(pattern)
    return expanded


def generate_hedge_position_templates(hedge_type="gen"):
    """
    Generate all template combinations for a specific hedge type.

    Args:
        hedge_type: One of "ir", "fx", "eq", "cp", "gen"

    Returns:
        List of all generated templates
    """
    # Select appropriate accounting reasons based on hedge type
    accounting_reasons_map = {
        "ir": generic_accounting_reasons + ir_specific_reasons,
        "fx": generic_accounting_reasons + fx_specific_reasons,
        "eq": generic_accounting_reasons + eq_specific_reasons,
        "cp": generic_accounting_reasons + cp_specific_reasons,
        "gen": generic_accounting_reasons,
    }
    accounting_reasons = accounting_reasons_map.get(
        hedge_type.lower(), generic_accounting_reasons
    )

    templates = []

    # Generate single-year amount_swap_orders from patterns and connectors
    amount_swap_orders = []
    for pattern in amount_patterns:
        for connector in amount_connectors:
            amount_swap_orders.append(
                to_sentence_case(pattern.replace("{connector}", connector))
            )

    # Generate two-year amounts from patterns and connectors
    two_year_amounts = []
    for pattern in two_year_amount_patterns:
        for connector in amount_connectors:
            two_year_amounts.append(
                to_sentence_case(pattern.replace("{connector}", connector))
            )

    # Generate three-year amounts from patterns and connectors
    three_year_amounts = []
    for pattern in three_year_amount_patterns:
        for connector in amount_connectors:
            three_year_amounts.append(
                to_sentence_case(pattern.replace("{connector}", connector))
            )

    # Single-year templates
    for prefix in time_prefixes:
        for amount_order in amount_swap_orders:
            for designation in hedge_designations:
                full = (
                    f"{prefix}, {{company}} {{verb}} {amount_order} {designation}"
                    if designation
                    else f"{prefix}, {{company}} {{verb}} {amount_order}"
                )
                templates.append(to_sentence_case(full))

    # Two-year templates
    for prefix in two_year_prefixes:
        for amount_order in two_year_amounts:
            for designation in hedge_designations:
                full = (
                    f"{prefix}, {{company}} {{verb}} {amount_order} {designation}"
                    if designation
                    else f"{prefix}, {{company}} {{verb}} {amount_order}"
                )
                templates.append(to_sentence_case(full))

    # Three-year templates
    for prefix in three_year_prefixes:
        for amount_order in three_year_amounts:
            for designation in hedge_designations:
                full = (
                    f"{prefix}, {{company}} {{verb}} {amount_order} {designation}"
                    if designation
                    else f"{prefix}, {{company}} {{verb}} {amount_order}"
                )
                templates.append(to_sentence_case(full))

    # Historical templates with state descriptors
    for template in historical_templates:
        if "{state}" in template:
            for state in state_descriptors:
                if state:
                    full = template.replace("{state}", state)
                    templates.append(to_sentence_case(full))
        else:
            templates.append(to_sentence_case(template))

    # Accounting impact templates with hedge-type-specific reasons
    for template in accounting_impact_templates:
        if "{reason}" in template:
            for reason in accounting_reasons:
                full = template.replace("{reason}", reason)
                templates.append(to_sentence_case(full))
        else:
            templates.append(to_sentence_case(template))

    # Two-year no-prior-year templates with patterns
    for template in two_year_no_prior_templates:
        for pattern in two_year_no_prior_patterns:
            full = template.replace("{no_prior_pattern}", pattern)
            templates.append(to_sentence_case(full))

    # Three-year no-prior-year templates with patterns
    for template in three_year_no_prior_templates:
        for pattern in three_year_no_prior_patterns:
            full = template.replace("{no_prior_pattern}", pattern)
            templates.append(to_sentence_case(full))

    return templates


# Create a final output
def expand_derivative_terms(placeholders, types, standalone):
    """
    Combine placeholders with types (if any) and add standalone terms.
    Returns a flat list of derivative keyword strings.
    """
    results = []
    for ph in placeholders:
        for t in types:
            results.append(f"{ph} {t}".strip())
    results.extend(standalone)
    return sorted(set(results))


derivative_keywords = {
    "ir": expand_derivative_terms(
        derivative_template["IR_PLACEHOLDER"],
        derivative_template["IR_TYPES"],
        derivative_template["IR_STANDALONE"],
    ),
    "fx": expand_derivative_terms(
        derivative_template["FX_PLACEHOLDER"],
        derivative_template["FX_TYPES"],
        derivative_template["FX_STANDALONE"],
    ),
    "cp": expand_derivative_terms(
        derivative_template["CP_PLACEHOLDER"], derivative_template["CP_TYPES"], []
    ),
    "gen": expand_derivative_terms(
        derivative_template["GEN_PLACEHOLDER"],
        derivative_template["GEN_TYPES"],
        derivative_template["GEN_STANDALONE"],
    ),
}

ir_position_templates = generate_hedge_position_templates("ir")
fx_position_templates = generate_hedge_position_templates("fx")
cp_position_templates = generate_hedge_position_templates("cp")
eq_position_templates = generate_hedge_position_templates("eq")
gen_position_templates = generate_hedge_position_templates("gen")
