warrant_issuance_templates = [
    'In connection with the {event}, {company} issued warrants to purchase up to {shares} shares of common stock at an exercise price of {currency_code}{price} per share, in accordance with the guidance contained in FASB ASC 815 "Derivatives and Hedging" whereby under that provision the warrants do not meet the criteria for equity treatment and must be recorded as a liability',
    "During {month} {year}, {company} issued {shares} warrants exercisable at {currency_code}{price} per share in conjunction with {event} and is classified as a liability",
    "As part of {event}, {company} granted liability-classified warrants for {shares} shares with a strike price of {currency_code}{price}, expiring in {expiry_year}",
    "{company} issued {shares} warrants at an exercise price of {currency_code}{price} per share, are classified as liabilities the guidence of ASC 815, as consideration for {event}",
    "In {month} {year}, warrants to acquire {shares} shares at {currency_code}{price} per share were issued in connection with {event}, and are derivative liabilities",
    "Under the guidance in ASC 815-40, certain warrants issued at {year} do not meet the criteria for equity treatment",
]

# Warrant events/reasons
warrant_events = [
    "a debt financing transaction",
    "the series B preferred stock offering",
    "a credit facility agreement",
    "initial public offering",
    "a strategic partnership agreement",
    "the convertible note issuance",
    "a private placement",
    "the acquisition financing",
    "vendor financing arrangements",
]

# Warrant fair value measurement templates
warrant_fv_templates = [
    "The fair value of the warrants classifed as liabilities was determined to be {currency_code}{amount} {money_unit} using the  as of {date}",
    "At issuance, the warrant liabilities were valued at {currency_code}{amount} {money_unit} using a ",
    "{company} estimated the fair value of the warrants at {currency_code}{amount} {money_unit} as of {month} {end_day}, {year} using the {model} methodology",
    "Using a {model}, the warrant liabilities were fair valued at {currency_code}{amount} {money_unit} as of {date}",
    "The fair value of outstanding liability-classified warrants totaled {currency_code}{amount} {money_unit} at year-end {year}, {verb} using {model}",
    "The fair value of outstanding warrant liabilities totaled {currency_code}{amount} {money_unit} at year-end {year}, {verb} using {model}",
    "The fair value of the warrants classified as liabilities is estimated using the , with the following inputs as of {month} {year}",
    "The fair value of the warrant liabilities presented below were {verb} using {model}",
]


# Warrant liability classification templates
warrant_liability_templates = [
    "The warrants are classified as liabilities and marked to market each reporting period with changes in fair value recorded in {location}",
    "These warrants are recorded as liabilities at fair value, with subsequent changes recognized in {location}",
    "{company} accounts for the warrants as liabilities rather than equity measured at fair value through {location}",
    "After all relevant assessments, {company} determined that the warrants issued under the {event} require classification as a liability pursuant to ASC 840"
    "Warrant liabilities are remeasured to fair value at each balance sheet date with gains and losses recorded in {location}",
    "As the warrants contain certain provisions, they are classified as liabilities and adjusted to fair value quarterly through {location}",
    "Warrants accounted for as liabilities have the potential to be settled in cash or are not indexed to {company}'s own stock",
    "This warrant liability will be re-measured at each balance sheet date until the warrants are exercised or expire, and any change in fair value will be recognized in {company}'s {location}",
    "Any decrease or increase in the estimated fair value of the warrant liability since the most recent balance sheet date is recorded in {company}'s {location} as changes in fair value of derivative liabilities",
    "The amount of warrant liability was determined and recognized on {location} for the applicable reporting period based on the number of warrants that would have been issued",
]


