# ==============================================================================
# MODULAR DERIVATIVE LIABILITIES TEMPLATE SYSTEM
# Covers: Warrants, Earnouts, Embedded Derivatives, and related disclosures
# ==============================================================================

# ------------------------------------------------------------------------------
# SHARED COMPONENTS (Used across multiple derivative types)
# ------------------------------------------------------------------------------

# Time periods (shared)
time_periods = [
    "In {{month}} {{year}}",
    "During {{month}} {{year}}",
    "As of {{month}} {{end_day}}, {{year}}",
    "At {{month}} {{end_day}}, {{year}}",
    "During {{year}}",
    "In {{year}}",
    "At year-end {{year}}",
    "As of {{month}} {{year}}",
]

# Valuation models (shared)
valuation_models = [
    "Monte Carlo simulation model",
    "binomial lattice model",
    "Black-Scholes option pricing model",
    "BSM model",
]

# Fair value change locations (shared)
fv_change_locations = [
    "other income (expense)",
    "earnings",
    "the consolidated statement of operations",
    "other expense",
    "changes in fair value of derivative liabilities",
]

# Gain/loss indicators (shared)
gain_loss_indicators = [
    "gain",
    "loss",
]

# Change directions (shared)
change_directions = [
    "increase",
    "decrease",
]

# Valuation assumptions (shared)
valuation_assumptions = [
    "stock price volatility, risk-free interest rates, and expected term",
    "credit spreads, conversion probability, and stock price volatility",
    "volatility, dividend yield, and time to maturity",
    "probability of conversion, discount rates, and market price of common stock",
    "expected volatility, probability of redemption, and time to maturity",
]

# Assessment/evaluation verbs (shared)
assessment_verbs = [
    "performed",
    "conducted",
    "completed",
    "evaluated",
    "assessed",
    "analyzed",
    "reviewed",
]

# ------------------------------------------------------------------------------
# WARRANT-SPECIFIC COMPONENTS
# ------------------------------------------------------------------------------

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

# Warrant issuance actions
warrant_issuance_actions = [
    "issued warrants to purchase up to {{shares}} shares of common stock at an exercise price of {{currency_code}}{{price}} per share",
    "issued {{shares}} warrants exercisable at {{currency_code}}{{price}} per share",
    "granted liability-classified warrants for {{shares}} shares with a strike price of {{currency_code}}{{price}}, expiring in {{expiry_year}}",
    "issued {{shares}} warrants at an exercise price of {{currency_code}}{{price}} per share",
    "warrants to acquire {{shares}} shares at {{currency_code}}{{price}} per share were issued",
]

# Warrant issuance connectors
warrant_issuance_connectors = [
    "In connection with {event}, {{company}} {action}",
    "{time_period}, {{company}} {action} in conjunction with {event}",
    "As part of {event}, {{company}} {action}",
    "{{company}} {action} as consideration for {event}",
]

# Warrant liability classification reasons
warrant_classification_reasons = [
    "in accordance with the guidance contained in FASB ASC 815 'Derivatives and Hedging' whereby under that provision the warrants do not meet the criteria for equity treatment and must be recorded as a liability",
    "and is classified as a liability",
    "are classified as liabilities under the guidance of ASC 815",
    "and are derivative liabilities",
    "Under the guidance in ASC 815-40, the warrants do not meet the criteria for equity treatment",
]

# Warrant fair value determination phrases
warrant_fv_determination = [
    "The fair value of the warrants classified as liabilities was determined to be {{currency_code}}{{amount}} {{money_unit}}",
    "The warrant liabilities were valued at {{currency_code}}{{amount}} {{money_unit}}",
    "{{company}} estimated the fair value of the warrants at {{currency_code}}{{amount}} {{money_unit}}",
    "The warrant liabilities were fair valued at {{currency_code}}{{amount}} {{money_unit}}",
    "The fair value of outstanding liability-classified warrants totaled {{currency_code}}{{amount}} {{money_unit}}",
    "The fair value of outstanding warrant liabilities totaled {{currency_code}}{{amount}} {{money_unit}}",
]

# Warrant fair value timing
warrant_fv_timing = [
    "using the {model} as of {{month}} {{end_day}}, {{year}}",
    "at issuance, using a {model}",
    "as of {{month}} {{end_day}}, {{year}} using the {model} methodology",
    "at year-end {{year}}, {{verb}} using {model}",
    "using the {model}, with the following inputs as of {{month}} {{year}}",
]

# Warrant remeasurement phrases
warrant_remeasurement = [
    "The warrants are classified as liabilities and marked to market each reporting period with changes in fair value recorded in {location}",
    "These warrants are recorded as liabilities at fair value, with subsequent changes recognized in {location}",
    "{{company}} accounts for the warrants as liabilities rather than equity measured at fair value through {location}",
    "Warrant liabilities are remeasured to fair value at each balance sheet date with gains and losses recorded in {location}",
    "The warrants are classified as liabilities and adjusted to fair value quarterly through {location}",
    "The warrant liability will be re-measured at each balance sheet date until the warrants are exercised or expire, and any change in fair value will be recognized in {{company}}'s {location}",
]

# Warrant liability reasons
warrant_liability_reasons = [
    "Warrants accounted for as liabilities have the potential to be settled in cash or are not indexed to {{company}}'s own stock",
    "After all relevant assessments, {{company}} determined that the warrants issued under the {event} require classification as a liability pursuant to ASC 815-40",
    "As the warrants contain certain provisions, they are classified as liabilities",
]

# Down round features
down_round_features = [
    "The warrants contain down round provisions that adjust the exercise price if {{company}} issues equity securities at prices below the then-current exercise price",
    "Due to down round features that could result in a variable number of shares upon exercise, the warrants are classified as liabilities rather than equity",
    "The warrants include anti-dilution protection in the form of down round provisions, requiring liability classification under ASC 815-40",
    "Down round features embedded in the warrants preclude equity classification and require remeasurement at fair value each period",
]

