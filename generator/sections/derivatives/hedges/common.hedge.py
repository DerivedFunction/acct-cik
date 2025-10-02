hedge_past_event_template = [
    "In {month} {year}, {company} entered into {swap_type} agreements with a total notional amount of {currency_code}{amount} {money_unit}, resulting in fair value losses recorded in equity",
    "During {month} {year}, {swap_type} were designated as {hedge_type} hedges, resulting in {currency_code}{amount} {money_unit} of unrealized losses recorded in accumulated OCI",
]


hedge_active_position_template = [
    "As of {month} {end_day}, {year}, {company} maintains {swap_type} with notional amounts totaling {currency_code}{notional} {money_unit}",
    "At year-end {year}, {company} had {swap_type} outstanding with aggregate notional values of {currency_code}{notional} {money_unit} designated as hedges",
    "As of {month} {year}, outstanding {swap_type} with notional amounts of {currency_code}{notional} {money_unit} remain in effect",
    "{company}'s derivative portfolio at {month} {end_day}, {year} consists of {swap_type} with combined notional values of {currency_code}{notional} {money_unit}",
    "At the end of {year}, {swap_type} with an aggregate notional value of {currency_code}{notional} {money_unit} remain active in {company}’s derivative portfolio",
    "As of {month} {end_day}, {year}, {company} has {swap_type} outstanding with a notional amount of {currency_code}{notional} {money_unit}",
    "At year-end {year}, {company}’s derivative portfolio includes {swap_type} with a notional value of {currency_code}{notional} {money_unit}",
    "As of {month} {end_day}, {year}, outstanding {swap_type} totaling {currency_code}{notional} {money_unit} remain designated as hedges",
    "{company} holds {swap_type} with a notional amount of {currency_code}{notional} {money_unit} at {month} {end_day}, {year}, as part of its hedging strategy",
    "At the close of {year}, {swap_type} with an aggregate notional value of {currency_code}{notional} {money_unit} remain designated as hedges",
    "As of {month} {year}, {company}’s {swap_type} portfolio includes notional amounts totaling {currency_code}{notional} {money_unit}",
    "{company}’s derivative instruments as of {month} {end_day}, {year}, include {swap_type} with a total notional amount of {currency_code}{notional} {money_unit}",
]
hedge_optional_templates = [
    "{company} also have entered into {swap_type} to hedge forecasted revenue which were not part of a collar strategy. Such {swap_type} had a notional value of {currency_code}{notional1} {money_unit} and {currency_code}{notional2} {money_unit} as of {month} {end_day}, {year} and {month} {end_day}, {prev_year}, respectively",
    "{company} entered into {swap_type} with notional values of {currency_code}{notional1} {money_unit} as of {month} {end_day}, {year} compared to {currency_code}{notional2} {money_unit} as of {month} {end_day}, {prev_year}",
    "As of {month} {end_day}, {year}, {company} maintained {swap_type} with a notional value of {currency_code}{notional1} {money_unit}, compared to {currency_code}{notional2} {money_unit} in the prior year",
    "{company} utilized {swap_type} to hedge forecasted transactions, with notional amounts decreasing from {currency_code}{notional2} {money_unit} as of {month} {end_day}, {prev_year} to {currency_code}{notional1} {money_unit} as of {month} {end_day}, {year}",
    "As of {month} {end_day}, {year}, {swap_type} with a notional value of {currency_code}{notional1} {money_unit} were in place, down from {currency_code}{notional2} {money_unit} as of {month} {end_day}, {prev_year}",
    "{company} maintained {swap_type} to hedge revenue streams, with notional amounts of {currency_code}{notional1} {money_unit} at {month} {end_day}, {year} compared to {currency_code}{notional2} {money_unit} at {month} {end_day}, {prev_year}",
    "In {year}, {swap_type} with a notional value of {currency_code}{notional1} {money_unit} were active, compared to {currency_code}{notional2} {money_unit} in {prev_year}",
    "As of {month} {end_day}, {year}, {company}’s {swap_type} portfolio had a notional value of {currency_code}{notional1} {money_unit}, reduced from {currency_code}{notional2} {money_unit} in {prev_year}",
    "{company}’s {swap_type} for hedging forecasted revenue had notional values of {currency_code}{notional1} {money_unit} and {currency_code}{notional2} {money_unit} as of {month} {end_day}, {year} and {prev_year}, respectively",
    "At year-end {year}, {swap_type} with a notional amount of {currency_code}{notional1} {money_unit} were used to hedge transactions, compared to {currency_code}{notional2} {money_unit} in {prev_year}",
    "{company} employed {swap_type} with a notional value of {currency_code}{notional1} {money_unit} as of {month} {end_day}, {year}, down from {currency_code}{notional2} {money_unit} as of {month} {end_day}, {prev_year}",
    "As of {month} {end_day}, {year}, {swap_type} to hedge forecasted revenue totaled {currency_code}{notional1} {money_unit}, compared to {currency_code}{notional2} {money_unit} in the prior year",
    "{company}’s {swap_type} portfolio for revenue hedging had a notional value of {currency_code}{notional1} {money_unit} at {month} {end_day}, {year}, versus {currency_code}{notional2} {money_unit} at {month} {end_day}, {prev_year}",
    "In {year}, {company} maintained {swap_type} with a notional amount of {currency_code}{notional1} {money_unit}, reduced from {currency_code}{notional2} {money_unit} in {prev_year}",
    "As of {month} {end_day}, {year}, {swap_type} used for hedging had a notional value of {currency_code}{notional1} {money_unit}, compared to {currency_code}{notional2} {money_unit} as of {month} {end_day}, {prev_year}",
    "{company}’s {swap_type} for transaction hedging totaled {currency_code}{notional1} {money_unit} at {month} {end_day}, {year}, down from {currency_code}{notional2} {money_unit} in {prev_year}",
    "At year-end {year}, {swap_type} with a notional value of {currency_code}{notional1} {money_unit} were active, compared to {currency_code}{notional2} {money_unit} at {month} {end_day}, {prev_year}",
    "{company} utilized {swap_type} with notional amounts of {currency_code}{notional1} {money_unit} as of {month} {end_day}, {year}, versus {currency_code}{notional2} {money_unit} in the prior year",
    "As of {month} {end_day}, {year}, {company}’s {swap_type} for revenue hedging had a notional value of {currency_code}{notional1} {money_unit}, down from {currency_code}{notional2} {money_unit} in {prev_year}",
    "{company} maintained {swap_type} with a notional amount of {currency_code}{notional1} {money_unit} at {month} {end_day}, {year}, compared to {currency_code}{notional2} {money_unit} at {month} {end_day}, {prev_year}",
]
hedge_termination_templates = [
    "In the {quarter} quarter of {year}, {company} terminated all remaining {swap_type} agreements. {company} has no outstanding derivative positions as of year-end {year}",
    "During the {quarter} quarter of {year}, all previously designated {swap_type} were settled or expired, resulting in no outstanding hedge positions as of {month} {end_day}, {year}",
    "{company} closed out all {swap_type} positions during the {quarter} quarter of {year}, with no derivative instruments remaining at period end",
    "All outstanding {swap_type} matured or were terminated in the {quarter} quarter of {year}, leaving no active derivative positions at year-end",
    "In {month} {year}, {company} settled all {swap_type} agreements, resulting in no active hedges as of {month} {end_day}, {year}",
    "During the {quarter} quarter of {year}, {company} closed out {swap_type} positions, leaving no derivative instruments outstanding",
    "In the {quarter} quarter of {year}, all {swap_type} were terminated, with no remaining hedge positions at year-end {year}",
    "{company} settled all outstanding {swap_type} in {month} {year}, resulting in no active derivative contracts at period end",
    "during the {quarter} quarter of {year}, {company} terminated its {swap_type} portfolio, leaving no outstanding hedges as of {month} {end_day}, {year}",
    "In {month} {year}, all {swap_type} agreements were closed out, with no derivative positions remaining at year-end",
    "{company} ended all {swap_type} contracts in the {quarter} quarter of {year}, resulting in no active hedges at period end",
    "During {year}, all outstanding {swap_type} were settled, leaving {company} with no derivative instruments at {month} {end_day}, {year}",
    "In the {quarter} quarter of {year}, {company} terminated {swap_type} agreements, with no hedges remaining at year-end",
    "All {swap_type} positions were closed out in {month} {year}, resulting in no outstanding derivative instruments",
    "During the {quarter} quarter of {year}, {company} settled all {swap_type}, leaving no active derivative positions",
    "In {month} {year}, {company} terminated all {swap_type} contracts, with no hedges in place at {month} {end_day}, {year}",
    "{company} closed out its {swap_type} portfolio in the {quarter} quarter of {year}, with no derivatives outstanding at year-end",
    "During {month} {year}, all {swap_type} were settled or expired, resulting in no active hedge positions",
    "In the {quarter} quarter of {year}, {company} ended all {swap_type} agreements, leaving no derivative contracts at period end",
    "All {swap_type} were terminated in {month} {year}, with no outstanding hedges as of {month} {end_day}, {year}",
]