# Derivative liability general templates
deriv_liability_general_templates = [
    "Derivative liabilities consist primarily of warrant liabilities and are measured at fair value on a recurring basis using Level 3 inputs",
    "{company}'s derivative liabilities primarily relate to freestanding warrants and embedded conversion features that require bifurcation",
    "As of {month} {end_day}, {year}, derivative liabilities totaled {currency_code}{amount} {money_unit} compared to {currency_code}{prev_amount} {money_unit} in the prior year",
    "Changes in the fair value of derivative liabilities during {year} resulted in a {gain_loss} of {currency_code}{amount} {money_unit}",
    "{company} recognized derivative liabilities of {currency_code}{amount} {money_unit} related to warrants issued in connection with financing transactions during {year}",
    "{company}’s warrant liability is based on  utilizing management judgment and pricing inputs from observable and unobservable markets with less volume and transaction frequency than active markets",
    "The following table presents information about {company}'s warrant liabilities that are measured at fair value on a recurring basis at {month} {end_day}, {year} and indicates the fair value hierarchy of the valuation inputs",
]

# Down round feature templates
down_round_templates = [
    "The warrants contain down round provisions that adjust the exercise price if {company} issues equity securities at prices below the then-current exercise price",
    "Due to down round features that could result in a variable number of shares upon exercise, the warrants are classified as liabilities rather than equity",
    "The warrants include anti-dilution protection in the form of down round provisions, requiring liability classification under ASC 815-40",
    "Down round features embedded in the warrants preclude equity classification and require remeasurement at fair value each period",
]

# Earnout liability templates
earnout_templates = [
    "In connection with the acquisition of {target}, {company} recorded an earnout liability of {currency_code}{amount} {money_unit}, which will be settled in cash or shares based on achievement of revenue milestones through {year}",
    "{company} assumed earnout obligations valued at {currency_code}{amount} {money_unit} as part of the {target} acquisition, payable upon achievement of specified operational targets",
    "Contingent consideration arrangements from business combinations resulted in derivative liabilities of {currency_code}{amount} {money_unit} as of {month} {end_day}, {year}",
    "The earnout liability related to the {target} acquisition was remeasured to {currency_code}{amount} {money_unit} during {year}, with the change recorded in other income (expense)",
]

# Historical warrant templates (for label 5)
warrant_past_templates = [
    "During {year}, {company} had outstanding warrant liabilities to purchase {shares} shares at {currency_code}{price} per share, which expired unexercised in {month} {year}",
    "In {year}, all outstanding warrants were exercised or expired, and {company} has no derivative liabilities as of {month} {end_day}, {current_year}",
    "{company} previously issued warrants in connection with {event} during {year}. These derivative liabilities were fully exercised by {month} {expiry_year}",
    "Warrants issued in {year} with an exercise price of {currency_code}{price} per share were settled during {settlement_year}, eliminating all derivative warrant liabilities",
    "As of {month} {end_day}, {current_year}, {company} no longer has any outstanding derivative liabilities. All liability-classified warrants issued in {year} were exercised or expired by {expiry_year}",
]

warrant_liability_extinguishment_templates = [
    "The warrant liabilities of {currency_code}{amount} {money_unit} recorded in {year} were extinguished upon exercise and expiration during {settlement_year}",
    "All warrant liabilities were eliminated in {settlement_year} following the exercise of outstanding warrants by holders",
    "During {settlement_year}, {company} settled all outstanding warrant liabilities, recognizing a final fair value adjustment of {currency_code}{amount} {money_unit}",
    "The warrant liability balance of {currency_code}{amount} {money_unit} at {month} {end_day}, {year} was reduced to zero during {settlement_year} upon warrant exercises",
]

earnout_past_templates = [
    "The earnout liability related to the {target} acquisition, recorded in {year}, was settled in {settlement_year} upon achievement of the specified milestones",
    "Contingent consideration from the {year} acquisition of {target} was paid out in {settlement_year}, extinguishing the {currency_code}{amount} {money_unit} earnout liability",
    "{company}'s earnout obligations from prior acquisitions were fully satisfied by {settlement_year}, with no remaining contingent consideration liabilities",
    "During {settlement_year}, {company} paid {currency_code}{amount} {money_unit} to settle earnout liabilities related to business combinations completed in {year}",
]