# ------------------------------------------------------------------------------
# EARNOUT-SPECIFIC COMPONENTS
# ------------------------------------------------------------------------------

# Earnout recording phrases
earnout_recording = [
    "In connection with the acquisition of {target}, {{company}} recorded an earnout liability of {{currency_code}}{{amount}} {{money_unit}}",
    "{{company}} assumed earnout obligations valued at {{currency_code}}{{amount}} {{money_unit}} as part of the {target} acquisition",
    "Contingent consideration arrangements from business combinations resulted in derivative liabilities of {{currency_code}}{{amount}} {{money_unit}}",
    "The earnout liability related to the {target} acquisition was remeasured to {{currency_code}}{{amount}} {{money_unit}}",
]

# Earnout settlement terms
earnout_settlement_terms = [
    "which will be settled in cash or shares based on achievement of revenue milestones through {{year}}",
    "payable upon achievement of specified operational targets",
    "as of {{month}} {{end_day}}, {{year}}",
    "during {{year}}, with the change recorded in {location}",
]

# ------------------------------------------------------------------------------
# EMBEDDED DERIVATIVE COMPONENTS
# ------------------------------------------------------------------------------

# Host contracts (shared)
host_contracts = [
    "convertible debt instruments",
    "OTC convertible notes hedge",
    "convertible hedge",
    "hybrid financial instruments",
    "convertible preferred stock",
    "redeemable preferred stock",
    "convertible notes payable",
    "customer contracts",
    "supplier agreements",
    "lease agreements with variable payments",
    "warrants",
]

# Embedded derivative types (shared)
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
    "put options",
    "call options",
    "prepayment options",
    "step-up interest features",
    "participating payment features",
    "profit participation features",
    "contingent conversion features",
    "down-round protection",
    "ratchet provisions",
    "dual currency provisions",
    "interest rate reset features",
    "equity-linked provisions",
    "inflation indexation clauses",
    "performance-based conversion",
]


# Embedded derivative identification phrases
embedded_identification = [
    "{{company}} has identified embedded derivatives within certain {host_contract} that require bifurcation and separate accounting under ASC 815",
    "Certain {host_contract} contain embedded features that meet the definition of derivatives and are not clearly and closely related to the host contract",
    "{{company}}'s {host_contract} include embedded derivative features that have been bifurcated and recorded separately at fair value",
    "Embedded derivatives have been identified within {host_contract} and are accounted for separately from the host instrument",
    "{{company}} {{verb}} {host_contract} and determined that certain embedded features require bifurcation under derivative accounting guidance",
]

# Embedded derivative type descriptions
embedded_type_descriptions = [
    "The embedded derivatives consist primarily of {embedded_type} that are measured at fair value through earnings",
    "{{company}} has bifurcated {embedded_type} from the host {host_contract}",
    "Embedded {embedded_type} within {host_contract} are carried at fair value with changes recorded in {location}",
    "The {embedded_type} embedded in the {host_contract} requires separate recognition as a derivative liability",
]

# Clearly and closely related conclusions
ccr_bifurcation_required = [
    "{{company}} {{verb}} an assessment of whether the embedded features were clearly and closely related to the economic characteristics of the host contract and concluded bifurcation was required",
    "The embedded features are not clearly and closely related to the debt host instrument",
    "Management {{verb}} the economic characteristics and risks of the embedded features and determined they are not clearly and closely related to the host, requiring separate accounting",
    "The embedded derivative fails the clearly and closely related test",
]

ccr_bifurcation_not_required = [
    "{{company}} {{verb}} the terms of the embedded provisions and concluded they are clearly and closely related to the host contract, and therefore do not require bifurcation",
    "The embedded features are considered clearly and closely related to the debt host instrument, and accordingly no separate derivative recognition is necessary",
    "Management determined that the embedded option is clearly and closely related to the host contract and remains accounted for within the host instrument",
]

ccr_assessment_neutral = [
    "Management {{verb}} whether the embedded features were clearly and closely related to the host instrument as required under ASC 815",
    "{{company}} {{verb}} the economic characteristics of the embedded provisions in accordance with the clearly and closely related guidance",
    "An evaluation of the embedded derivative features was performed to {{verb}} whether they are clearly and closely related to the host contract",
]

# Embedded FX-specific phrases
embedded_fx_identification = [
    "Certain {host_contract} contain payments indexed to foreign currency exchange rates that represent embedded foreign currency derivatives",
    "{{company}} has identified embedded foreign currency derivatives in {host_contract} where payments are denominated in a currency other than the functional currency of either party",
    "Embedded foreign exchange derivatives arise from {host_contract} with payment terms linked to movements in the {currency_pair} exchange rate",
    "{{company}}'s {host_contract} include embedded FX derivatives requiring bifurcation due to currency mismatches",
]

# Convertible debt issuance phrases
convertible_debt_issuance = [
    "{{company}} issued {{currency_code}}{{principal}} {{money_unit}} in convertible senior notes in {{month}} {{year}}",
    "{{company}} completed an offering of {{currency_code}}{{principal}} {{money_unit}} aggregate principal amount of convertible notes",
    "The convertible notes include conversion features that are not clearly and closely related to the debt host",
    "Upon issuance of the {{currency_code}}{{principal}} {{money_unit}} convertible debt in {{year}}",
]

# Convertible debt bifurcation outcomes
convertible_bifurcation_outcome = [
    "The conversion feature was determined to be an embedded derivative requiring bifurcation, with an initial fair value of {{currency_code}}{{embedded_fv}} {{money_unit}}",
    "The embedded conversion option was bifurcated and valued at {{currency_code}}{{embedded_fv}} {{money_unit}}",
    "The embedded derivative was recorded at a fair value of {{currency_code}}{{embedded_fv}} {{money_unit}} at issuance",
    "{{company}} allocated {{currency_code}}{{embedded_fv}} {{money_unit}} to the embedded conversion derivative",
]

