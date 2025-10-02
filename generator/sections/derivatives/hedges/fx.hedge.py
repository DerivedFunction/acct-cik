fx_types = [
    "forward rate agreement",
    "forward rate contract",
    "forward rate option",
    "forward foreign exchange contract",
    "forward foreign exchange rate contract",
    "foreign exchange contract",
    "foreign exchange rate contract",
    "foreign exchange forward",
    "foreign exchange forward contract",
    "foreign exchange rate forward",
    "foreign exchange future",
    "foreign exchange swap",
    "foreign exchange rate swap",
    "foreign exchange option",
    "foreign exchange cap",
    "foreign exchange floor",
    "foreign exchange collar",
    "cross-currency swap",
    "cross-currency forward",
    "cross-currency option",
    "cross currency swap",
    "cross currency forward",
    "cross currency option",
    "currency swap",
    "currency forward",
    "currency option",
    "currency cap",
    "currency floor",
    "currency collar",
    "foreign currency forward",
    "foreign currency forward contract",
    "foreign currency purchased put option",
]
fx_strategy_templates = [
    "{company} entered into {swap_type} as part of a collar strategy to limit exposure to foreign currency fluctuations within a defined range",
    "Collar strategies utilizing {swap_type} were implemented to provide downside protection while capping upside exposure to currency movements",
    "{company} established collar positions through {swap_type} to manage foreign exchange risk on forecasted transactions",
    "As part of its risk management program, {company} uses collar strategies combining {swap_type} to hedge currency exposure",
    "In {month} {year}, {company} implemented {swap_type} within a collar strategy to limit foreign currency risk",
    "{company} utilized {swap_type} in a collar structure to manage exposure to currency fluctuations",
    "Collar strategies with {swap_type} were employed to hedge foreign exchange risk on international transactions",
    "{company} entered into {swap_type} as part of a collar to cap currency exposure while retaining some upside potential",
    "in the {quarter} quarter of {year}, {swap_type} were used in a collar strategy to mitigate foreign currency volatility",
    "{company} implemented collar positions with {swap_type} to stabilize foreign exchange impacts",
    "{swap_type} were utilized in a collar strategy to limit currency risk on forecasted revenue",
    "{company} established {swap_type} within a collar framework to manage foreign exchange exposure",
    "Collar strategies involving {swap_type} were used to hedge currency fluctuations in {year}",
    "{company} employed {swap_type} in a collar structure to protect against adverse currency movements",
    "In {month} {year}, {swap_type} were implemented as part of a collar to manage currency risk",
    "{swap_type} within a collar strategy were used to limit exposure to foreign exchange volatility",
    "{company} utilized collar positions with {swap_type} to hedge currency risk on international contracts",
    "in the {quarter} quarter of {year}, {company} entered into {swap_type} as part of a collar to manage forex exposure",
    "Collar strategies with {swap_type} were implemented to stabilize currency impacts on forecasted transactions",
    "{company} used {swap_type} in a collar framework to cap foreign exchange risk while retaining flexibility",
]

fx_context_templates = [
    "As a multinational corporation, {company} face exposure to changes in foreign currency values that can affect our financial position and operating results",
    "Our business is subject to risks from foreign currency fluctuations due to operations in diverse international markets",
    "{company}’s international activities result in exposure to currency exchange risks and government regulations",
    "{company}’s international operations face risks from currency exchange rate volatility and local market conditions",
    "Foreign currency transaction exposures arising on external and internal trade flows are selectively hedged",
]

fx_impact_templates = [
    "Depending on the direction of change relative to {major_currency}, foreign currency values can {verb} the reported dollar value of our net assets and results of operations",
    "Fluctuations in exchange rates {verb} our reported revenues, expenses, assets, and liabilities when translated into {major_currency}",
    "Changes in foreign currency exchange rates relative to {major_currency} {verb} both our financial position and operating performance",
    "Currency movements {verb} the dollar value of our international cash flows and balance sheet items denominated in foreign currencies",
    "Foreign exchange rate fluctuations {verb} the reported value of our international assets and liabilities in {major_currency}",
    "Changes in currency exchange rates {verb} the financial results and net asset values reported in {major_currency}",
    "Movements in foreign currency values {verb} our consolidated financial statements when translated into {major_currency}",
    "Exchange rate volatility {verb} the reported dollar value of our international revenues and expenses",
    "Foreign currency fluctuations {verb} the translated value of our assets, liabilities, and operating results",
    "Changes in exchange rates relative to {major_currency} {verb} our financial position and reported earnings",
    "Currency exchange rate movements {verb} the dollar value of our international operations and balance sheet",
    "Fluctuations in foreign currencies {verb} our reported financial performance and net asset values",
    "Exchange rate changes {verb} {major_currency} value of our international cash flows and financial position",
    "Foreign currency movements {verb} the reported value of our global revenues and balance sheet items",
    "Changes in foreign exchange rates {verb} the dollar-denominated value of our international operations",
    "Currency fluctuations {verb} our consolidated financial results and net asset positions",
    "Movements in exchange rates {verb} the reported value of our international assets and operating results",
    "Foreign currency changes {verb} {major_currency} value of our global financial statements",
    "Exchange rate volatility {verb} the translated financial results of our international subsidiaries",
    "Changes in currency values {verb} the reported dollar value of our global operations and financial position",
]

