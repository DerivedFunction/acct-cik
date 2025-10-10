import itertools

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
hedge_types = ["cash flow", "fair value", "net investment"]
hedge_metrics = ["changes in cash flows", "changes in fair value", "variability", "exposure"]


hedge_mitigation_verbs = ["attempt","seek","pursue","undertake"]
hedge_may_mitigation_verbs = ["may attempt","may seek","may pursue","may undertake"]

hedge_use_verbs = ["entered into", "executed", "utilized", "employed", "used", "had", "reported", "maintained", "committed", "implemented", 
                   "applied", "engaged in", "pursued", "utilizes", "employs", "uses", "maintains", "has", "have", "applies", "reports"]
hedge_may_use_verbs = [ "may engage in", "may commit in", "may implement", "may enter into", "may utilize", "may employ", "may use", "may apply", "may have", "may pursue" ]

hedge_change_verbs = ["increase", "decrease", "affect", "impact"]

hedge_methods = [
    "regression analysis and dollar-offset methods",
    "quantitative analysis",
    "statistical methods",
    "the dollar-offset method",
    "prospective and retrospective testing",
]

hedge_standards = [
    "ASC 815",
    "applicable accounting guidance",
    "U.S. GAAP",
    "accounting standards",
    "ASU 2017-12",  # Targeted Improvements to Hedge Accounting
    "ASC 815",  # Derivatives and Hedging
    "Topic 815",  # Derivatives and Hedging
]