# Embedded fair value measurement phrases
embedded_fv_measurement = [
    "The fair value of the embedded derivative was {{currency_code}}{{amount}} {{money_unit}}",
    "Embedded derivative liabilities totaled {{currency_code}}{{amount}} {{money_unit}}",
    "{{company}} recorded embedded derivative liabilities of {{currency_code}}{{amount}} {{money_unit}}",
    "The embedded derivatives had a fair value of {{currency_code}}{{amount}} {{money_unit}}",
]

# Embedded fair value timing
embedded_fv_timing = [
    "as of {{month}} {{end_day}}, {{year}}, compared to {{currency_code}}{{prev_amount}} {{money_unit}} at {{month}} {{end_day}}, {{prev_year}}",
    "at year-end {{year}}, representing a {change_direction} from {{currency_code}}{{prev_amount}} {{money_unit}} in the prior year",
    "as of {{month}} {{end_day}}, {{year}} measured using Level 3 inputs",
    "at {{month}} {{end_day}}, {{year}}, with changes in value recorded in {location}",
]

# Embedded valuation methodology
embedded_valuation_method = [
    "The fair value of embedded derivatives is determined using a {model}, incorporating assumptions for {assumptions}",
    "{{company}} values embedded derivatives using {model} with key inputs including {assumptions}",
    "Fair value is estimated using {model}, which considers {assumptions}",
    "Embedded derivatives are valued using {model}, with significant unobservable inputs related to {assumptions}",
]

# Embedded fair value change recognition
embedded_fv_change_recognition = [
    "During {{year}}, {{company}} recognized a {gain_loss} of {{currency_code}}{{amount}} {{money_unit}} related to changes in the fair value of embedded derivatives",
    "Changes in fair value of embedded derivatives resulted in a {gain_loss} of {{currency_code}}{{amount}} {{money_unit}} for the year ended {{month}} {{end_day}}, {{year}}",
    "{{company}} recorded {gain_loss}s of {{currency_code}}{{amount}} {{money_unit}} from the remeasurement of embedded derivative liabilities during {{year}}",
    "Fair value adjustments on embedded derivatives contributed a {gain_loss} of {{currency_code}}{{amount}} {{money_unit}} to {location} in {{year}}",
]

# Settlement/conversion phrases
settlement_phrases = [
    "Upon conversion or redemption of the host instrument, the embedded derivative is remeasured to fair value with any gain or loss recognized in earnings, and the liability is extinguished",
    "{time_period}, {{currency_code}}{{principal}} {{money_unit}} of convertible notes were converted, resulting in settlement of the associated embedded derivative liability and recognition of a {gain_loss} of {{currency_code}}{{amount}} {{money_unit}}",
    "{{company}} settled embedded derivative liabilities totaling {{currency_code}}{{amount}} {{money_unit}} during {{year}} in connection with debt extinguishment transactions",
    "During the {{quarter}} quarter of {{year}}, the conversion of notes resulted in derecognition of {{currency_code}}{{amount}} {{money_unit}} in embedded derivative liabilities",
]

# ------------------------------------------------------------------------------
# HISTORICAL/PAST COMPONENTS (No longer outstanding)
# ------------------------------------------------------------------------------

# Expiration/exercise phrases
expiration_exercise = [
    "expired unexercised",
    "were exercised or expired",
    "were fully exercised",
    "were settled",
    "expired",
]

# Elimination phrases
elimination_phrases = [
    "eliminating all derivative warrant liabilities",
    "and {{company}} has no derivative liabilities",
    "These derivative liabilities were fully exercised",
    "eliminating all derivative liabilities",
]

# Historical warrant patterns
warrant_past_patterns = [
    "During {{year}}, {{company}} had outstanding warrant liabilities to purchase {{shares}} shares at {{currency_code}}{{price}} per share, which {expiration_exercise} in {{month}} {{year}}",
    "In {{year}}, all outstanding warrants {expiration_exercise}, {elimination}",
    "{{company}} previously issued warrants in connection with {event} during {{year}}. {elimination} by {{month}} {{expiry_year}}",
    "Warrants issued in {{year}} with an exercise price of {{currency_code}}{{price}} per share {expiration_exercise} during {{settlement_year}}, {elimination}",
    "As of {{month}} {{end_day}}, {{current_year}}, {{company}} no longer has any outstanding derivative liabilities. All liability-classified warrants issued in {{year}} {expiration_exercise} by {{expiry_year}}",
]

# Extinguishment phrases
extinguishment_phrases = [
    "were extinguished upon exercise and expiration",
    "were eliminated following the exercise of outstanding warrants by holders",
    "settled all outstanding warrant liabilities",
    "was reduced to zero upon warrant exercises",
]

# Warrant extinguishment patterns
warrant_extinguishment_patterns = [
    "The warrant liabilities of {{currency_code}}{{amount}} {{money_unit}} recorded in {{year}} {extinguishment} during {{settlement_year}}",
    "All warrant liabilities {extinguishment} in {{settlement_year}}",
    "During {{settlement_year}}, {{company}} {extinguishment}, recognizing a final fair value adjustment of {{currency_code}}{{amount}} {{money_unit}}",
    "The warrant liability balance of {{currency_code}}{{amount}} {{money_unit}} at {{month}} {{end_day}}, {{year}} {extinguishment} during {{settlement_year}}",
]

# Earnout settlement phrases
earnout_settlement_phrases = [
    "was settled in {{settlement_year}} upon achievement of the specified milestones",
    "was paid out in {{settlement_year}}, extinguishing the {{currency_code}}{{amount}} {{money_unit}} earnout liability",
    "were fully satisfied by {{settlement_year}}, with no remaining contingent consideration liabilities",
]

# Historical earnout patterns
earnout_past_patterns = [
    "The earnout liability related to the {target} acquisition, recorded in {{year}}, {settlement}",
    "Contingent consideration from the {{year}} acquisition of {target} {settlement}",
    "{{company}}'s earnout obligations from prior acquisitions {settlement}",
    "During {{settlement_year}}, {{company}} paid {{currency_code}}{{amount}} {{money_unit}} to settle earnout liabilities related to business combinations completed in {{year}}",
]