expiration_templates = [
    "All previously outstanding derivatives expired or were settled during {month} {year}, with no new positions entered into during the year",
    "{company}'s derivative portfolio was fully liquidated in {month} {year} with no replacement hedges executed during the remainder of the fiscal year",
    "Outstanding hedge positions matured throughout {year}, and {company} elected not to enter into new derivative contracts during the period",
    "During {month} {year}, all existing {swap_type} reached maturity, and no new hedging instruments were established for the fiscal year",
    "in the {quarter} quarter of {year}, all {swap_type} contracts matured, with no new derivative positions initiated",
    "{company}’s {swap_type} portfolio fully expired in {month} {year}, with no new hedges entered during the year",
    "During {year}, all outstanding {swap_type} reached maturity, and {company} did not execute new derivative contracts",
    "In {month} {year}, {company}’s {swap_type} positions expired, with no replacement hedges established",
    "All {swap_type} matured in the {quarter} quarter of {year}, and no new derivative instruments were entered into during the fiscal year",
    "During {month} {year}, {company}’s derivative portfolio of {swap_type} was fully settled, with no new positions taken",
    "In {year}, all {swap_type} contracts reached maturity, and {company} chose not to initiate new hedges",
    "{company}’s {swap_type} portfolio expired in {month} {year}, with no new derivative contracts executed",
    "during the {quarter} quarter of {year}, all outstanding {swap_type} matured, leaving no active hedges for the remainder of the year",
    "In {month} {year}, all {swap_type} reached their expiration date, with no new hedges established",
    "{company}’s derivative instruments, including {swap_type}, fully matured in {year}, with no new positions entered",
    "During {month} {year}, all {swap_type} contracts expired, and {company} did not replace them with new hedges",
    "in the {quarter} quarter of {year}, {company}’s {swap_type} portfolio reached maturity, with no new derivative contracts initiated",
    "All outstanding {swap_type} expired in {month} {year}, and no further hedging instruments were established",
    "During {year}, {company}’s {swap_type} contracts fully matured, with no new hedges entered into",
    "In {month} {year}, all derivative positions, including {swap_type}, expired, with no new contracts executed",
]