commodities = [
    "crude oil", "natural gas", "electricity", "aluminum", "copper", "steel",
    "corn", "soybeans", "grain", "metals", "titanium", "fuel",
    "diesel fuel", "gasoline", "raw materials", "commodity", "energy", "resin", "chemicals", "lumber"
]
cost_types = [
    "input costs", "energy costs", "fuel costs", "raw material costs", "manufacturing costs", "mining costs",
    "extraction costs", "transportation costs", "storage costs", "commodity costs", "production costs", "lumber costs",
]

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
    # REMOVED: "designated as hedges of the notes with a notional amount of {currency_code}{notional} {money_unit}, effectively converting portions of fixed-rate debt to floating rates",
    "effectively converting portions of fixed-rate debt to floating rates",
    "to modify the interest rate characteristics of outstanding senior notes",
    # REMOVED: "designated as fair value hedges of fixed-rate obligations",
    # REMOVED: "designated as hedging instruments against changes in the fair value of fixed-rate debt",
    "to hedge interest rate exposure on a portion of its debt portfolio",
    "to convert fixed-rate senior notes to variable rates",
    "to manage interest rate risk on long-term debt",
    # REMOVED: "designated as fair value hedges for its outstanding bonds",
    "to adjust the interest rate profile of its debt",
    "to hedge changes in the fair value of fixed-rate liabilities",
    "to manage exposure to interest rate fluctuations",
    # REMOVED: "designated to hedge fixed-rate debt obligations",
    "to modify the interest rate structure of its senior notes",
    "to hedge the fair value of outstanding debt",
    "to convert portions of its fixed-rate debt to floating rates",
    # REMOVED: "designated as fair value hedges against changes in debt valuation",
    "to manage interest rate exposure on bonds",
    "to adjust the interest rate characteristics of long-term liabilities",
    # REMOVED: "designated as hedges of fixed-rate note obligations",
    "to mitigate interest rate risk on debt issuances",
    "effectively convert the hedged portion of debt to floating rates",
    # REMOVED: "designated as fair value hedges",
    "to manage debt-related interest rate risk",
    "hedging fixed-rate obligations",
    # REMOVED: "designated as fair value hedges",
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
    # REMOVED: "designated as {hedge_type} hedges to hedge against changes in interest rates that could impact expected future issuances of debt",
    # REMOVED: "designated as {hedge_type} hedges to lock in favorable interest rates prior to anticipated debt issuances",
    # REMOVED: "designated as {hedge_type} hedges to hedge interest rate exposure on forecasted debt offerings",
    "to hedge against changes in interest rates that could impact expected future issuances of debt",
    "to lock in favorable interest rates prior to anticipated debt issuances",
    "to hedge interest rate exposure on forecasted debt offerings",
    "to mitigate the risk of rising interest rates on planned fixed-rate debt issuances",
    # REMOVED: "as {hedge_type} hedges to secure interest rates for future debt issuances",
    # REMOVED: "may designate as {hedge_type} hedges to manage interest rate risk",
    "to secure interest rates for future debt issuances",
    "to manage interest rate risk",
    "to protect against interest rate volatility for planned fixed-rate debt issuances",
    # REMOVED: "as {hedge_type} hedges to lock in rates for anticipated debt financings",
    # REMOVED: "designated as {hedge_type} hedges to stabilize future interest costs",
    "to lock in rates for anticipated debt financings",
    "to stabilize future interest costs",
    "to mitigate interest rate fluctuations on planned debt offerings",
    # REMOVED: "designated as {hedge_type} hedges to secure rates for future fixed-rate debt",
    "to secure rates for future fixed-rate debt",
    "to manage interest rate exposure for anticipated debt issuances",
    # REMOVED: "as {hedge_type} hedges to lock in rates prior to debt financings",
    "to lock in rates prior to debt financings",
    "to hedge against rising interest rates for planned debt issuances",
    # REMOVED: "designates as {hedge_type} hedges in preparation for fixed-rate debt",
    "to stabilize interest rates for forecasted bond issuances",
    # REMOVED: "implemented as {hedge_type} hedges to manage risk on future debt offerings",
    "to manage risk on future debt offerings",
    "to secure favorable rates for anticipated fixed-rate debt",
    # REMOVED: "designates as {hedge_type} hedges to mitigate interest rate risk on planned financings",
    "to mitigate interest rate risk on planned financings",
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
    "to manage translation exposure",
    "to hedge foreign borrowings",
    "to hedge exposure to foreign currency fluctuations on cross-border transactions",
    # REMOVED: "designated as cash flow hedges of forecasted foreign currency revenues",
    # REMOVED: "designated as cash flow hedges due to changes in foreign exchange rates and are recorded at fair value",
    "to hedge forecasted foreign currency revenues",
    "due to changes in foreign exchange rates and are recorded at fair value",
    "to manage translation risk of foreign subsidiaries",
    "to hedge anticipated foreign currency purchases",
    "to protect against volatility in foreign currency receivables",
    "to hedge forecasted foreign currency cash flows",
    "to manage currency risk",
    "to hedge forecasted foreign currency expenditures",
    "mitigating exposure to foreign currency fluctuations",
    # REMOVED: "designated as hedges of currency-denominated obligations",
    "to hedge currency-denominated obligations",
    "to hedge foreign currency exposures",
    # REMOVED: "designated as cash flow hedges of forecasted transactions",
    "to hedge forecasted foreign currency transactions",
    "to hedge foreign exchange exposures",
    "protecting against currency fluctuations",
    "to hedge intercompany transactions",
    "hedging foreign-denominated cash flows",
    "mitigating foreign exchange risk",
    # REMOVED: "designated as cash flow hedges of forecasted foreign currency transactions",
    "protecting against exchange rate movements",
    # REMOVED: "designated as hedges of intercompany exposures",
    "to hedge intercompany exposures",
    # REMOVED: "designated to manage currency-denominated cash flows",
    "to manage currency-denominated cash flows",
    # REMOVED: "serving as cash flow hedges of forecasted currency transactions",
]
# Equity (EQ) specific accounting reasons
eq_specific_reasons = [
    "offsetting market value changes in the underlying equity positions",
    "mitigating exposure to equity market volatility",
    "offsetting losses on equity investments",
    "offsetting gains on equity investments",
    "to manage exposure to changes in the market price of its common stock and related equity-based compensation costs",
    "to hedge variability in compensation expense associated with changes in share price",
    "to mitigate exposure to equity price movements",
    "to manage market risks associated with fluctuations in stock price",
    "hedging exposures tied to equity-based programs",
    "to offset potential volatility from changes in share price",
    "to reduce variability in reported expenses arising from equity-linked compensation",
    # REMOVED: "designated as economic hedges of share price exposure",
    "as economic hedges of share price exposure",
    "to hedge the market price risk associated with stock-based compensation plans",
    "to mitigate equity-related market risk",
    "linked to the value of its common stock or market indices",
    "to manage risks related to equity-linked compensation obligations",
    "intended to hedge changes in equity market values",
    "to manage share price exposure",
    "to offset volatility in stock-based compensation expense",
    "to hedge changes in equity valuation",
    "to hedge exposure to its common stock value",
    "related to equity-based compensation programs",
    "to manage equity-linked exposures",
    "to mitigate volatility in stock-based compensation costs",
    # REMOVED: "remaining in effect as hedges of equity price risk",
    "as hedges of equity price risk",
    "to manage changes in the value of its shares",
    "as part of its equity risk management strategy",
    "to hedge share price fluctuations",
    "to manage exposure to its common stock price volatility",
    "to hedge variability in equity-based compensation expenses",
    "to mitigate equity price risk",
    "to manage stock price fluctuations",
    "to hedge equity-related exposures",
    "to offset share price volatility",
    "to reduce variability in equity-linked compensation costs",
    "to manage market risks tied to stock-based compensation",
    "to hedge equity market risk",
    "to manage equity price movements",
    "to hedge equity-based compensation obligations",
    "to hedge equity price changes",
    "to mitigate volatility in equity-based compensation",
    "to manage equity valuation risks",
    "to manage equity price volatility",
    "to hedge stock-based compensation costs",
    "to mitigate volatility in equity compensation expenses",
    "to manage share price fluctuations",
    "to hedge equity market risks",
    "to hedge equity price exposure",
    "to manage stock price volatility",
    "to hedge equity-based compensation costs",
    "to manage share price risk",
    "to mitigate equity price volatility",
    "to hedge stock-based compensation risks",
    "to manage equity market risk",
    "to manage stock-based compensation costs",
    "to hedge equity-linked risks",
]