# Embedded past actions
embedded_past_actions = [
    "were fully converted or redeemed",
    "were extinguished upon conversion",
    "were eliminated following the redemption of the host instruments",
    "expired unexercised",
    "were settled",
]

# Historical embedded patterns
embedded_past_patterns = [
    "{{company}} previously {{verb}} embedded derivatives within {host_contract} issued in {{year}}. These instruments {past_action} by {{settlement_year}}",
    "Embedded derivative liabilities related to convertible notes issued in {{year}} {past_action} during {{settlement_year}}",
    "The embedded derivatives bifurcated from {host_contract} in {{year}} {past_action} in {{settlement_year}}",
    "All embedded features associated with convertible debt issued in {{year}} {past_action} by {{settlement_year}}",
    "As of {{month}} {{end_day}}, {{current_year}}, {{company}} has no embedded derivative liabilities. All instruments containing embedded features were settled in {{settlement_year}}",
]

# Convertible debt redemption actions
convertible_redemption_actions = [
    "were fully converted to common stock",
    "were redeemed",
    "matured, with all notes converted to equity prior to maturity",
    "completed the conversion of all notes",
    "induced early conversion",
]

# Convertible debt redemption patterns
convertible_redemption_patterns = [
    "The {{currency_code}}{{principal}} {{money_unit}} convertible notes issued in {{year}} {redemption_action} during {{settlement_year}}, resulting in derecognition of the {{currency_code}}{{embedded_fv}} {{money_unit}} embedded derivative liability",
    "{time_period}, {{company}} {redemption_action} all outstanding convertible debt originally issued in {{year}}, eliminating embedded derivative liabilities of {{currency_code}}{{amount}} {{money_unit}}",
    "The convertible debt instruments with embedded derivatives issued in {{year}} {redemption_action} in {{settlement_year}}",
    "During {{settlement_year}}, {{company}} {redemption_action}, extinguishing the related embedded derivative liability",
]

# No longer outstanding phrases
no_longer_outstanding = [
    "{{company}} no longer has any embedded derivative liabilities as all instruments containing bifurcated features were settled, converted, or matured by {{settlement_year}}",
    "As of {{month}} {{end_day}}, {{current_year}}, there are no outstanding embedded derivatives. All such liabilities were extinguished in {{settlement_year}}",
    "No embedded derivatives remain outstanding as of year-end {{current_year}}. The last remaining instruments were settled in {{settlement_year}}",
    "No amounts related to embedded derivatives are recorded on the consolidated balance sheet as of {{month}} {{end_day}}, {{current_year}}",
    "Management has determined that as of {{month}} {{end_day}}, {{current_year}}, {{company}} does not have any contracts requiring bifurcation of embedded derivatives",
]

# ------------------------------------------------------------------------------
# GENERAL DERIVATIVE LIABILITY TEMPLATES
# ------------------------------------------------------------------------------

deriv_liability_general = [
    "Derivative liabilities consist primarily of warrant liabilities and are measured at fair value on a recurring basis using Level 3 inputs",
    "{{company}}'s derivative liabilities primarily relate to freestanding warrants and embedded conversion features that require bifurcation",
    "As of {{month}} {{end_day}}, {{year}}, derivative liabilities totaled {{currency_code}}{{amount}} {{money_unit}} compared to {{currency_code}}{{prev_amount}} {{money_unit}} in the prior year",
    "Changes in the fair value of derivative liabilities during {{year}} resulted in a {gain_loss} of {{currency_code}}{{amount}} {{money_unit}}",
    "{{company}} recognized derivative liabilities of {{currency_code}}{{amount}} {{money_unit}} related to warrants issued in connection with financing transactions during {{year}}",
    "{{company}}'s warrant liability is based on utilizing management judgment and pricing inputs from observable and unobservable markets with less volume and transaction frequency than active markets",
    "The following table presents information about {{company}}'s warrant liabilities that are measured at fair value on a recurring basis at {{month}} {{end_day}}, {{year}} and indicates the fair value hierarchy of the valuation inputs",
]

# ------------------------------------------------------------------------------
# ADDITIONAL STANDALONE TEMPLATES
# ------------------------------------------------------------------------------

additional_standalone = [
    "{{company}} adopted SFAS 155, 'Accounting for Certain Hybrid Instruments' to identify all embedded derivative features",
    "{{company}} measures a hybrid financial instrument in its entirety at fair value after having identified all embedded derivative features",
    "{{company}} identified and documented the embedded derivative features, and irrevocably elected to measure and carry the {host_contract} at fair value",
    "This standard requires the conversion feature of {host_contract} be separated from the host contract and presented as a derivative instrument if certain conditions are met",
]

# ==============================================================================
# TEMPLATE GENERATION FUNCTIONS
# ==============================================================================


def generate_warrant_issuance_templates():
    """Generate all warrant issuance templates."""
    templates = []
    for connector in warrant_issuance_connectors:
        for event in warrant_events:
            for action in warrant_issuance_actions:
                for reason in warrant_classification_reasons:
                    # Replace time_period if present
                    if "{time_period}" in connector:
                        for time in time_periods:
                            temp = connector.replace("{time_period}", time)
                            temp = temp.replace("{event}", event)
                            temp = temp.replace("{action}", action)
                            templates.append(f"{temp} {reason}")
                    else:
                        temp = connector.replace("{event}", event)
                        temp = temp.replace("{action}", action)
                        templates.append(f"{temp} {reason}")
    return templates


def generate_warrant_fv_templates():
    """Generate all warrant fair value templates."""
    templates = []
    for determination in warrant_fv_determination:
        for timing in warrant_fv_timing:
            for model in valuation_models:
                temp = f"{determination} {timing}"
                templates.append(temp.replace("{model}", model))
    return templates


def generate_warrant_remeasurement_templates():
    """Generate all warrant remeasurement templates."""
    templates = []
    for remeasure in warrant_remeasurement:
        for location in fv_change_locations:
            templates.append(remeasure.replace("{location}", location))
    # Add reasons
    templates.extend(warrant_liability_reasons)
    templates.extend(down_round_features)
    return templates