quarterly_event_templates = [
    "In the {quarter} quarter of {year}, {company} settled {currency_code}{notional} {money_unit} in {swap_type} agreements, resulting in cash proceeds of {currency_code}{settlement} {money_unit}",
    "During the {quarter} quarter of {year}, {swap_type} with notional amounts of {currency_code}{notional} {money_unit} were terminated, generating {currency_code}{settlement} {money_unit} in settlement payments to {company}",
    "{company} unwound {currency_code}{notional} {money_unit} notional of {swap_type} in the {quarter} quarter of {year}, recognizing {currency_code}{settlement} {money_unit} in cash settlements",
    "In the {quarter} quarter of {year}, {company} terminated {swap_type} totaling {currency_code}{notional} {money_unit} notional value, with net settlement receipts of {currency_code}{settlement} {money_unit}",
    "During {month} {year}, {company} settled {currency_code}{notional} {money_unit} in {swap_type}, resulting in {currency_code}{settlement} {money_unit} in cash proceeds",
    "In the {quarter} quarter of {year}, {swap_type} with a notional value of {currency_code}{notional} {money_unit} were unwound, generating {currency_code}{settlement} {money_unit} in settlement payments",
    "{company} terminated {currency_code}{notional} {money_unit} of {swap_type} in {month} {year}, with cash settlements of {currency_code}{settlement} {money_unit}",
    "During the {quarter} quarter of {year}, {company} closed out {currency_code}{notional} {money_unit} in {swap_type}, receiving {currency_code}{settlement} {money_unit} in net proceeds",
    "In {month} {year}, {company} settled {swap_type} with a notional amount of {currency_code}{notional} {money_unit}, resulting in {currency_code}{settlement} {money_unit} in cash receipts",
    "{company} unwound {swap_type} totaling {currency_code}{notional} {money_unit} in the {quarter} quarter of {year}, with {currency_code}{settlement} {money_unit} in settlement proceeds",
    "during the {quarter} quarter of {year}, {company} terminated {currency_code}{notional} {money_unit} in {swap_type} agreements, recognizing {currency_code}{settlement} {money_unit} in cash settlements",
    "In the {quarter} quarter of {year}, {swap_type} with a notional value of {currency_code}{notional} {money_unit} were settled, generating {currency_code}{settlement} {money_unit} in proceeds",
    "{company} closed out {currency_code}{notional} {money_unit} of {swap_type} in {month} {year}, with net settlement payments of {currency_code}{settlement} {money_unit}",
    "during the {quarter} quarter of {year}, {company} unwound {swap_type} totaling {currency_code}{notional} {money_unit}, receiving {currency_code}{settlement} {money_unit} in cash",
    "In {month} {year}, {company} settled {currency_code}{notional} {money_unit} in {swap_type}, resulting in {currency_code}{settlement} {money_unit} in net settlement proceeds",
    "{company} terminated {swap_type} with a notional amount of {currency_code}{notional} {money_unit} in the {quarter} quarter of {year}, with {currency_code}{settlement} {money_unit} in cash proceeds",
    "During {month} {year}, {swap_type} totaling {currency_code}{notional} {money_unit} were unwound, generating {currency_code}{settlement} {money_unit} in settlement receipts",
    "In the {quarter} quarter of {year}, {company} settled {currency_code}{notional} {money_unit} of {swap_type}, recognizing {currency_code}{settlement} {money_unit} in cash payments",
    "{company} closed out {swap_type} with a notional value of {currency_code}{notional} {money_unit} in the {quarter} quarter of {year}, with {currency_code}{settlement} {money_unit} in proceeds",
    "During {month} {year}, {company} terminated {currency_code}{notional} {money_unit} in {swap_type}, resulting in {currency_code}{settlement} {money_unit} in cash settlements",
]

