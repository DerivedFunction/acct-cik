# Embedded derivative identification templates
embedded_identification_templates = [
    "{company} has identified embedded derivatives within certain {host_contract} that require bifurcation and separate accounting under ASC 815",
    "Certain {host_contract} contain embedded features that meet the definition of derivatives and are not clearly and closely related to the host contract",
    "{company}'s {host_contract} include embedded derivative features that have been bifurcated and recorded separately at fair value",
    "Embedded derivatives have been identified within {host_contract} and are accounted for separately from the host instrument",
    "{company} evaluated {host_contract} and determined that certain embedded features require bifurcation under derivative accounting guidance",
    '{company} adopted SFAS 155, "Accounting for Certain Hybrid Instruments" to identify all embedded derivative features',
    "{company} measures a hybrid financial instrument in its entirety at fair value after having identified all embedded derivative features."
    "{company} identified and documented the embedded derivative features, and the irrevocably elected to measure and carry the {host_contract} at fair value",
]

host_contracts = [
    "convertible debt instruments",
    "hybrid financial instruments",
    "convertible preferred stock",
    "redeemable preferred stock",
    "convertible notes payable",
    "customer contracts",
    "supplier agreements",
    "lease agreements with variable payments",
]

# Specific embedded derivative types
embedded_types_templates = [
    "The embedded derivatives consist primarily of {embedded_type} that are measured at fair value through earnings",
    "{company} has bifurcated {embedded_type} from the host {host_contract}",
    "Embedded {embedded_type} within {host_contract} are carried at fair value with changes recorded in {location}",
    "The {embedded_type} embedded in the {host_contract} requires separate recognition as a derivative liability",
]

embedded_types = [
    "conversion features",
    "redemption features",
    "reset provisions",
    "make-whole provisions",
    "contingent interest features",
    "price adjustment mechanisms",
    "indexed payment terms",
    "foreign currency-linked provisions",
    "commodity price escalation clauses",
]

# Convertible debt embedded derivative templates
convertible_debt_templates = [
    "{company} issued {currency_code}{principal} {money_unit} in convertible senior notes in {month} {year}. The conversion feature was determined to be an embedded derivative requiring bifurcation, with an initial fair value of {currency_code}{embedded_fv} {money_unit}",
    "In {month} {year}, {company} completed an offering of {currency_code}{principal} {money_unit} aggregate principal amount of convertible notes. The embedded conversion option was bifurcated and valued at {currency_code}{embedded_fv} {money_unit}",
    "The convertible notes include conversion features that are not clearly and closely related to the debt host. The embedded derivative was recorded at a fair value of {currency_code}{embedded_fv} {money_unit} at issuance",
    "Upon issuance of the {currency_code}{principal} {money_unit} convertible debt in {year}, {company} allocated {currency_code}{embedded_fv} {money_unit} to the embedded conversion derivative",
]

# Fair value measurement of embedded derivatives
embedded_fv_templates = [
    "The fair value of the embedded derivative was {currency_code}{amount} {money_unit} as of {month} {end_day}, {year}, compared to {currency_code}{prev_amount} {money_unit} at {month} {end_day}, {prev_year}",
    "Embedded derivative liabilities totaled {currency_code}{amount} {money_unit} at year-end {year}, representing a {change_direction} from {currency_code}{prev_amount} {money_unit} in the prior year",
    "As of {month} {end_day}, {year}, {company} recorded embedded derivative liabilities of {currency_code}{amount} {money_unit} measured using Level 3 inputs",
    "The embedded derivatives had a fair value of {currency_code}{amount} {money_unit} at {month} {end_day}, {year}, with changes in value recorded in other expense",
]

# Valuation methodology templates
embedded_valuation_templates = [
    "The fair value of embedded derivatives is determined using a {model}, incorporating assumptions for {assumptions}",
    "{company} values embedded derivatives using {model} with key inputs including {assumptions}",
    "Fair value is estimated using {model}, which considers {assumptions}",
    "Embedded derivatives are valued using {model}, with significant unobservable inputs related to {assumptions}",
]