def generate_earnout_templates():
    """Generate all earnout templates."""
    templates = []
    for recording in earnout_recording:
        for settlement in earnout_settlement_terms:
            if "{location}" in settlement:
                for location in fv_change_locations:
                    templates.append(
                        f"{recording} {settlement}".replace("{location}", location)
                    )
            else:
                templates.append(f"{recording} {settlement}")
    return templates


def generate_embedded_identification_templates():
    """Generate all embedded derivative identification templates."""
    templates = []
    for phrase in embedded_identification:
        for host in host_contracts:
            for verb in assessment_verbs:
                templates.append(
                    phrase.replace("{host_contract}", host).replace("{{verb}}", verb)
                )
    # Add standalone
    templates.extend(additional_standalone)
    return templates


def generate_embedded_types_templates():
    """Generate all embedded derivative type templates."""
    templates = []
    for desc in embedded_type_descriptions:
        for emb_type in embedded_types:
            for host in host_contracts:
                temp = desc.replace("{embedded_type}", emb_type).replace(
                    "{host_contract}", host
                )
                if "{location}" in temp:
                    for location in fv_change_locations:
                        templates.append(temp.replace("{location}", location))
                else:
                    templates.append(temp)
    return templates


def generate_ccr_templates():
    """Generate all clearly and closely related assessment templates."""
    templates = []
    for assessment in (
        ccr_bifurcation_required + ccr_bifurcation_not_required + ccr_assessment_neutral
    ):
        for verb in assessment_verbs:
            templates.append(assessment.replace("{{verb}}", verb))
    return templates


def generate_embedded_fv_templates():
    """Generate all embedded derivative fair value templates."""
    templates = []
    for measurement in embedded_fv_measurement:
        for timing in embedded_fv_timing:
            for direction in change_directions:
                for location in fv_change_locations:
                    temp = f"{measurement} {timing}"
                    temp = temp.replace("{change_direction}", direction)
                    templates.append(temp.replace("{location}", location))
    return templates


def generate_embedded_valuation_templates():
    """Generate all embedded valuation methodology templates."""
    templates = []
    for method in embedded_valuation_method:
        for model in valuation_models:
            for assumption in valuation_assumptions:
                temp = method.replace("{model}", model)
                templates.append(temp.replace("{assumptions}", assumption))
    return templates


def generate_embedded_fv_change_templates():
    """Generate all embedded derivative fair value change templates."""
    templates = []
    for recognition in embedded_fv_change_recognition:
        for gain_loss in gain_loss_indicators:
            for location in fv_change_locations:
                temp = recognition.replace("{gain_loss}", gain_loss)
                templates.append(temp.replace("{location}", location))
    return templates


def generate_convertible_debt_templates():
    """Generate all convertible debt templates."""
    templates = []
    for issuance in convertible_debt_issuance:
        for outcome in convertible_bifurcation_outcome:
            templates.append(f"{issuance}. {outcome}")
    return templates


def generate_embedded_fx_templates():
    """Generate all embedded FX derivative templates."""
    templates = []
    for phrase in embedded_fx_identification:
        for host in host_contracts:
            temp = phrase.replace("{host_contract}", host)
    return templates


def generate_settlement_templates():
    """Generate all settlement/conversion templates."""
    templates = []
    for phrase in settlement_phrases:
        if "{time_period}" in phrase:
            for time in time_periods:
                for gain_loss in gain_loss_indicators:
                    temp = phrase.replace("{time_period}", time)
                    templates.append(temp.replace("{gain_loss}", gain_loss))
        else:
            templates.append(phrase)
    return templates


def generate_warrant_past_templates():
    """Generate all historical warrant templates."""
    templates = []
    for pattern in warrant_past_patterns:
        for exp_ex in expiration_exercise:
            for elim in elimination_phrases:
                temp = pattern.replace("{expiration_exercise}", exp_ex)
                temp = temp.replace("{elimination}", elim)
                if "{event}" in temp:
                    for event in warrant_events:
                        templates.append(temp.replace("{event}", event))
                else:
                    templates.append(temp)
    return templates


def generate_warrant_extinguishment_templates():
    """Generate all warrant extinguishment templates."""
    templates = []
    for pattern in warrant_extinguishment_patterns:
        for ext in extinguishment_phrases:
            templates.append(pattern.replace("{extinguishment}", ext))
    return templates


def generate_earnout_past_templates():
    """Generate all historical earnout templates."""
    templates = []
    for pattern in earnout_past_patterns:
        for settlement in earnout_settlement_phrases:
            templates.append(pattern.replace("{settlement}", settlement))
    return templates


def generate_embedded_past_templates():
    """Generate all historical embedded derivative templates."""
    templates = []
    for pattern in embedded_past_patterns:
        for host in host_contracts:
            for action in embedded_past_actions:
                for verb in assessment_verbs:
                    temp = pattern.replace("{host_contract}", host)
                    temp = temp.replace("{past_action}", action)
                    templates.append(temp.replace("{{verb}}", verb))
    # Add no longer outstanding
    templates.extend(no_longer_outstanding)
    return templates


def generate_convertible_redemption_templates():
    """Generate all convertible debt redemption templates."""
    templates = []
    for pattern in convertible_redemption_patterns:
        for action in convertible_redemption_actions:
            if "{time_period}" in pattern:
                for time in time_periods:
                    temp = pattern.replace("{time_period}", time)
                    templates.append(temp.replace("{redemption_action}", action))
            else:
                templates.append(pattern.replace("{redemption_action}", action))
    return templates


# ==============================================================================
# GENERATE ALL TEMPLATE SETS
# ==============================================================================