hedge_dedesignation_templates = [
    "{company} de-designated all of our {swap_type} prior to {month} {end_day}, {year}",
    "{company} de-designated {swap_type} during {year}, removing hedge accounting treatment for these instruments",
    "All {swap_type} were de-designated as hedging instruments prior to year-end {year}",
    "During {year}, {company} discontinued hedge accounting for all outstanding {swap_type}",
    "{company} removed hedge designation from {swap_type} in the {quarter} quarter of {year}",
    "In {month} {year}, {company} de-designated all {swap_type}, discontinuing hedge accounting",
    "During the {quarter} quarter of {year}, all {swap_type} were removed from hedge accounting treatment",
    "{company} ceased hedge accounting for {swap_type} in {month} {year}",
    "In {year}, all {swap_type} were de-designated, with no hedge accounting applied at year-end",
    "{company} discontinued hedge designation for {swap_type} during the {quarter} quarter of {year}",
    "All {swap_type} were de-designated in {month} {year}, removing their hedge accounting status",
    "During {year}, {company} ended hedge accounting for its {swap_type} portfolio",
    "In the {quarter} quarter of {year}, {company} de-designated its {swap_type} contracts",
    "{company} removed hedge accounting from {swap_type} in {month} {year}",
    "during the {quarter} quarter of {year}, all {swap_type} lost their hedge designation status",
    "In {year}, {company} de-designated all {swap_type}, discontinuing hedge accounting treatment",
    "{company} ceased applying hedge accounting to {swap_type} in the {quarter} quarter of {year}",
    "All {swap_type} were de-designated prior to {month} {year}, ending their hedge accounting status",
    "During the {quarter} quarter of {year}, {company} removed hedge designation from all {swap_type}",
    "In {month} {year}, {company} discontinued hedge accounting for its {swap_type} portfolio",
]