valuation_assumptions = [
    "stock price volatility, risk-free interest rates, and expected term",
    "credit spreads, conversion probability, and stock price volatility",
    "volatility, dividend yield, and time to maturity",
    "probability of conversion, discount rates, and market price of common stock",
    "expected volatility, probability of redemption, and time to maturity",
]

# Closely and clearly related analysis templates
ccr_analysis_templates = [
    "{company} performed an assessment of whether the embedded features were clearly and closely related to the economic characteristics of the host contract and concluded bifurcation was required",
    "The embedded features are not clearly and closely related to the debt host instrument, as the conversion feature is indexed to {company}'s own stock and includes down round protection",
    "Management evaluated the economic characteristics and risks of the embedded features and determined they are not clearly and closely related to the host, requiring separate accounting",
    "The embedded derivative fails the clearly and closely related test due to its equity-linked characteristics and variable settlement provisions",
]

# Conversion/settlement templates
embedded_settlement_templates = [
    "Upon conversion or redemption of the host instrument, the embedded derivative is remeasured to fair value with any gain or loss recognized in earnings, and the liability is extinguished",
    "In {month} {year}, {currency_code}{principal} {money_unit} of convertible notes were converted, resulting in settlement of the associated embedded derivative liability and recognition of a {gain_loss} of {currency_code}{amount} {money_unit}",
    "{company} settled embedded derivative liabilities totaling {currency_code}{amount} {money_unit} during {year} in connection with debt extinguishment transactions",
    "During the {quarter} quarter of {year}, the conversion of notes resulted in derecognition of {currency_code}{amount} {money_unit} in embedded derivative liabilities",
]

# Embedded FX derivatives templates
embedded_fx_templates = [
    "Certain {host_contract} contain payments indexed to foreign currency exchange rates that represent embedded foreign currency derivatives",
    "{company} has identified embedded foreign currency derivatives in {host_contract} where payments are denominated in a currency other than the functional currency of either party",
    "Embedded foreign exchange derivatives arise from {host_contract} with payment terms linked to movements in the {currency_pair} exchange rate",
    "{company}'s {host_contract} include embedded FX derivatives requiring bifurcation due to currency mismatches between contract terms and functional currencies",
]


# Historical embedded derivative templates (for label 7)
embedded_past_templates = [
    "{company} previously maintained embedded derivatives within {host_contract} issued in {year}. These instruments were fully converted or redeemed by {settlement_year}",
    "Embedded derivative liabilities related to convertible notes issued in {year} were extinguished upon conversion during {settlement_year}",
    "As of {month} {end_day}, {current_year}, {company} has no embedded derivative liabilities. All instruments containing embedded features were settled in {settlement_year}",
    "The embedded derivatives bifurcated from {host_contract} in {year} were eliminated following the redemption of the host instruments in {settlement_year}",
]

convertible_debt_redemption_templates = [
    "The {currency_code}{principal} {money_unit} convertible notes issued in {year} were fully converted to common stock during {settlement_year}, resulting in derecognition of the {currency_code}{embedded_fv} {money_unit} embedded derivative liability",
    "In {month} {settlement_year}, {company} redeemed all outstanding convertible debt originally issued in {year}, eliminating embedded derivative liabilities of {currency_code}{amount} {money_unit}",
    "The convertible debt instruments with embedded derivatives issued in {year} matured in {settlement_year}, with all notes converted to equity prior to maturity",
    "During {settlement_year}, {company} completed the conversion of all {currency_code}{principal} {money_unit} in convertible notes, extinguishing the related embedded derivative liability",
]

embedded_no_longer_outstanding_templates = [
    "{company} no longer has any embedded derivative liabilities as all instruments containing bifurcated features were settled, converted, or matured by {settlement_year}",
    "As of {month} {end_day}, {current_year}, there are no outstanding embedded derivatives. All such liabilities were extinguished in {settlement_year}",
    "The embedded derivative liabilities of {currency_code}{amount} {money_unit} recorded in prior years were fully eliminated by {settlement_year}",
    "No embedded derivatives remain outstanding as of year-end {current_year}. The last remaining instruments were settled in {settlement_year}",
]