warrant_issuance_templates = generate_warrant_issuance_templates()
warrant_fv_templates = generate_warrant_fv_templates()
warrant_remeasurement_templates = generate_warrant_remeasurement_templates()
earnout_templates = generate_earnout_templates()
embedded_identification_templates = generate_embedded_identification_templates()
embedded_types_templates = generate_embedded_types_templates()
ccr_assessment_templates = generate_ccr_templates()
embedded_fv_templates = generate_embedded_fv_templates()
embedded_valuation_templates = generate_embedded_valuation_templates()
embedded_fv_change_templates = generate_embedded_fv_change_templates()
convertible_debt_templates = generate_convertible_debt_templates()
embedded_fx_templates = generate_embedded_fx_templates()
settlement_templates = generate_settlement_templates()
warrant_past_templates = generate_warrant_past_templates()
warrant_extinguishment_templates = generate_warrant_extinguishment_templates()
earnout_past_templates = generate_earnout_past_templates()
embedded_past_templates = generate_embedded_past_templates()
convertible_redemption_templates = generate_convertible_redemption_templates()

# General derivative liability templates (no generation needed)
deriv_liability_general_templates = deriv_liability_general
# ==============================================================================
# SEQUENTIAL TEMPLATE COMBINATIONS
# ==============================================================================

# Warrant issuance + classification + remeasurement (full disclosure sequence)
warrant_full_disclosure_patterns = [
    "{issuance} {classification} {remeasurement}",
    "{issuance} {classification}",
]


def generate_warrant_full_disclosure_templates():
    """Generate complete warrant disclosure sequences."""
    templates = []

    # Generate base issuance phrases
    issuance_phrases = []
    for connector in warrant_issuance_connectors:
        for event in warrant_events:
            for action in warrant_issuance_actions:
                if "{time_period}" in connector:
                    for time in time_periods:  # Limit combinations
                        temp = connector.replace("{time_period}", time)
                        temp = temp.replace("{event}", event)
                        issuance_phrases.append(temp.replace("{action}", action))
                else:
                    temp = connector.replace("{event}", event)
                    issuance_phrases.append(temp.replace("{action}", action))

    # Combine issuance + classification + remeasurement
    for pattern in warrant_full_disclosure_patterns:
        for issuance in issuance_phrases:  # Limit for brevity
            for classification in warrant_classification_reasons:
                if "{remeasurement}" in pattern:
                    for remeasure in warrant_remeasurement:
                        for location in fv_change_locations:
                            temp = pattern.replace("{issuance}", issuance)
                            temp = temp.replace("{classification}", classification)
                            remeasure_text = remeasure.replace("{location}", location)
                            templates.append(
                                temp.replace("{remeasurement}", remeasure_text)
                            )
                else:
                    temp = pattern.replace("{issuance}", issuance)
                    templates.append(temp.replace("{classification}", classification))

    return templates


# Embedded derivative identification + CCR assessment + bifurcation outcome
embedded_full_disclosure_patterns = [
    "{identification} {ccr_assessment} {outcome}",
    "{identification} {ccr_assessment}",
]


def generate_embedded_full_disclosure_templates():
    """Generate complete embedded derivative disclosure sequences."""
    templates = []

    # Generate identification phrases
    identification_phrases = []
    for phrase in embedded_identification:  # Limit
        for host in host_contracts:
            for verb in assessment_verbs:
                identification_phrases.append(
                    phrase.replace("{host_contract}", host).replace("{{verb}}", verb)
                )

    # CCR outcomes
    ccr_outcomes = ccr_bifurcation_required + ccr_bifurcation_not_required

    # Bifurcation outcomes (for required cases)
    bifurcation_outcomes = [
        "requiring separate accounting",
        "requiring bifurcation and separate fair value measurement",
        "necessitating derivative liability recognition",
    ]

    for pattern in embedded_full_disclosure_patterns:
        for identification in identification_phrases:
            for ccr in ccr_outcomes:
                for verb in assessment_verbs:
                    ccr_text = ccr.replace("{{verb}}", verb)
                    if "{outcome}" in pattern:
                        for outcome in bifurcation_outcomes:
                            temp = pattern.replace("{identification}", identification)
                            temp = temp.replace("{ccr_assessment}", ccr_text)
                            templates.append(temp.replace("{outcome}", outcome))
                    else:
                        temp = pattern.replace("{identification}", identification)
                        templates.append(temp.replace("{ccr_assessment}", ccr_text))

    return templates


# Convertible debt issuance + bifurcation + fair value measurement
convertible_full_disclosure_patterns = [
    "{issuance} {bifurcation} {fair_value_measurement}",
    "{issuance} {bifurcation}",
]


def generate_convertible_full_disclosure_templates():
    """Generate complete convertible debt disclosure sequences."""
    templates = []

    for pattern in convertible_full_disclosure_patterns:
        for issuance in convertible_debt_issuance:
            for bifurcation in convertible_bifurcation_outcome:
                if "{fair_value_measurement}" in pattern:
                    for measurement in embedded_fv_measurement:
                        for timing in embedded_fv_timing:
                            temp = pattern.replace("{issuance}", issuance)
                            temp = temp.replace("{bifurcation}", bifurcation)
                            fv_text = f"{measurement} {timing}"
                            templates.append(
                                temp.replace("{fair_value_measurement}", fv_text)
                            )
                else:
                    temp = pattern.replace("{issuance}", issuance)
                    templates.append(temp.replace("{bifurcation}", bifurcation))

    return templates


# Historical warrant + extinguishment + final adjustment
warrant_historical_full_patterns = [
    "{historical} {extinguishment} {final_adjustment}",
    "{historical} {extinguishment}",
]


def generate_warrant_historical_full_templates():
    """Generate complete historical warrant disclosure sequences."""
    templates = []

    final_adjustments = [
        "with no remaining warrant liabilities on the balance sheet",
        "resulting in zero derivative liability balances",
        "and no further fair value adjustments are required",
    ]

    for pattern in warrant_historical_full_patterns:
        for historical in warrant_past_patterns:
            for exp_ex in expiration_exercise:
                historical_text = historical.replace("{expiration_exercise}", exp_ex)
                for ext in extinguishment_phrases:
                    if "{final_adjustment}" in pattern:
                        for adjustment in final_adjustments:
                            temp = pattern.replace("{historical}", historical_text)
                            temp = temp.replace("{extinguishment}", ext)
                            templates.append(
                                temp.replace("{final_adjustment}", adjustment)
                            )
                    else:
                        temp = pattern.replace("{historical}", historical_text)
                        templates.append(temp.replace("{extinguishment}", ext))

    return templates