hedge_context_templates = [
    "Our international operations are subject to government-imposed constraints, including laws on pricing, reimbursement, and access to our products",
    "Our global presence exposes {company} to foreign exchange rate volatility and regulatory risks across multiple jurisdictions",
    "{company}’s global footprint subjects it to currency exchange risks and market-specific regulatory challenges",
    "{company}’s operations in international markets expose it to foreign currency risks and regulatory constraints",
]


fx_ir_context_templates = [
    "{company}'s global operations expose it to various market risks, including fluctuations in foreign currency exchange rates and interest rates",
    "Our business operations in multiple countries result in exposure to foreign currency exchange rate movements and interest rate volatility",
    "{company} operates in numerous international markets, which subjects us to risks from changes in currency exchange rates and interest rates",
    "{company}’s multinational operations are impacted by foreign currency movements and interest rate changes in various markets",
    "As a global entity, {company} faces exposure to exchange rate volatility and interest rate risks in its operations",
    "Our operations across multiple countries expose us to foreign exchange rate changes and interest rate variability",
    "Operating in various jurisdictions, {company} are exposed to fluctuations in foreign currencies and interest rate movements",
    "Our global business model results in exposure to foreign exchange rate changes and interest rate fluctuations",
    "As a multinational company, {company} are subject to risks from currency movements and interest rate volatility across regions",
    "Our global operations are impacted by changes in foreign exchange rates and varying interest rate environments",
    "{company} faces currency exchange and interest rate risks due to its operations in multiple international markets",
]

fx_ir_mitigation_templates = [
    "{company} {verb} to reduce the impact of currency and interest rate movements through natural hedging strategies and the use of derivative contracts",
    "To mitigate these risks, {company} {verb} various hedging strategies including the use of derivative instruments",
    "{company} {verb} to minimize exposure to adverse movements in exchange rates and interest rates through both operational measures and financial derivatives",
    "{company} {verb} to limit currency and interest rate risks through operational adjustments and derivative contracts",
    "{company} {verb} to offset the impact of foreign exchange volatility using derivatives and operational hedging strategies",
    "To manage currency and interest rate risks, {company} {verb} a combination of financial instruments and operational tactics",
    "{company} {verb} to protect against adverse currency and interest rate movements with derivatives and strategic operations",
    "{company} {verb} to stabilize financial results by using derivatives and operational hedging techniques",
    "{company} {verb} to reduce currency and interest rate exposure through strategic operations and derivative contracts",
    "{company} {verb} to manage foreign currency and interest rate risks through hedging and operational strategies",
    "{company} {verb} to offset currency and interest rate volatility with derivative instruments and operational adjustments",
]
hedge_mitigation_templates = [
    "To mitigate market risks, {company} {verb} a combination of derivatives and operational risk management",
    "{company} {verb} to manage overall financial market exposures, including currency, interest rate, and other price risks, through a balanced hedging approach",
    "Our risk management strategy includes the selective use of derivative instruments to reduce exposure to various market risks",
    "{company} {verb} to minimize the effect of adverse financial market movements on earnings and cash flows through operational and financial measures",
    "{company} employs a risk management framework that combines natural hedging techniques with the use of derivative contracts",
    "To manage financial risks, {company} {verb} both centralized treasury operations and selective hedging strategies",
    "{company} {verb} to offset market risk exposures using a combination of operational practices and financial instruments",
    "Our market risk management approach is designed to reduce the volatility of earnings and cash flows caused by fluctuations in financial variables",
    "{company} {verb} to align its market risk exposure with its overall risk tolerance through the use of derivatives and other risk management practices",
    "To mitigate exposure to unpredictable financial markets, {company} {verb} a mix of natural hedging, diversification, and derivative usage",
]