# Commodity Price (CP) specific accounting reasons
cp_specific_reasons = [
    "offsetting {commodity} price fluctuations",
    "mitigating exposure to volatile {commodity} prices",
    "stabilizing cost of goods sold despite {commodity} price movements",
    "hedging against increases in {commodity} costs",
    "hedging against decreases in {commodity} sale prices",
    "to hedge {commodity} price risk",
    "to manage {commodity} exposures",
    "to hedge forecasted {commodity} purchases or sales",
    "to manage fluctuations in {commodity} prices",
    "for {commodity} risk management",
    "to hedge volatility in {commodity} costs",
    "to mitigate {commodity} price exposure",
    "effectively hedged volatility in {commodity} costs",
    # REMOVED: "designated as hedges for {commodity} procurement",
    "to hedge {commodity} procurement",
    "to stabilize {commodity} costs",
    "to manage {commodity} price volatility",
    "to hedge {commodity} exposures",
    "to mitigate risks from {commodity} price swings",
    "to protect against {commodity} market fluctuations",
    "to manage {commodity} exposure",
    "to lock in pricing",
    "to manage {commodity} cost volatility",
    "to hedge forecasted {commodity} purchases",
    "mitigating exposure to {commodity} price fluctuations",
    "protecting against changes in {commodity} prices",
    # REMOVED: "designated for hedging {commodity} exposures",
    "to stabilize input costs",
    "to hedge {commodity} procurement risks",
    # REMOVED: "serving as {commodity} price hedges",
    "protecting against {commodity} market volatility",
    "to hedge {commodity} procurement risk",
]

# Special templates for accounting impact
accounting_impact_templates = [
    "As of {month} {end_day}, {year}, {swap_type} were designated as {hedge_type} hedges, {reason}",
    "At {end_day} {month}, {year}, {company} {verb} {swap_type} with a total notional amount of {currency_code}{notional} {money_unit}, {reason}",
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
    "{company} also have {verb} {swap_type} {purpose}. Such {swap_type} had a notional value of {currency_code}{notional1} {money_unit} and {currency_code}{notional2} {money_unit} as of {month} {end_day}, {year} and {month} {end_day}, {prev_year}, respectively",
    "{company} {verb} {swap_type} with notional values of {currency_code}{notional1} {money_unit} as of {month} {end_day}, {year} {comparison} {currency_code}{notional2} {money_unit} as of {month} {end_day}, {prev_year}",
    "As of {month} {end_day}, {year}, {company} {verb} {swap_type} with a notional value of {currency_code}{notional1} {money_unit}, {comparison} {currency_code}{notional2} {money_unit} in the prior year",
    "{company} {verb} {swap_type} {purpose}, {trend} {currency_code}{notional2} {money_unit} as of {month} {end_day}, {prev_year} to {currency_code}{notional1} {money_unit} as of {month} {end_day}, {year}",
    "As of {month} {end_day}, {year}, {swap_type} with a notional value of {currency_code}{notional1} {money_unit} were in place, {comparison} {currency_code}{notional2} {money_unit} as of {month} {end_day}, {prev_year}",
    "In {year}, {swap_type} with a notional value of {currency_code}{notional1} {money_unit} were active, {comparison} {currency_code}{notional2} {money_unit} in {prev_year}",
    "As of {month} {end_day}, {year}, {company}'s {swap_type} portfolio had a notional value of {currency_code}{notional1} {money_unit}, {comparison} {currency_code}{notional2} {money_unit} in {prev_year}",
    "At year-end {year}, {swap_type} with a notional amount of {currency_code}{notional1} {money_unit} were {verb} {purpose}, {comparison} {currency_code}{notional2} {money_unit} in {prev_year}",
]