# ==============================================================================
# ADDITIONAL SEQUENTIAL TEMPLATE COMBINATIONS
# ==============================================================================

# 1. EARNOUT: Recording + Settlement Terms + Remeasurement
earnout_full_disclosure_patterns = [
    "{recording} {settlement_terms} {remeasurement}",
    "{recording} {settlement_terms}",
]


def generate_earnout_full_disclosure_templates():
    """Generate complete earnout disclosure sequences."""
    templates = []

    remeasurement_phrases = [
        "The liability was subsequently remeasured to {{currency_code}}{{amount}} {{money_unit}} during {{year}}",
        "Fair value adjustments resulted in a {gain_loss} of {{currency_code}}{{amount}} {{money_unit}}",
        "with changes in fair value recorded in {location}",
    ]

    for pattern in earnout_full_disclosure_patterns:
        for recording in earnout_recording:
            for settlement in earnout_settlement_terms:
                if "{remeasurement}" in pattern:
                    for remeasure in remeasurement_phrases:
                        for location in fv_change_locations:
                            for gain_loss in gain_loss_indicators:
                                temp = pattern.replace("{recording}", recording)
                                temp = temp.replace("{settlement_terms}", settlement)
                                remeasure_text = remeasure.replace(
                                    "{location}", location
                                ).replace("{gain_loss}", gain_loss)
                                templates.append(
                                    temp.replace("{remeasurement}", remeasure_text)
                                )
                else:
                    temp = pattern.replace("{recording}", recording)
                    templates.append(temp.replace("{settlement_terms}", settlement))

    return templates


# 2. EMBEDDED FX: Identification + CCR Analysis + Bifurcation Decision
embedded_fx_full_disclosure_patterns = [
    "{fx_identification} {ccr_analysis} {bifurcation_decision}",
    "{fx_identification} {ccr_analysis}",
]


def generate_embedded_fx_full_disclosure_templates():
    """Generate complete embedded FX disclosure sequences."""
    templates = []

    bifurcation_decisions = [
        "and was bifurcated as a separate derivative instrument",
        "and therefore require separate accounting as derivatives",
        "and do not require bifurcation under ASC 815",
        "and remain within the host contract's accounting treatment",
    ]

    for pattern in embedded_fx_full_disclosure_patterns:
        for fx_id in embedded_fx_identification:
            for host in host_contracts:
                fx_id_text = fx_id.replace("{host_contract}", host)
                for ccr in (ccr_bifurcation_required + ccr_bifurcation_not_required):
                    for verb in assessment_verbs:
                        ccr_text = ccr.replace("{{verb}}", verb)
                        if "{bifurcation_decision}" in pattern:
                            for decision in bifurcation_decisions:
                                temp = pattern.replace("{fx_identification}", fx_id_text)
                                temp = temp.replace("{ccr_analysis}", ccr_text)
                                templates.append(temp.replace("{bifurcation_decision}", decision))
                        else:
                            temp = pattern.replace("{fx_identification}", fx_id_text)
                            templates.append(temp.replace("{ccr_analysis}", ccr_text))

    return templates


# 3. EMBEDDED TYPES: Type Description + Fair Value Measurement + Change Recognition
embedded_types_full_disclosure_patterns = [
    "{type_description} {fv_measurement} {fv_change}",
    "{type_description} {fv_measurement}",
]


def generate_embedded_types_full_disclosure_templates():
    """Generate complete embedded derivative type disclosure sequences."""
    templates = []

    for pattern in embedded_types_full_disclosure_patterns:
        for desc in embedded_type_descriptions:
            for emb_type in embedded_types:
                for host in host_contracts:
                    desc_text = desc.replace("{embedded_type}", emb_type).replace(
                        "{host_contract}", host
                    )

                    for measurement in embedded_fv_measurement:
                        for timing in embedded_fv_timing:
                            fv_text = f"{measurement} {timing}"

                            if "{fv_change}" in pattern:
                                for change in embedded_fv_change_recognition:
                                    for gain_loss in gain_loss_indicators:
                                        for location in fv_change_locations:
                                            temp = pattern.replace(
                                                "{type_description}", desc_text
                                            )
                                            temp = temp.replace(
                                                "{fv_measurement}", fv_text
                                            )
                                            change_text = change.replace(
                                                "{gain_loss}", gain_loss
                                            ).replace("{location}", location)
                                            templates.append(
                                                temp.replace("{fv_change}", change_text)
                                            )
                            else:
                                temp = pattern.replace("{type_description}", desc_text)
                                templates.append(
                                    temp.replace("{fv_measurement}", fv_text)
                                )

    return templates


# 4. EMBEDDED VALUATION: Methodology + Assumptions + Fair Value Result
embedded_valuation_full_disclosure_patterns = [
    "{methodology} {fv_result}",
    "{methodology}",
]


def generate_embedded_valuation_full_disclosure_templates():
    """Generate complete embedded valuation disclosure sequences."""
    templates = []

    fv_results = [
        "resulting in a fair value of {{currency_code}}{{amount}} {{money_unit}} as of {{month}} {{end_day}}, {{year}}",
        "The embedded derivative liability was measured at {{currency_code}}{{amount}} {{money_unit}}",
        "yielding a derivative liability balance of {{currency_code}}{{amount}} {{money_unit}}",
    ]

    for pattern in embedded_valuation_full_disclosure_patterns:
        for method in embedded_valuation_method:
            for model in valuation_models:
                for assumption in valuation_assumptions:
                    method_text = method.replace("{model}", model).replace(
                        "{assumptions}", assumption
                    )

                    if "{fv_result}" in pattern:
                        for result in fv_results:
                            temp = pattern.replace("{methodology}", method_text)
                            templates.append(temp.replace("{fv_result}", result))
                    else:
                        templates.append(pattern.replace("{methodology}", method_text))

    return templates


