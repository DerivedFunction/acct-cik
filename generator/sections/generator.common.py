months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
    "Jan.",
    "Feb.",
    "Mar.",
    "Apr.",
    "May",
    "Aug.",
    "Sep.",
    "Oct.",
    "Nov.",
    "Dec.",
]

quarters = ["first", "second", "third", "fourth", "1st", "2nd", "3rd", "4th"]
# Currency codes for international flavor
currency_codes = ["$", "€", "£", "¥", "CHF ", "SGD ", "CAD ", "AUD "]
currency_pairs = [
    "EUR/USD",
    "EUR/GBP",
    "EUR/JPY",
    "EUR/CHF",
    "EUR/SGD",
    "USD/JPY",
    "GBP/USD",
    "USD/CAD",
    "AUD/USD",
    "USD/CNY",
]

major_currencies = [
    "the Euro",
    "the British pound",
    "the Swiss franc",
    "the Japanese yen",
    "the Canadian dollar",
    "the Australian dollar",
    "the Chinese yuan",
    "the U.S. Dollar",
]

european_currencies = [
    "the Euro",
    "the British pound",
    "the Swiss franc",
    "the Norwegian krone",
    "the Swedish krona",
    "the Polish zloty",
    "the Czech koruna",
    "the Hungarian forint",
]

asian_currencies = [
    "the Japanese yen",
    "the Chinese yuan",
    "the Indian rupee",
    "the South Korean won",
    "the Singapore dollar",
    "the Thai baht",
    "the Malaysian ringgit",
]

americas_currencies = [
    "the Canadian dollar",
    "the Mexican peso",
    "the Brazilian real",
    "the Argentine peso",
    "the Chilean peso",
    "the Colombian peso",
]
all_currencies = (
    set(major_currencies)
    | set(european_currencies)
    | set(asian_currencies)
    | set(americas_currencies)
)
all_currencies = list(all_currencies)

fv_change_locations = [
    "other income (expense), net",
    "change in fair value of derivative liabilities",
    "other comprehensive income",
    "earnings",
    "the consolidated statements of operations",
    "statement of operations",
]

valuation_models = [
    "Monte Carlo simulation model",
    "binomial lattice model",
    "Black-Scholes option pricing model",
    "BSM model",
]

frequencies = [
    "quarterly",
    "on a regular basis",
    "at least quarterly",
    "monthly",
    "periodically",
]
assessment_verbs = ["assessed", "evaluated", "tested", "measured", "analyzed"]
assesment_methods = [
    "regression analysis and dollar-offset methods",
    "quantitative analysis",
    "statistical methods",
    "the dollar-offset method",
    "prospective and retrospective testing",
]
impact_verbs = [
    "increase or decrease",
    "affect",
    "impact",
    "influence",
    "alter",
    "modify",
    "change",
    "adjust",
    "impact positively or negatively",
    "shift",
]