fx_mitigation_templates = [
    "{company} selectively hedges foreign exchange exposures resulting from cross-border trade flows and intercompany transactions",
    "Transaction exposures from external trade and internal group transactions are managed through selective hedging programs",
    "{company} hedges foreign currency transaction risk arising from both third-party and intercompany commercial activities",
    "{company} {verb} to reduce foreign currency transaction exposure by matching currency inflows and outflows at the subsidiary level",
    "To mitigate transaction risk, {company} {verb} natural hedging strategies by matching local currency revenues with local currency costs",
    "{company}'s objective is to minimise the exposure of overseas operating subsidiaries to transaction risk by matching local currency income with local currency costs where possible",
    "{company}'s objective is to minimize transaction risk exposure by aligning local currency revenues with local currency expenses in its foreign operations",
    "{company}'s internal trading transactions are matched centrally and inter-company payment terms are managed to reduce foreign currency risk",
    "Intercompany transactions are centrally netted and payment terms are optimized to minimize foreign exchange exposure",
    "{company} operates a central matching system for internal trade flows to reduce gross foreign currency exposures",
    "{company} centrally manages intercompany trading positions and payment schedules to mitigate currency risk",
    "Where possible, {company} manages the cash surpluses or borrowing requirements of subsidiary companies centrally using {swap_type} to hedge future repayments back into the originating currency",
    "{company} centrally manages subsidiary liquidity and uses {swap_type} to hedge foreign exchange exposure on intercompany funding arrangements",
    "Subsidiary cash positions are managed centrally with {swap_type} hedging the repatriation of funds to originating currencies",
    "{company} employs {swap_type} to hedge foreign currency risk on centrally managed subsidiary funding and cash movements",
    "{company} may use {swap_type} to adjust the currency profile of its debt portfolio as needed",
    "{company} employs {swap_type} to modify the currency composition of borrowings based on operational needs",
    "{swap_type} are utilized to convert borrowings into {major_currency} when strategically beneficial",
    "{swap_type} not designated as hedges, failing to be hedges or failing to continue as effective hedges are included in operations as {swap_type} gains or losses",
    "Discounts or premiums on {swap_type} designated and effective as hedges are amortized or accreted to expense using the straight-line method over the term of the related contract",
    "Discounts or premiums on {swap_type} not designated or effective as hedges are included in the mark to market adjustment and recognized in income as {swap_type} gains or losses",
]


fx_currency_template = [
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

fx_alternative_management_templates = [
    "Depending on market conditions, foreign currency risk is also managed through the use of foreign currency debt",
    "{company} may use foreign currency-denominated debt as a natural hedge against foreign currency exposure",
    "In certain circumstances, {company} utilize foreign currency borrowings to offset translation exposure",
    "Foreign currency debt may be used strategically to create natural hedging relationships",
]

fx_generic_hedge_templates = [
    '{company} may choose to hedge against possible fluctuations in foreign subsidiaries net assets ("{hedge_type} hedge") and {verb} {swap_type} and {swap_type} in the past in order to hedge such an exposure',
    "From time to time, {company} {verb} {swap_type} to hedge {hedge_type} in foreign operations",
    "{hedge_type} hedges {verb} to protect the value of {company}'s investments in foreign subsidiaries from adverse currency movements",
    "{company} {verb} derivative instruments designated as {hedge_type} hedges to mitigate currency translation risk on foreign operations",
]

fx_specific_hedge_templates = [
    "Includes forward purchases with a notional amount of {notional_currency} {notional_amount} {money_unit} expiring in {expiry_year}, designated as a fair value hedge of the exposure of an equivalent amount of {hedged_item} to fluctuations in the {currency_pair} spot rate",
    "{company} designated {swap_type} with a notional value of {notional_currency} {notional_amount} {money_unit} expiring in {expiry_year} as fair value hedges against exposure to {currency_pair} exchange rate movements on {hedged_item}",
    "Forward contracts totaling {notional_currency} {notional_amount} {money_unit} and expiring in {expiry_year} were designated as hedges of {notional_currency} {notional_amount} {money_unit} of {hedged_item} against {currency_pair} fluctuations",
    "{swap_type} with notional amounts of {notional_currency} {notional_amount} {money_unit} maturing in {expiry_year} hedge the {currency_pair} exposure on {hedged_item}",
]

cash_pooling_templates = [
    "{company} also operates cash pooling arrangements to manage the surplus cash and short-term liquidity needs of foreign subsidiaries located outside {major_currency} zone",
    "{company} operates cash pooling arrangements to optimize liquidity management across foreign subsidiaries and reduce external borrowing costs",
    "Cash pooling structures are utilized to centralize cash management and provide efficient funding to international operations",
    "{company} maintains centralized cash pooling facilities to manage working capital needs of subsidiaries in various currencies",
]

# Foreign Exchange (foreign exchange) Debt Optimization Templates
fx_debt_optimization_templates = [
    "{company} employs {instrument_list} to adjust the currency composition of its debt portfolio, managing exposure to {currency_code} fluctuations",
    "To hedge foreign exchange risk, {company} uses {instrument_list} to convert borrowings from {currency_code} into its functional currency",
    "{company} applies {instrument_list} to manage foreign exchange exposure on international debt, mitigating translation and transaction risk",
    "Foreign currency borrowings are optimized using {instrument_list} to reduce volatility from {currency_code} exchange rate movements",
    "To manage currency risk, {company} utilizes {instrument_list} to modify the currency mix of its debt obligations",
    "{company} uses {instrument_list} to convert debt from {currency_code} into other currencies as part of its foreign exchange risk management strategy",
    "The company employs {instrument_list} to hedge foreign currency exposure on its international debt portfolio",
    "To stabilize the currency profile of debt, {company} applies {instrument_list} converting obligations into {currency_code} where beneficial",
    "{company} manages foreign exchange risk on long-term borrowings by using {instrument_list} to adjust the currency allocation",
    "To reduce foreign exchange volatility, {company} utilizes {instrument_list} to optimize the composition of multi-currency debt",
]