# ------------------------------------------------------------------------------
# SHARED TIMING COMPONENTS (Used across all events: termination, expiration, dedesignation, settlement)
# ------------------------------------------------------------------------------

# Time periods
time_periods = [
    "In the {quarter} quarter of {year}",
    "During the {quarter} quarter of {year}",
    "In {month} {year}",
    "During {month} {year}",
    "In {year}",
    "During {year}",
    "prior to {month} {end_day}, {year}",
    "prior to year-end {year}",
    "As of {month} {end_day}, {year}",
]

# Action verbs (shared across all events)
termination_verbs = [
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
# Payment phrases
payment_phrases = [
    # Settlement patterns (merged)
    "Under each {swap_type}, settlements occur {frequency} for {currency_code}{notional} {money_unit}, {result}",
    "Each {swap_type} settles {frequency} for {currency_code}{notional} {money_unit}, {result}",
    "{frequency} payments of {currency_code}{notional} {money_unit} are required under each {swap_type}, {result}",
    "For every {swap_type}, {frequency} payments of {currency_code}{notional} {money_unit} are made, {result}",
    "Each {swap_type} involves {frequency} settlements of {currency_code}{notional} {money_unit}, {result}",
    "{frequency} settlements under each {swap_type} for {currency_code}{notional} {money_unit} {result}",
    "Each {swap_type} calls for {frequency} payments of {currency_code}{notional} {money_unit}, {result}",
    "Each {swap_type} entails {frequency} settlement of {currency_code}{notional} {money_unit}, {result}",
]
# Settlement result phrases
payment_results = [
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
    "{company} {verb} no outstanding derivative positions as of year-end {year}",
    "resulting in no outstanding hedge positions as of {month} {end_day}, {year}",
    "with no derivative instruments remaining at period end",
    "leaving no active derivative positions at year-end",
    "resulting in no active hedges as of {month} {end_day}, {year}",
    "leaving no derivative instruments outstanding",
    "with no remaining hedge positions at year-end {year}",
    "resulting in no active derivative contracts at period end",
    "leaving no outstanding hedges as of {month} {end_day}, {year}",
    "with no derivative positions remaining at year-end",
    "resulting in no active hedges at period end",
    "with no hedges remaining at year-end",
    "resulting in no outstanding derivative instruments",
    "leaving no active derivative positions",
    "with no hedges in place at {month} {end_day}, {year}",
    "with no derivatives outstanding at year-end",
    "resulting in no active hedge positions",
    "leaving no derivative contracts at period end",
    "with no outstanding hedges as of {month} {end_day}, {year}",
    "there were no such {swap_type} outstanding",
]

# No-replacement phrases (for expirations specifically)
no_replacement_phrases = [
    "with no new positions {verb} during the year",
    "with no replacement hedges executed during the remainder of the fiscal year",
    "and {company} elected not to enter into new derivative contracts during the period",
    "and no new hedging instruments were established for the fiscal year",
    "with no new derivative positions initiated",
    "with no new hedges entered during the year",
    "and {company} did not execute new derivative contracts",
    "with no replacement hedges established",
    "and no new derivative instruments were {verb} during the fiscal year",
    "with no new positions taken",
    "and {company} chose not to initiate new hedges",
    "with no new derivative contracts executed",
    "leaving no active hedges for the remainder of the year",
    "with no new hedges established",
    "with no new positions entered",
    "and {company} did not replace them with new hedges",
    "with no new derivative contracts initiated",
    "and no further hedging instruments were established",
    "with no new hedges entered into",
    "with no new contracts {verb}",
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
all_event_results =  no_position_results + dedesignation_specific_results

# Merged event template patterns (termination, expiration, dedesignation, settlement)
merged_event_patterns = [
    # Termination patterns
    "{time_period}, {company} {termination_verb} all remaining {swap_type} agreements. {result}",
    "{time_period}, all previously designated {swap_type} were {termination_verb}, {result}",
    "{company} {termination_verb} all {swap_type} positions {time_period}, {result}",
    "All outstanding {swap_type} matured or were {termination_verb} {time_period}, {result}",
    "{time_period}, {company} {termination_verb} all {swap_type} agreements, {result}",
    "{time_period}, {company} {termination_verb} {swap_type} positions, {result}",
    "{time_period}, all {swap_type} were {termination_verb}, {result}",
    "{company} {termination_verb} all outstanding {swap_type} {time_period}, {result}",
    "{time_period}, {company} {termination_verb} its {swap_type} portfolio, {result}",
    "{time_period}, all {swap_type} agreements were {termination_verb}, {result}",
    "As of {month} {end_day}, {year}, there were no such {swap_type} outstanding",
    # Expiration patterns
    "All previously outstanding derivatives {termination_verb} {time_period}, {no_replacement}",
    "{company}'s derivative portfolio was fully {termination_verb} {time_period} {no_replacement}",
    "Outstanding hedge positions {termination_verb} throughout {year}, {no_replacement}",
    "{time_period}, all existing {swap_type} {termination_verb}, {no_replacement}",
    "{time_period}, all {swap_type} contracts {termination_verb}, {no_replacement}",
    "{company}'s {swap_type} portfolio fully {termination_verb} {time_period}, {no_replacement}",
    "{time_period}, all outstanding {swap_type} {termination_verb}, {no_replacement}",
    "{time_period}, {company}'s {swap_type} positions {termination_verb}, {no_replacement}",
    "All {swap_type} {termination_verb} {time_period}, {no_replacement}",
    "{time_period}, {company}'s derivative portfolio of {swap_type} was fully settled, {no_replacement}",
    # De-designation patterns
    "{company} {dedesignation_action} all of our {swap_type} {time_period}",
    "{company} {dedesignation_action} {swap_type} {time_period}, {result}",
    "All {swap_type} were {dedesignation_action} as hedging instruments {time_period}",
    "{time_period}, {company} {dedesignation_action} all outstanding {swap_type}",
    "{time_period}, all {swap_type} were {dedesignation_action}, {result}",
    "All {swap_type} were {dedesignation_action} {time_period}, {result}",
    "{time_period}, all {swap_type} lost their hedge designation status",
    # Quarterly termination with settlement patterns
    "{time_period}, {company} {termination_verb} {swap_type} with {frequency} settlements, {result}",
    "{time_period}, all {swap_type} were {termination_verb} {frequency}, {result}",
    "{company} conducted {frequency} {termination_verb} of {swap_type} {time_period}, {result}",
]


# Other templates
fx_currency_templates = [
    "The currency hedged items are usually denominated in the following main currencies: {currencies}",
    "{company}'s primary currency exposures include {currencies}",
    "Foreign currency risk primarily relates to exposures in {currencies}",
    "Our most significant currency exposures are to {currencies}",
    "{company} faces foreign exchange risk primarily from {currencies}",
    "In order to reduce foreign currency translation exposure from {currencies}, {company} seeks to denominate borrowings in the currencies of our principal assets and cash flows. These are primarily denominated in {currencies}",
    "To minimize translation exposure, {company} aligns the currency composition of its debt with the currencies of its operating assets, primarily {currencies}",
    "{company} reduces foreign currency translation risk by borrowing in the same currencies as its principal assets and cash flows, which are mainly {currencies}",
    "{company} matches debt currency denomination to the currencies of its key operating assets to mitigate translation exposure, focusing on {currencies}",
]

# ==============================================================================
# HEDGE POLICY
# ==============================================================================
hedge_policy_templates = [
    "Changes in the fair value of {swap_type} are recorded each period in current earnings or other comprehensive income (loss), depending on whether a derivative instrument is designated as part of a hedging transaction and, if it is, the type of hedging transaction",
    "{swap_type} are measured at fair value with gains and losses recorded in earnings or accumulated other comprehensive income based on hedge designation",
    "{company} accounts for {swap_type} at fair value, with changes in fair value recognized in either net income or other comprehensive income depending on the nature of the hedging relationship",
    "Fair value changes in {swap_type} are reflected in the financial statements through either the income statement or other comprehensive income, based on whether hedge accounting is applied",
    "{company} records {swap_type} at fair value, with changes recognized in earnings or OCI depending on hedge designation",
    "Changes in derivative fair values are recorded in net income or accumulated OCI, based on the type of hedge and its designation",
    "{swap_type} are accounted for at fair value, with gains or losses recorded in earnings or other comprehensive income per hedge accounting rules",
    "{company} recognizes fair value changes of {swap_type} in either current earnings or OCI, depending on the hedging relationship",
    "{swap_type} are measured at fair value, with changes reflected in net income or accumulated OCI based on hedge designation",
    "Fair value adjustments for derivatives are recorded in earnings or OCI, depending on whether the instrument qualifies for hedge accounting",
    "{company} accounts for {swap_type} at fair value, recognizing changes in either the income statement or other comprehensive income",
    "Changes in the fair value of {swap_type} are recorded in earnings or OCI, based on the nature of the hedging relationship",
    "{swap_type} are valued at fair value, with gains and losses recognized in net income or OCI depending on hedge accounting treatment",
    "{company} records fair value changes in {swap_type} in either earnings or accumulated OCI, based on hedge designation",
    "Derivative fair value changes are recognized in the income statement or OCI, depending on the type of hedging relationship",
    "{company} accounts for {swap_type} at fair value, with changes recorded in earnings or OCI per applicable accounting standards",
    "Fair value changes in {swap_type} are reflected in net income or OCI, based on their hedge designation",
    "{swap_type} are measured at fair value, with changes recorded in earnings or other comprehensive income depending on hedge accounting",
    "{company} recognizes derivative fair value changes in either net income or OCI, based on the hedging relationship",
    "Changes in derivative fair values are recorded in current earnings or OCI, depending on the hedge type and accounting treatment",
    "All {swap_type}, other than those that satisfy specific exceptions, are recorded at fair value. {company} record changes in the fair value of our derivative positions based on the value for which the derivative instrument could be exchanged between willing parties",
    "If market quotes are not available to estimate fair value, management’s best estimate of fair value is based on the quoted market price of {swap_type} with similar characteristics or determined through industry-standard valuation techniques",
    "{company} value our {swap_type} using observable inputs including interest rate curves, risk adjusted discount rates, credit spreads and other relevant data",
    "Gains and losses on {swap_type} are recognized currently in earnings",
    "The ultimate fair value of our {swap_type} is uncertain, and {company} believe that it is reasonably possible that a change in the estimated fair value could occur in the near future",
    "The accounting for the changes in the fair value of the {swap_type} depends on the intended use of the {swap_type} and the resulting designation",
    "For a {swap_type} that does not qualify as a {hedge_type} hedge, the change in {hedge_type} is recognized currently in net income",
    "Based upon certain factors, including a review of the {swap_type} for {company}'s counterparties, {company} determined its counterparty credit risk to be immaterial",
    "Based upon certain factors, including a review of the {swap_type} for {company}'s counterparties, {company} determined its counterparty credit risk to be material",
]

hedge_documentation_templates = [
    "For a derivative to qualify as a hedge at inception and throughout the hedged period, {company} formally document the nature and relationships between the hedging instruments and hedged item",
    "For a derivative designated as a {hedge_type} hedge, the gain or loss is recognized in earnings in the period of change together with the offsetting loss or gain on the risk being hedged",
    "{company} maintains formal documentation of all hedging relationships, including the risk management objective and strategy for undertaking the hedge",
    "Hedge accounting requires formal documentation at inception describing the hedging relationship and {company}'s risk management objectives",
    "{company} document our hedging relationships and risk management strategies at inception in accordance with applicable accounting standards",
    "{company} prepares formal documentation for all hedges, detailing the hedging instrument, hedged item, and risk management strategy",
    "At hedge inception, {company} document the relationship between the derivative and the hedged item, including the risk management objective",
    "{company} maintains detailed documentation of hedging relationships to comply with hedge accounting requirements",
    "{company} formally document all hedging relationships at inception, including the strategy and objectives for risk management",
    "Hedge documentation includes the risk management objective, hedging instrument, and hedged item, prepared at inception",
    "{company} records formal documentation for hedges, outlining the relationship and risk management strategy",
    "{company} document the hedging relationship and risk management objectives at the start of each hedge in line with accounting standards",
    "{company} maintains documentation for all derivative hedges, including the hedged item and risk management strategy",
    "Formal documentation of hedging relationships is prepared at inception to support hedge accounting treatment",
    "{company} document the nature of hedging relationships and risk management objectives at the outset of each hedge",
    "{company} ensures formal documentation of all hedges, including the hedged item and risk management strategy",
    "Hedge accounting documentation includes the hedging instrument, hedged item, and risk management objectives at inception",
    "{company} prepare formal documentation for all hedging relationships to meet accounting standard requirements",
    "{company} documents the risk management strategy and hedging relationships at the start of each hedge",
    "Formal hedge documentation is maintained, detailing the hedged item, hedging instrument, and risk management objectives",
    "{company} document all hedging relationships at inception, including the risk management strategy and hedge objectives",
]

hedge_effectiveness_templates = [
    "{company} {verb}, both at inception and on an on-going basis, whether the {swap_type} that are utilized in {hedge_type} hedging transactions are highly effective in offsetting the {metric} of hedged items",
    "{company} {verb} hedge effectiveness {frequency} to ensure derivatives continue to meet the criteria for hedge accounting",
    "Hedge effectiveness is {verb} {frequency} using {method} in accordance with {standard}",
    "{company} {verb} {frequency} assessments of hedge effectiveness to determine whether hedging relationships remain highly effective",
    "{company} {verb} hedge effectiveness {frequency} in accordance with {standard}",
    "Hedge effectiveness is {verb} {frequency} to confirm that {swap_type} remain highly effective in offsetting {metric}",
    "{company} {verb} hedge effectiveness {frequency} using {method} to ensure compliance with {standard}",
    "{company} {verb} {frequency} tests of hedge effectiveness for {swap_type} to offset changes in {metric}",
    "Hedge effectiveness is {verb} {frequency} to verify that derivatives qualify for hedge accounting under {standard}",
    "{company} evaluate {swap_type} effectiveness {frequency} to ensure they offset {metric} as intended",
    "{company} {verb} effectiveness of {swap_type} {frequency} using {method} per {standard}",
    "Hedge effectiveness for {swap_type} is {verb} {frequency} to confirm alignment with {metric}",
    "{company} {verb} {frequency} hedge effectiveness tests using {method} to comply with {standard}",
    "{company} {verb} {swap_type} {frequency} to ensure they effectively hedge {metric}",
    "Hedge effectiveness is {verb} {frequency} for {swap_type} to meet {standard} requirements",
    "{company} {verb} the effectiveness of {swap_type} {frequency} to offset changes in {metric} per {standard}",
    "{company} {verb} {frequency} assessments of {swap_type} effectiveness using {method}",
    "Hedge effectiveness is {verb} {frequency} to ensure {swap_type} offset {metric} as required",
    "{company} {verb} hedge effectiveness {frequency} for {swap_type} in accordance with {standard}",
    "{company} {verb} {swap_type} effectiveness {frequency} to confirm compliance with {standard}",
    "Each {swap_type} guarantees a return equal to the actual return, and as such, effectively acts as a hedge",
]
hedge_ineffectiveness_templates = [
    "{company} assess hedge ineffectiveness {frequency} and record the gain or loss related to the ineffective portion of derivative instruments, if any, to current earnings",
    "Any hedge ineffectiveness is recognized immediately in earnings in the period identified",
    "Ineffectiveness, if present, is measured {frequency} and recorded in the consolidated statements of operations",
    "{company} recognizes any ineffective portion of hedging instruments in current period earnings",
    "Gains or losses from the ineffective portion of derivative instruments are recognized in earnings {frequency}",
    "{company} evaluates hedge effectiveness and records any ineffectiveness in the statement of operations for the relevant period",
    "Ineffective amounts arising from hedging relationships are reported in earnings as part of the assessment {frequency}",
    "{company} monitors hedge effectiveness and immediately recognizes any ineffectiveness in income",
    "Hedge ineffectiveness, when identified, is reflected in earnings for the reporting period in which it occurs",
    "The ineffective portion of designated hedges is calculated and recognized in current earnings {frequency}",
]

hedge_discontinuation_templates = [
    "If {company} determine that a forecasted transaction is no longer probable of occurring, {company} discontinue hedge accounting and any related unrealized gain or loss on the derivative instrument is recognized in current earnings",
    "Hedge accounting is discontinued if the hedged forecasted transaction is no longer expected to occur, with accumulated gains or losses reclassified to earnings",
    "When a hedged forecasted transaction becomes improbable, {company} dedesignates the hedging relationship and recognizes deferred gains or losses immediately",
    "If a forecasted transaction fails to occur, amounts previously deferred in other comprehensive income are reclassified to current period earnings",
    "{company} ceases hedge accounting for derivatives when the hedged item is no longer expected to occur, with any accumulated gains or losses recorded in earnings",
    "Deferred gains or losses on discontinued hedges are recognized immediately in the consolidated statements of operations",
    "Upon dedesignation of a hedge, the ineffective and deferred portions of derivative instruments are recorded in current period earnings",
    "Hedge discontinuation is applied when the underlying forecasted transaction is no longer probable, reclassifying previously deferred amounts to income",
    "If the hedged item does not materialize, accumulated OCI amounts for the hedge are transferred to current earnings",
    "{company} derecognizes hedge accounting when criteria are no longer met, and any associated gains or losses are recognized in the period of discontinuation",
]

hedge_no_trading_templates = [
    "{company} does not enter into derivative transactions for trading purposes",
    "{company}'s policy prohibits the use of derivatives for speculative or trading purposes",
    "Derivatives are {verb} solely for hedging and risk management, not for speculative trading",
    "{company} does not engage in derivative transactions for speculative purposes",
    "All derivative transactions are {verb} for hedging purposes and not for trading or speculation",
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


def _expand_pattern(pattern):
    """Expand placeholders in a pattern using all combinations of replacement lists."""
    placeholder_map = {
        "{result}": all_event_results,
        "{frequency}": settlement_frequencies,
        "{termination_verb}": termination_verbs,
        "{comparison}": comparison_phrases,
        "{trend}": trend_descriptors,
        "{purpose}": optional_purposes,
        "{time_period}": time_periods,
        "{no_replacement}": no_replacement_phrases,
        "{dedesignation_action}": dedesignation_actions,
        "{state}": state_descriptors,
    }

    # Identify placeholders present in the pattern
    active_placeholders = [k for k in placeholder_map if k in pattern]
    if not active_placeholders:
        return [pattern]

    # Create all possible combinations of replacements
    replacement_lists = [placeholder_map[k] for k in active_placeholders]
    expanded = []
    for combo in itertools.product(*replacement_lists):
        new_pattern = pattern
        for key, val in zip(active_placeholders, combo):
            new_pattern = new_pattern.replace(key, val)
        expanded.append(new_pattern)
    return expanded


def generate_optional_templates():
    """Generate all optional/comparative templates."""
    templates = []
    for pattern in optional_template_patterns:
        expanded = _expand_pattern(pattern)
        templates.extend([to_sentence_case(t) for t in expanded])
    return templates


def generate_termination_templates():
    """Generate all merged event templates (termination, expiration, dedesignation)."""
    templates = []
    for pattern in merged_event_patterns:
        expanded = _expand_pattern(pattern)
        templates.extend([to_sentence_case(t) for t in expanded])
    return templates


def generate_payment_templates():
    """Generate payment-related templates."""
    templates = []
    for pattern in payment_phrases:
        expanded = _expand_pattern(pattern)
        templates.extend([to_sentence_case(t) for t in expanded])
    return templates


def generate_hedge_position_templates(hedge_type="gen"):
    """
    Generate all template combinations for a specific hedge type.
    Args:
        hedge_type: One of "ir", "fx", "eq", "cp", "gen"
    Returns:
        List of all generated templates
    """
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

    # Single-year amount_swap_orders
    amount_swap_orders = [
        to_sentence_case(pattern.replace("{connector}", connector))
        for pattern in amount_patterns
        for connector in amount_connectors
    ]

    # Two-year and three-year versions
    two_year_amounts = [
        to_sentence_case(pattern.replace("{connector}", connector))
        for pattern in two_year_amount_patterns
        for connector in amount_connectors
    ]
    three_year_amounts = [
        to_sentence_case(pattern.replace("{connector}", connector))
        for pattern in three_year_amount_patterns
        for connector in amount_connectors
    ]

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

    # Historical templates
    for template in historical_templates:
        expanded = _expand_pattern(template)
        templates.extend([to_sentence_case(t) for t in expanded])

    # Accounting impact templates
    for template in accounting_impact_templates:
        if "{reason}" in template:
            for reason in accounting_reasons:
                full = template.replace("{reason}", reason)
                templates.append(to_sentence_case(full))
        else:
            templates.append(to_sentence_case(template))

    # Two-year / Three-year "no prior year" templates
    for template in two_year_no_prior_templates:
        for pattern in two_year_no_prior_patterns:
            templates.append(
                to_sentence_case(template.replace("{no_prior_pattern}", pattern))
            )
    for template in three_year_no_prior_templates:
        for pattern in three_year_no_prior_patterns:
            templates.append(
                to_sentence_case(template.replace("{no_prior_pattern}", pattern))
            )

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

hedge_payment_templates = generate_payment_templates()
hedge_termination_templates = generate_termination_templates()
hedge_types = ["ir", "fx", "cp", "eq", "gen"]
hedge_position_templates = {}
for ht in hedge_types:
    hedge_position_templates[ht] = generate_hedge_position_templates(ht)

# for i in hedge_position_templates["ir"]:
#     print(i)