# 5. SETTLEMENT: Action + Impact + Final Status
settlement_full_disclosure_patterns = [
    "{settlement_action} {financial_impact} {final_status}",
    "{settlement_action} {financial_impact}",
]


def generate_settlement_full_disclosure_templates():
    """Generate complete settlement/conversion disclosure sequences."""
    templates = []

    financial_impacts = [
        "resulting in recognition of a {gain_loss} of {{currency_code}}{{amount}} {{money_unit}}",
        "with a {gain_loss} recorded in {location}",
        "generating {gain_loss}s totaling {{currency_code}}{{amount}} {{money_unit}}",
    ]

    final_statuses = [
        "All related derivative liabilities have been extinguished",
        "with no remaining embedded derivative balances",
        "eliminating all bifurcated liabilities from the balance sheet",
    ]

    for pattern in settlement_full_disclosure_patterns:
        for settlement in settlement_phrases:
            if "{time_period}" in settlement:
                for time in time_periods:
                    settlement_text = settlement.replace("{time_period}", time)
                    for impact in financial_impacts:
                        for gain_loss in gain_loss_indicators:
                            for location in fv_change_locations:
                                impact_text = impact.replace(
                                    "{gain_loss}", gain_loss
                                ).replace("{location}", location)

                                if "{final_status}" in pattern:
                                    for status in final_statuses:
                                        temp = pattern.replace(
                                            "{settlement_action}", settlement_text
                                        )
                                        temp = temp.replace(
                                            "{financial_impact}", impact_text
                                        )
                                        templates.append(
                                            temp.replace("{final_status}", status)
                                        )
                                else:
                                    temp = pattern.replace(
                                        "{settlement_action}", settlement_text
                                    )
                                    templates.append(
                                        temp.replace("{financial_impact}", impact_text)
                                    )
            else:
                templates.append(settlement)

    return templates


# 6. EARNOUT HISTORICAL: Past Recording + Settlement + Final Status
earnout_historical_full_disclosure_patterns = [
    "{past_recording} {settlement_action} {final_status}",
    "{past_recording} {settlement_action}",
]


def generate_earnout_historical_full_disclosure_templates():
    """Generate complete earnout historical disclosure sequences."""
    templates = []

    final_statuses = [
        "No earnout liabilities remain outstanding as of {{month}} {{end_day}}, {{current_year}}",
        "with no remaining contingent consideration obligations",
        "All earnout obligations have been fully satisfied",
    ]

    for pattern in earnout_historical_full_disclosure_patterns:
        for past in earnout_past_patterns:
            for settlement in earnout_settlement_phrases:
                past_text = past.replace("{settlement}", settlement)

                if "{final_status}" in pattern:
                    for status in final_statuses:
                        temp = pattern.replace("{past_recording}", past_text)
                        temp = temp.replace("{settlement_action}", settlement)
                        templates.append(temp.replace("{final_status}", status))
                else:
                    temp = pattern.replace("{past_recording}", past_text)
                    templates.append(temp.replace("{settlement_action}", settlement))

    return templates


# 7. CONVERTIBLE REDEMPTION: Redemption Action + Derivative Impact + Balance Status
convertible_redemption_full_disclosure_patterns = [
    "{redemption_action} {derivative_impact} {balance_status}",
    "{redemption_action} {derivative_impact}",
]


def generate_convertible_redemption_full_disclosure_templates():
    """Generate complete convertible redemption disclosure sequences."""
    templates = []

    derivative_impacts = [
        "resulting in derecognition of the {{currency_code}}{{embedded_fv}} {{money_unit}} embedded derivative liability",
        "eliminating embedded derivative liabilities of {{currency_code}}{{amount}} {{money_unit}}",
        "extinguishing the related embedded derivative liability",
    ]

    balance_statuses = [
        "No embedded derivative liabilities from convertible notes remain outstanding",
        "with zero convertible note derivative balances as of {{month}} {{end_day}}, {{current_year}}",
        "All related bifurcated liabilities have been eliminated from the financial statements",
    ]

    for pattern in convertible_redemption_full_disclosure_patterns:
        for redemption in convertible_redemption_patterns:
            for action in convertible_redemption_actions:
                if "{time_period}" in redemption:
                    for time in time_periods:
                        redemption_text = redemption.replace(
                            "{time_period}", time
                        ).replace("{redemption_action}", action)
                        for impact in derivative_impacts:
                            if "{balance_status}" in pattern:
                                for status in balance_statuses:
                                    temp = pattern.replace(
                                        "{redemption_action}", redemption_text
                                    )
                                    temp = temp.replace("{derivative_impact}", impact)
                                    templates.append(
                                        temp.replace("{balance_status}", status)
                                    )
                            else:
                                temp = pattern.replace(
                                    "{redemption_action}", redemption_text
                                )
                                templates.append(
                                    temp.replace("{derivative_impact}", impact)
                                )
                else:
                    templates.append(redemption)

    return templates


# Generate all additional sequential templates
earnout_full_disclosure_templates = generate_earnout_full_disclosure_templates()
embedded_fx_full_disclosure_templates = generate_embedded_fx_full_disclosure_templates()
embedded_types_full_disclosure_templates = (
    generate_embedded_types_full_disclosure_templates()
)
embedded_valuation_full_disclosure_templates = (
    generate_embedded_valuation_full_disclosure_templates()
)
settlement_full_disclosure_templates = generate_settlement_full_disclosure_templates()
earnout_historical_full_disclosure_templates = (
    generate_earnout_historical_full_disclosure_templates()
)
convertible_redemption_full_disclosure_templates = (
    generate_convertible_redemption_full_disclosure_templates()
)

# Generate all sequential templates
warrant_full_disclosure_templates = generate_warrant_full_disclosure_templates()
embedded_full_disclosure_templates = generate_embedded_full_disclosure_templates()
convertible_full_disclosure_templates = generate_convertible_full_disclosure_templates()
warrant_historical_full_templates = generate_warrant_historical_full_templates()
