# ============ DEBT AND CREDIT FACILITIES ============

debt_templates = [
    # General facilities and balances
    "{company} maintains a {currency_code}{amount} {money_unit} revolving credit facility that expires in {year}, with {currency_code}{outstanding} {money_unit} outstanding as of {month} {end_day}, {current_year}, with annual interest rate of {pct}%",
    "As of {month} {end_day}, {year}, {company} had total long-term debt of {currency_code}{amount} {money_unit}, consisting primarily of {debt_types}, with an average interest rate of {pct}% and {pct2}%, respectively",
    "Long-term debt, with an annual interest rate of {pct}% as of {month} {end_day}, {year} totaled {currency_code}{amount} {money_unit}, consisting of {debt_types}",
    "At year-end {year}, {company} reported total debt of {currency_code}{amount} {money_unit} with interest rates ranging from {pct}% to {pct2}%, including {debt_types}",
    "{company}'s outstanding borrowings under its revolving credit facility totaled {currency_code}{outstanding} {money_unit} with average interest rate of {pct}% to {pct2}% as of {month} {end_day}, {year}",
    "As of {month} {end_day}, {year}, there was {currency_code}{outstanding} {money_unit} outstanding on the {debt_type} and {currency_code}{outstanding} {money_unit} outstanding on {debt_types}",
    # Issuances and repayments
    "During {year}, {company} issued {currency_code}{amount} {money_unit} in {debt_types} with a maturity date of {maturity_year} and a weighted average interest rate of {pct}%",
    "In {year}, {company} completed a private placement of {currency_code}{amount} {money_unit} of {debt_types}, bearing interest at {pct}% per annum",
    "During {year}, {company} repaid {currency_code}{amount} {money_unit} of its outstanding {debt_type} prior to maturity",
    "{company} repaid {currency_code}{amount} {money_unit} of outstanding {debt_type} during {year} using cash from operations",
    "In {year}, {company} refinanced {currency_code}{amount} {money_unit} of existing {debt_type} at interest rate of {pct}%, extending the maturity to {maturity_year}",
    # Interest rate and maturity details
    "As of year-end {year}, {company} had total {debt_type} of {currency_code}{amount} {money_unit}, {currency_code}{amount2} {money_unit} of which was fixed rate debt with a weighted average interest rate of {pct}% to {pct2}%",
    "The weighted average interest rate on {company}'s {debt_type} was approximately {pct}% as of {month} {end_day}, {year}",
    "As of {month} {end_day}, {year}, {company}'s {debt_type} had a weighted average maturity of {years} years",
    "As of {month} {end_day}, {year}, {company}'s variable-rate borrowings bore interest at an average rate of {pct}%",
    "Interest expense related to {debt_type} for {year} was approximately {currency_code}{amount} {money_unit}",
    "At {month} {year}, {company} repaid {currency_code}{amount} {money_unit} of the {currency_code}{amount2} {money_unit} borrowed",
    # Other specialized cases
    "During {year}, {company} entered into a new {currency_code}{amount} {money_unit} {debt_type} with a maturity in {maturity_year} and annual interest rate of {pct}%",
    "Proceeds from the {debt_type} issuance were used to repay existing borrowings and for general corporate purposes",
    "In {year}, {company} retired {currency_code}{amount} {money_unit} of {debt_type} upon maturity",
    "At {month} {end_day}, {year}, unamortized debt issuance costs related to {debt_type} totaled {currency_code}{amount} {money_unit}",
    "The fair value of {company}'s {debt_type} was estimated at {currency_code}{amount2} {money_unit} as of {month} {end_day}, {year}",
]

debt_types_list = [
    # Common corporate instruments
    "senior unsecured notes and term loans",
    "convertible senior notes and revolving credit borrowings",
    "senior secured notes and equipment financing",
    "bonds and bank term loans",
    "fixed-rate debt",
    "floating-rate debt",
    "term loan B facility",
    "credit facility borrowings",
    "notes payable",
    "long-term loan agreement",
    "short-term loan",
    "long-term debt",
    "short-term debt",
    # Market rate–specific
    "LIBOR-based loans",
    "SOFR-based revolving loans",
    "Eurodollar borrowings",
    "variable-rate debt",
    # Specialized and legacy forms
    "bridge loans",
    "debentures",
    "subordinated notes",
    "commercial paper",
    "secured term loans",
    "lease financing obligations",
    "private placement notes",
]


debt_covenant_templates = [
    "The credit agreement contains customary affirmative and negative covenants, including financial covenants related to leverage ratios and interest coverage",
    "As of {month} {end_day}, {year}, {company} was in compliance with all debt covenants",
    "The revolving credit facility requires maintenance of a maximum leverage ratio of {ratio}:1 and minimum interest coverage ratio of {coverage}:1",
    "Debt agreements contain restrictions on dividends, additional indebtedness, and asset sales, subject to certain exceptions",
    # Covenant and credit facility context
    "The revolving credit facility contains customary financial covenants, including maintaining a maximum leverage ratio and minimum interest coverage ratio",
    "{company} was in compliance with all debt covenants as of {month} {end_day}, {year}",
    "{company}'s credit agreements require maintenance of specified leverage and coverage ratios, which {company} met as of {month} {end_day}, {year}",
]