hedge_policy_templates = [
    "Changes in the fair value of derivative instruments are recorded each period in current earnings or other comprehensive income (loss), depending on whether a derivative instrument is designated as part of a hedging transaction and, if it is, the type of hedging transaction",
    "Derivative instruments are measured at fair value with gains and losses recorded in earnings or accumulated other comprehensive income based on hedge designation",
    "{company} accounts for derivatives at fair value, with changes in fair value recognized in either net income or other comprehensive income depending on the nature of the hedging relationship",
    "Fair value changes in derivatives are reflected in the financial statements through either the income statement or other comprehensive income, based on whether hedge accounting is applied",
    "{company} records derivative instruments at fair value, with changes recognized in earnings or OCI depending on hedge designation",
    "Changes in derivative fair values are recorded in net income or accumulated OCI, based on the type of hedge and its designation",
    "Derivatives are accounted for at fair value, with gains or losses recorded in earnings or other comprehensive income per hedge accounting rules",
    "{company} recognizes fair value changes of derivatives in either current earnings or OCI, depending on the hedging relationship",
    "Derivative instruments are measured at fair value, with changes reflected in net income or accumulated OCI based on hedge designation",
    "Fair value adjustments for derivatives are recorded in earnings or OCI, depending on whether the instrument qualifies for hedge accounting",
    "{company} accounts for derivatives at fair value, recognizing changes in either the income statement or other comprehensive income",
    "Changes in the fair value of derivatives are recorded in earnings or OCI, based on the nature of the hedging relationship",
    "Derivatives are valued at fair value, with gains and losses recognized in net income or OCI depending on hedge accounting treatment",
    "{company} records fair value changes in derivatives in either earnings or accumulated OCI, based on hedge designation",
    "Derivative fair value changes are recognized in the income statement or OCI, depending on the type of hedging relationship",
    "{company} accounts for derivatives at fair value, with changes recorded in earnings or OCI per applicable accounting standards",
    "Fair value changes in derivative instruments are reflected in net income or OCI, based on their hedge designation",
    "Derivatives are measured at fair value, with changes recorded in earnings or other comprehensive income depending on hedge accounting",
    "{company} recognizes derivative fair value changes in either net income or OCI, based on the hedging relationship",
    "Changes in derivative fair values are recorded in current earnings or OCI, depending on the hedge type and accounting treatment",
    "All derivative instruments, other than those that satisfy specific exceptions, are recorded at fair value. {company} record changes in the fair value of our derivative positions based on the value for which the derivative instrument could be exchanged between willing parties"
    "If market quotes are not available to estimate fair value, management’s best estimate of fair value is based on the quoted market price of derivatives with similar characteristics or determined through industry-standard valuation techniques",
    "{company} value our {swap_type} using observable inputs including interest rate curves, risk adjusted discount rates, credit spreads and other relevant data",
    "Gains and losses on derivative instruments are recognized currently in earnings",
    "The ultimate fair value of our derivative instruments is uncertain, and {company} believe that it is reasonably possible that a change in the estimated fair value could occur in the near future",
    "The accounting for the changes in the fair value of the derivative depends on the intended use of the derivative and the resulting designation",
    "For a derivative that does not qualify as a {hedge_type} hedge, the change in {hedge_type} is recognized currently in net income",
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
    "{company} assess, both at inception and on an on-going basis, whether the derivative instruments that are used in {hedge_type} hedging transactions are highly effective in offsetting the {metric} of hedged items",
    "{company} evaluates hedge effectiveness {frequency} to ensure derivatives continue to meet the criteria for hedge accounting",
    "Hedge effectiveness is {verb} {frequency} using {method} in accordance with {standard}",
    "{company} perform {frequency} assessments of hedge effectiveness to determine whether hedging relationships remain highly effective",
    "{company} {verb} hedge effectiveness {frequency} in accordance with {standard}",
    "Hedge effectiveness is evaluated {frequency} to confirm that {swap_type} remain highly effective in offsetting {metric}",
    "{company} assess hedge effectiveness {frequency} using {method} to ensure compliance with {standard}",
    "{company} performs {frequency} tests of hedge effectiveness for {swap_type} to offset changes in {metric}",
    "Hedge effectiveness is {verb} {frequency} to verify that derivatives qualify for hedge accounting under {standard}",
    "{company} evaluate {swap_type} effectiveness {frequency} to ensure they offset {metric} as intended",
    "{company} {verb} effectiveness of {swap_type} {frequency} using {method} per {standard}",
    "Hedge effectiveness for {swap_type} is assessed {frequency} to confirm alignment with {metric}",
    "{company} perform {frequency} hedge effectiveness tests using {method} to comply with {standard}",
    "{company} evaluates {swap_type} {frequency} to ensure they effectively hedge {metric}",
    "Hedge effectiveness is {verb} {frequency} for {swap_type} to meet {standard} requirements",
    "{company} assess the effectiveness of {swap_type} {frequency} to offset changes in {metric} per {standard}",
    "{company} conducts {frequency} assessments of {swap_type} effectiveness using {method}",
    "Hedge effectiveness is evaluated {frequency} to ensure {swap_type} offset {metric} as required",
    "{company} {verb} hedge effectiveness {frequency} for {swap_type} in accordance with {standard}",
    "{company} assesses {swap_type} effectiveness {frequency} to confirm compliance with {standard}",
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


hedge_types = [
    "cash flow",
    "fair value",
    "net investment",
]
hedge_metrics = ["changes in cash flows", "changes in fair value", "variability", "exposure"]


hedge_commit_verbs = [
    "attempt",
    "seek",
    "endeavor",
    "strive",
    "work",
    "aim",
    "pursue",
    "undertake",
    "engage",
    "commit",
    "implement",
]

hedge_enter_into_verbs = [
    "entered into",
    "executed",
    "utilized",
    "employed",
    "has used",
    "may enter into",
    "may utilize",
    "may employ",
]
hedge_counterparty_templates = [
    "Most of the counterparties to the derivatives are major banks and {company} is monitoring the associated inherent credit risks",
    "{company} enters into derivative contracts with major financial institutions and monitors counterparty credit risk on an ongoing basis",
    "Derivative counterparties are limited to major banking institutions with strong credit ratings to minimize counterparty risk",
    "Credit risk from derivatives is mitigated by transacting only with highly-rated financial institution counterparties",
    "{company} manages counterparty credit exposure by diversifying its derivative contracts among multiple major banks",
]

hedge_no_trading_templates = [
    "{company} does not enter into derivative transactions for trading purposes",
    "{company}'s policy prohibits the use of derivatives for speculative or trading purposes",
    "Derivatives are used solely for hedging and risk management, not for speculative trading",
    "{company} does not engage in derivative transactions for speculative purposes",
    "All derivative transactions are entered into for hedging purposes and not for trading or speculation",
]

hedge_fv_position_templates = [
    'As of {month} {end_day}, {year}, the fair value of the swaps was a {position_type} of {currency_code}{amount} {money_unit}, the opposite entry for {currency_code}{oci_amount} {money_unit} of which was {oci_action} to "Other comprehensive income" under the cost of hedging accounting treatment',
    'As of {month} {end_day}, {year}, the fair value of these {swap_type} represented a {position_type} of {currency_code}{amount} {money_unit}; the opposite entry was recognized in "Other comprehensive income", with the impact on financial income and expense being immaterial',
    "The fair value of {swap_type} as of {month} {end_day}, {year} was a {position_type} of {currency_code}{amount} {money_unit}, with {currency_code}{oci_amount} {money_unit} {oci_action} to other comprehensive income",
    "As of year-end {year}, outstanding {swap_type} had a fair value {position_type} of {currency_code}{amount} {money_unit}, the offsetting entry being recorded in accumulated other comprehensive income",
]

# Generic Debt Optimization Templates
ir_fx_debt_optimization_templates = [
    "{company} uses {swap_type} to optimize the cost and risk profile of its debt portfolio, adjusting both interest rate and currency exposures",
    "To manage borrowing costs and currency risk, {company} employs {swap_type} to modify the effective interest rate and currency mix of outstanding debt",
    "{company} implements {swap_type} to reduce volatility from interest rate fluctuations and foreign exchange movements on its borrowings",
    "As part of its debt strategy, {company} utilizes {swap_type} to transform debt characteristics, including both fixed/floating rate and currency composition",
    "To hedge against interest rate and foreign exchange risks, {company} applies {swap_type} to optimize its debt obligations",
    "{company} uses {swap_type} to manage exposure to both interest rate changes and currency fluctuations across its debt portfolio",
    "The company employs {swap_type} to balance interest rate and currency risk, converting portions of debt as needed",
    "{company} optimizes its borrowings by using {swap_type} to adjust interest rate terms and currency allocations simultaneously",
    "To stabilize debt costs, {company} applies {swap_type} to manage both cash flow interest rate risk and foreign exchange risk",
    "{company} manages risk on forecasted and existing borrowings using {swap_type} to optimize interest rate and currency profiles",
]


hedge_standards = [
    "ASC 815",
    "applicable accounting guidance",
    "U.S. GAAP",
    "accounting standards",
]
