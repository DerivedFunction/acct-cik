# %%
import random
import pandas as pd
from openpyxl import load_workbook
import re
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import json
import multiprocessing as mp

from template.hedges import *
from template.common import *
from template.other import *
from template.w_emb import *

output_file = "./training_data.xlsx"
company_name_file = "./names.xlsx"
parquet_file = "./training_data.parquet"
# Precompile regex patterns
pattern_we_s = re.compile(r"We's", flags=re.IGNORECASE)
pattern_we_is = re.compile(r"We is", flags=re.IGNORECASE)
pattern_nil = re.compile(r" (0|0.0) (thousand|million|billion)", flags=re.IGNORECASE)
pattern_notional = re.compile(f"notional", flags=re.IGNORECASE)
pattern_spaces = re.compile(r"\s+")
pattern_dots = re.compile(r"\. +")

company_name_df = pd.read_excel(company_name_file)
company_names = list(company_name_df["name"])

def pick_company_name(company_name: str) -> str:
    return random.choices([company_name, "The Company"], weights=[0.75, 0.25], k=1)[0]


def generate_value(haveZero=True, upperlimit=1000):
    """Generate a random previous notional value with chance of being zero,
    and optional rounding for variability. Returns int if whole, else float."""
    if haveZero:
        chance = 0.1
    else:
        chance = 0

    upperlimit = int(upperlimit)
    value = (
        0.0
        if random.random() < chance
        else (1 if upperlimit <= 1 else random.randint(1, upperlimit))
    )

    if random.random() < 0.5:
        divisor = random.choice([10, 100])
        decimals = random.randint(1, 2)
        value = round(value / divisor, decimals)

    # Cast to int if it's a whole number with 50% chance
    if isinstance(value, float) and value.is_integer() and random.random() < 0.5:
        value = int(value)

    return value


def cleanup(all_sentences: list[str], reporting_year: int, fullCheck: bool = True):
    """
    Join sentences into a paragraph and apply sanitizing regexes.
    Fixed: assign results of regex.sub back to paragraph so substitutions take effect.
    """
    paragraph = ""
    # Capitalize each sentence
    for i in range(len(all_sentences)):
        all_sentences[i] = all_sentences[i].capitalize()
    try:
        paragraph = ". ".join(all_sentences)
    except:
        print(all_sentences)

    # Apply substitutions and assign back to paragraph
    paragraph = pattern_we_s.sub("Our", paragraph)
    paragraph = pattern_we_is.sub("We are", paragraph)

    if random.random() < 0.25:  # Chance to replace values with nil
        paragraph = pattern_nil.sub(
            random.choice([" nil", " 0", " 0.0", " 0.00"]),
            paragraph,
        )

    if random.random() < 0.5:
        paragraph = pattern_notional.sub("", paragraph)
        
    paragraph = pattern_dots.sub(". ", paragraph)  # Remove double periods
    paragraph = pattern_spaces.sub(" ", paragraph)  # Remove extra whitespace
    
    if (
        fullCheck and (
        paragraph.find("{") != -1
        or paragraph.find(".." ) != -1
        or paragraph.find("[") != -1
        )
    ):
        print("Error in format", paragraph)

    paragraph = f"<reportingYear>{reporting_year}</reportingYear> {paragraph}."
    return paragraph


def get_primary_label(labels: dict) -> int:
    """
    Convert multi-hot label dict into a single categorical label.

    Prioritization:
      1. Actual use (_use) → Current or Historic
      2. Speculative mentions (spec)
      3. Context only (no _use) → Current
      4. Irrelevant
    """

    # --- Irrelevant override ---
    if labels.get("irr"):
        return 19

    # --- Derivative Warrants ---
    if labels.get("warr"):
        return 16 if labels.get("hist") else 15

    # --- Embedded Derivatives ---
    if labels.get("emb"):
        return 18 if labels.get("hist") else 17

    # --- Hedge type label map ---
    hedge_map = {
        "gen": (0, 1, 2),
        "ir": (3, 4, 5),
        "fx": (6, 7, 8),
        "cp": (9, 10, 11),
        "eq": (12, 13, 14),
    }

    # --- 1. Check for actual use ---
    for hedge_type in hedge_map.keys():
        if labels.get(f"{hedge_type}_use"):
            curr_id, hist_id, spec_id = hedge_map[hedge_type]
            if labels.get("curr"):
                return curr_id
            if labels.get("hist"):
                return hist_id
            if labels.get("spec"):
                return spec_id
            # Default to current if _use flagged but no time context
            return curr_id

    # --- 2. Speculative mention (no actual use) ---
    for hedge_type in hedge_map.keys():
        if labels.get(hedge_type) and labels.get("spec"):
            return hedge_map[hedge_type][2]

    # --- 3. Context only (no _use, not speculative) ---
    for hedge_type in hedge_map.keys():
        if labels.get(hedge_type):
            return hedge_map[hedge_type][0]

    # --- 4. Default fallback ---
    return 19


def new_label():
    return {
        # -----------------
        # Context / Mention flags
        # -----------------
        "ir": 0,  # Interest rate context mentioned
        "fx": 0,  # FX context mentioned
        "cp": 0,  # Commodity context mentioned
        "eq": 0,  # Equity context mentioned
        "gen": 0,  # Generic derivative context mention (not type-specific)
        # -----------------
        # Actual use flags
        # -----------------
        "ir_use": 0,  # Actively used interest rate derivative
        "fx_use": 0,  # Actively used FX derivative
        "cp_use": 0,  # Actively used commodity derivative
        "eq_use": 0,  # Actively used equity derivative
        "gen_use": 0,  # Actively used generic derivative (any hedge)
        # -----------------
        # Time / Status flags
        # -----------------
        "curr": 0,  # Current derivative user
        "hist": 0,  # Historic/past derivative user
        "spec": 0,  # Speculative mention (not confirmed use)
        # -----------------
        # Special derivative types
        # -----------------
        "warr": 0,  # Warrants
        "emb": 0,  # Embedded derivatives
        "irr": 0,  # Irrelevant / not a hedge
        # -----------------
        # Optional overall derivative flag
        # -----------------
        "deriv": 0,  # Any derivative mention (context + use)
    }


def generate_hedge_paragraph(
    has_active_derivative: bool,
    swapType=None,
    year_range=(1990, 2025),
    max_past_years: int = 3,
    include_policy=None,
    company_name=None,
):
    labels = new_label()
    # Decide whether to include policy statements
    if include_policy is None and random.random() < 0.35:
        include_policy = True

    # If has_active_derivative not given, default to speculative/policy
    if has_active_derivative is None:
        include_policy = True

    # Pick company name
    if company_name is None:
        company_name = (
            random.choice(company_names) if random.random() < 0.95 else "The Company"
        )

    # Determine swap type if not provided
    if swapType is None:
        swapType = random.choice(["ir", "fx", "cp", "eq", "gen"])
    swap_types = derivative_keywords[swapType]

    # Currency and year setup
    money_units = random.choice(money_unit_list)
    currency_code = random.choice(currency_codes)
    major_currency = random.choice(all_currencies)

    current_year = random.randint(year_range[0], year_range[1])
    reporting_year = current_year
    num_past_years = random.randint(1, max_past_years)
    past_years = sorted(
        random.sample(range(current_year - 5, current_year), num_past_years)
    )
    month = random.choice(months)
    end_day = random.randint(28, 31)
    quarter = random.choice(quarters)

    cost_type = random.choice(cost_types)
    hedge_type = random.choice(hedge_types)
    swap_type = random.choice(swap_types)

    # Swaps Setup
    swaps_list = []
    for _ in range(3):
        swaps_list.append(random.choice(swap_types))
        if random.random() < 0.5:
            break
    swaps = (
        ", ".join(swaps_list[:-1]) + " and " + swaps_list[-1]
        if len(swaps_list) > 1
        else swaps_list[0]
    )

    # Commodity setup
    commodity = random.choice(commodities)
    selected_cps = ""
    if swapType == "cp":  # A various number of commodities
        cp_list = [commodity if not commodity == "commodity" else commodity]
        for _ in range(2):
            cp_list.append(random.choice(commodities))
            if random.random() < 0.5:
                break
        selected_cps = (
            ", ".join(cp_list[:-1]) + " and " + cp_list[-1]
            if len(cp_list) > 1
            else cp_list[0]
        )
        selected_cps = selected_cps if random.random() < 0.85 else "commodity"
    all_sentences = []

    # =====================
    # Assign multi-labels. The training data is only specific, but we need to watch out during actual model classification
    # =====================
    # Initialize labels
    labels = new_label()

    # Always mark a derivative mention
    labels["deriv"] = 1
    
    # -----------------------
    # Actual use
    # -----------------------
    if has_active_derivative is not None:
        # Mark specific hedge type as used
        labels[f"{swapType}_use"] = 1

        # Mark generic hedge use
        labels["gen_use"] = 1

        # Mark current vs historic
        if has_active_derivative:
            labels["curr"] = 1
        else:
            labels["hist"] = 1

    # -----------------------
    # Speculative mention
    # -----------------------
    if include_policy:
        # Only set spec if not actively using (optional, depends on your logic)
        labels["spec"] = 1

    def generate_debt() -> list[str]:
        sentences = []
        debt_type_list = []
        # Build the debt type combination
        for _ in range(3):
            debt_type_list.append(random.choice(debt_types_list))
            if random.random() < 0.95:
                break
        selected_debt = (
            ", ".join(debt_type_list[:-1]) + " and " + debt_type_list[-1]
            if len(debt_type_list) > 1
            else debt_type_list[0]
        )
        for _ in range(random.randint(1, 3)):
            template = random.choice(debt_templates)
            amount = generate_value(False)
            amount2 = generate_value(False)
            pct = generate_value(False, 8)
            pct2 = generate_value(False, 20)
            outstanding = random.randint(0, int(amount) // 2)
            debt_type = random.choice(debt_types_list)
            maturity_year = current_year + random.randint(3, 10)
            years = random.randint(3, 10)
            sentence = template.format(
                amount=amount,
                amount2=amount2,
                year=maturity_year,
                month=month,
                outstanding=outstanding,
                current_year=current_year,
                debt_types=selected_debt,
                debt_type=debt_type,
                maturity_year=maturity_year,
                company=pick_company_name(company_name),
                currency_code=currency_code,
                major_currency=major_currency,
                money_unit=money_units,
                end_day=end_day,
                pct=pct,
                pct2=pct2,
                years=years,
                hedge_type=hedge_type,
            )
            sentences.append(sentence)
        return sentences

    def generate_derivative_sentences() -> list[str]:
        labels[swapType] = 1  # Context for the specific hedge type
        """Generate derivative-related sentences for FX, IR, CP, or generic types."""
        sentences = []

        # --- Common fields ---
        verb = random.choice(hedge_use_verbs)

        # --- FX: add currency description sentence (0-1 chance) ---
        if swapType == "fx" and random.random() < 0.6:
            selected = random.sample(major_currencies, random.randint(2, 3))
            if random.random() < 0.5:
                selected += random.sample(european_currencies, random.randint(1, 2))
            if random.random() < 0.4:
                selected += random.sample(asian_currencies, random.randint(1, 2))
            if random.random() < 0.3:
                selected += random.sample(americas_currencies, random.randint(1, 2))
            selected = list(dict.fromkeys(selected))
            currency_list = (
                ", ".join(selected[:-1]) + " and " + selected[-1]
                if len(selected) > 1
                else selected[0]
            )
            if random.random() < 0.3:
                currency_list += " and other European and Latin American currencies"
            sentences.append(
                random.choice(fx_currency_templates).format(
                    company=pick_company_name(company_name),
                    currencies=currency_list,
                )
            )
            # IR: Add a chance of debt
        if swapType == "ir" and random.random() < 0.15:
            sentences.extend(generate_debt())

        template = random.choice(hedge_position_templates[swapType])
        # --- Time logic ---
        if has_active_derivative:
            year = current_year
        else:
            # 50-50 chance: current year or previous year
            year = current_year if random.random() < 0.5 else current_year - 1

        prev_year, prev2_year = year - 1, year - 2
        old_year = random.choice(past_years) if past_years else prev_year

        future_year = (
            random.randint(current_year + 1, current_year + 5)
            if has_active_derivative
            else random.randint(old_year - 1, prev_year)
        )

        # --- Notionals ---
        notional = generate_value(False) if has_active_derivative else 0

        # Previous notionals can still have some values for context
        prev_notional = generate_value()
        prev2_notional = generate_value()
        old_notional = generate_value(False)

        # --- Notionals ---
        notional = (
            generate_value(False)
            if has_active_derivative
            else (generate_value(False) if random.random() < 0.5 else 0)
        )
        prev_notional = generate_value()
        prev2_notional = generate_value()
        old_notional = generate_value(False)
        # --- Build main sentence ---
        sentence = template.format(
            company=pick_company_name(company_name),
            verb=verb,
            swap_type=swap_type,
            swap_types=swaps,
            commodity=commodity,
            month=month,
            end_day=end_day,
            quarter=quarter,
            year=year,
            prev_year=prev_year,
            prev2_year=prev2_year,
            old_year=old_year,
            future_year=future_year,
            currency_code=currency_code,
            notional=notional,
            prev_notional=prev_notional,
            prev2_notional=prev2_notional,
            old_notional=old_notional,
            money_unit=money_units,
            cost_type=cost_type,
            hedge_type=hedge_type,
        )
        sentences.append(sentence)

        # --- Expired hedges for non-active derivatives ---
        if not has_active_derivative and random.random() < 0.05:
            sentences.append(expire_hedge())
        # --- Chance of payment
        if random.random() < 0.15:
            sentences.append(hedge_payment())

        random.shuffle(sentences)
        return sentences

    def expire_hedge() -> str:
        labels["hist"] = 1
        # pick a random template from termination
        template = random.choice(hedge_termination_templates)
        term_year = random.choice(past_years) if past_years else current_year
        verb = random.choice(hedge_use_verbs)
        sentence = template.format(
            company=pick_company_name(company_name),
            swap_type=swap_type,
            month=random.choice(months),
            quarter=quarter,
            year=term_year,
            end_day=random.randint(28, 31),
            verb=verb,
        )
        return sentence

    def hedge_payment() -> str:
        # pick a random template from payment
        template = random.choice(hedge_payment_templates)
        notional = generate_value(False)
        sentence = template.format(
            company=pick_company_name(company_name),
            swap_type=swap_type,
            notional=notional,
            currency_code=currency_code,
            money_unit=money_units,
            month=month,
        )
        return sentence

    def hedge_policy() -> list[str]:
        labels["spec"] = 1 #  A speculation
        labels[swapType] = 0 # Not related to any swap
        sentences = []
        # Accounting policy (always)
        act_template = random.choice(hedge_policy_templates)
        swap_type = (
            random.choice(swap_types) if random.random() < 0.5 else "derivatives"
        )
        sentences.append(
            act_template.format(
                company=pick_company_name(company_name),
                swap_type=swap_type,
                hedge_type=hedge_type,
            )
        )
        # No trading policy (always)
        nt_template = random.choice(hedge_no_trading_templates)
        sentences.append(
            nt_template.format(
                company=pick_company_name(company_name),
                verb=random.choice(hedge_may_use_verbs),
            )
        )

        # Chance of documentation:
        if random.random() < 0.5:
            doc_template = random.choice(hedge_documentation_templates)
            sentences.append(
                doc_template.format(company=pick_company_name(company_name), hedge_type=hedge_type)
            )
        # Chance of hedge effectiveness or hedge ineffectiveness (frequency, verb, swap_type, method, metric, standard)
        if random.random() < 0.5:
            eff_template = random.choice(hedge_effectiveness_templates)
            verb = random.choice(assessment_verbs)
            method = random.choice(hedge_methods)
            metric = random.choice(hedge_metrics)
            standard = random.choice(hedge_standards)
            frequency = random.choice(frequencies)
            sentences.append(
                eff_template.format(
                    company=pick_company_name(company_name),
                    verb=verb,
                    swap_type=swap_type,
                    method=method,
                    metric=metric,
                    standard=standard,
                    frequency=frequency,
                    hedge_type=hedge_type,
                )
            )
        else:  # company, freqency
            ineff_template = random.choice(hedge_ineffectiveness_templates)
            frequency = random.choice(frequencies)
            sentences.append(
                ineff_template.format(
                    company=pick_company_name(company_name),
                    frequency=frequency,
                )
            )
        # Risk
        if random.random() < 0.5:
            materiality_choice = random.choice(materiality)
            template = random.choice(risk_templates)
            item = (
                random.choice(swap_types)
                if random.random() < 0.5
                else random.choice(risk_items_derivative)
            )
            template.format(
                item=item,
                company=pick_company_name(company_name),
                materiality=materiality_choice,
            )
            sentences.append(template)
        random.shuffle(sentences)
        return sentences

    def hedge_type_policy() -> list[str]:
        labels[swapType] = 1
        labels["spec"] = 1
        sentences = []
        # begin context template (company, verb)
        beg_ctx_template = random.choice(hedge_begin_context_templates[swapType])
        verb = (
            random.choice(hedge_use_verbs)
            if has_active_derivative
            else random.choice(hedge_may_use_verbs)
        )
        sentences.append(
            beg_ctx_template.format(
                company=pick_company_name(company_name),
                verb=verb,
                swap_type=swaps,
                commodities=selected_cps,
            )
        )
        # mitigation template
        ctx_template = random.choice(hedge_mitigation_templates[swapType])
        sentences.append(
            ctx_template.format(
                company=pick_company_name(company_name),
                verb=verb,
                swap_type=swaps,
                commodity=selected_cps,
            )
        )
        random.shuffle(sentences)
        return sentences

    def generate_hedge_policy_update():
        sentences = []
        labels["deriv"] = 1
        labels["spec"] = 1
        labels[swapType] = 0 # Not related to any swap
        # ==============================
        # 1. ISSUANCE STATEMENT
        # ==============================
        template = random.choice(hedge_change_policy_templates)
        issuer = random.choice(shared_issuers)
        standard = random.choice(hedge_standards)
        topic = random.choice(
            [
                "derivatives and hedging",
                "hedging activities",
                "cash flow hedges",
                "fair value hedges",
            ]
        )
        purpose = random.choice(shared_purposes)
        description = random.choice(hedging_descriptions)
        extra = random.choice(hedging_additional_features)

        issue_month = random.choice(months)
        issue_year = random.randint(current_year - 8, current_year)
        effective_year = issue_year + random.randint(2, 4)
        eff_month = random.choice(months)
        eff_day = random.randint(15, 31)

        issuance_sentence = template.format(
            month=issue_month,
            year=issue_year,
            issuer=issuer,
            standard=standard,
            topic=topic,
            purpose=purpose,
            description=description,
            additional_feature=extra,
            eff_month=eff_month,
            eff_day=eff_day,
            eff_year=effective_year,
            company=pick_company_name(company_name),
        )
        sentences.append(issuance_sentence)

        # Optional: Add effective date
        if random.random() < 0.25:
            eff_line = random.choice(shared_effective_date_templates).format(
                company=pick_company_name(company_name),
                month=eff_month,
                day=random.randint(15, 31),
                end_day=random.randint(15, 31),
                year=effective_year,
            )
            sentences.append(eff_line)

        # Optional: Add transition/disclosure/practical expedient
        if random.random() < 0.2:
            trans_line = random.choice(shared_transition_templates).format(
                company=pick_company_name(company_name),
                method=random.choice(shared_adoption_methods),
                feature=random.choice(shared_transition_features),
            )
            sentences.append(trans_line)

        if random.random() < 0.2:
            disclosure_line = random.choice(shared_disclosure_change_templates).format(
                company=pick_company_name(company_name),
                disclosure_topic=random.choice(
                    ["derivative disclosures", "risk management strategies"]
                ),
                disclosure_topic2=random.choice(
                    ["hedge effectiveness", "notional amounts"]
                ),
                year=effective_year,
            )
            sentences.append(disclosure_line)

        if random.random() < 0.15:
            expedient_line = random.choice(shared_practical_expedient_templates).format(
                company=pick_company_name(company_name),
                expedient_description=random.choice(shared_transition_features),
            )
            sentences.append(expedient_line)

        # ==============================
        # 2. ADOPTION STATEMENT
        # ==============================
        adopt_template = random.choice(shared_adoption_status_templates)
        adopt_standard = random.choice(hedge_standards)
        adopt_method = random.choice(shared_adoption_methods)
        adopt_month = random.choice(months)
        adopt_day = random.randint(1, 28)
        adopt_year = random.randint(current_year - 8, current_year + 4)

        adoption_sentence = adopt_template.format(
            company=pick_company_name(company_name),
            standard=adopt_standard,
            method=adopt_method,
            month=adopt_month,
            day=adopt_day,
            year=adopt_year,
        )
        sentences.append(adoption_sentence)

        # Optional: Adoption impact
        if random.random() < 0.25:
            impact_line = random.choice(shared_adoption_impact_templates).format(
                company=pick_company_name(company_name),
                impact=random.choice(
                    [
                        "a reduction in earnings volatility",
                        "an increase in OCI from effective hedge portions",
                        "no material impact on the consolidated financial statements",
                    ]
                ),
            )
            sentences.append(impact_line)

        # ==============================
        # 3. EVALUATION STATEMENT
        # ==============================
        evaluation_sentence = random.choice(shared_evaluation_templates).format(
            company=pick_company_name(company_name)
        )
        sentences.append(evaluation_sentence)

        # Optional: Recently issued pronouncement
        if random.random() < 0.2:
            pronouncement = random.choice(shared_recent_pronouncement_templates).format(
                company=pick_company_name(company_name),
                issuer=random.choice(shared_issuers),
                standard=random.choice(hedge_standards),
                topic=random.choice(
                    [
                        "hedging relationships",
                        "cash flow hedge presentation",
                        "fair value hedge accounting",
                    ]
                ),
                month=random.choice(months),
                year=random.randint(current_year - 2, current_year),
                adoption_year=random.randint(current_year, current_year + 3),
            )
            sentences.append(pronouncement)

        return sentences

    # Main Execution
    if has_active_derivative is None:
        if swapType is not None:
            # Specific hedge type policy
            all_sentences.extend(hedge_type_policy())
        else:
            # Generic policy if no hedge type is given
            if random.random() < 0.65:
                all_sentences.extend(hedge_policy())
            else:
                all_sentences.extend(generate_hedge_policy_update())
    else:
        all_sentences.extend(generate_derivative_sentences())
        # Chance to include policy
        if include_policy:
            all_sentences.extend(hedge_type_policy())

    label = get_primary_label(labels)
    return cleanup(all_sentences, current_year), labels, label

def generate_warrant_paragraph(
    use_case,  # 'current', 'historical', or 'speculative'
    year_range=(1990, 2025),
    max_past_years: int = 3,
    company_name=None,
):
    labels = new_label()
    labels['warr'] = 1
    labels['deriv'] = 1

    if use_case == 'current':
        labels['curr'] = 1
    elif use_case == 'historical':
        labels['hist'] = 1
    elif use_case == 'speculative':
        labels['spec'] = 1

    # Setup common variables
    if company_name is None:
        company_name = random.choice(company_names) if random.random() < 0.95 else "The Company"

    money_units = random.choice(money_unit_list)
    currency_code = random.choice(currency_codes)

    current_year = random.randint(year_range[0], year_range[1])
    reporting_year = current_year
    num_past_years = random.randint(1, max_past_years)
    past_years = sorted(random.sample(range(current_year - 5, current_year), num_past_years))
    month = random.choice(months)
    end_day = random.randint(28, 31)

    # Warrant specific variables
    shares = generate_value(False, 1000000)
    price = generate_value(False, 100)
    expiry_year = current_year + random.randint(1, 10)
    amount = generate_value(False)
    settlement_year = random.choice(past_years) if past_years else current_year - 1

    # Select template pool
    if use_case == 'current':
        template_pool = sum(warrant_templates_for_ml['current_use'], [])
    elif use_case == 'historical':
        template_pool = sum(warrant_templates_for_ml['historical_use'], [])
    else: # speculative
        template_pool = sum(warrant_templates_for_ml['speculative'], [])

    if not template_pool:
        return None, None, None

    template = random.choice(template_pool)

    # Format sentence
    replacements = {
        "{company}": pick_company_name(company_name),
        "{shares}": str(shares),
        "{currency_code}": currency_code,
        "{price}": str(price),
        "{expiry_year}": str(expiry_year),
        "{month}": month,
        "{end_day}": str(end_day),
        "{year}": str(current_year),
        "{amount}": str(amount),
        "{money_unit}": money_units,
        "{settlement_year}": str(settlement_year),
        "{current_year}": str(current_year),
        "{quarter}": random.choice(quarters),
    }

    sentence = template
    for key, value in replacements.items():
        sentence = sentence.replace(key, value)

    all_sentences = [sentence]

    label = get_primary_label(labels)
    paragraph = cleanup(all_sentences, reporting_year)
    # If it has teh words shares or stock, mark it as equity
    if paragraph.find("stock") != -1 or paragraph.find("share") != -1 or paragraph.find("equit") != -1:
        labels["eq"] = 1
    return paragraph, labels, label

def generate_emb_paragraph(
    use_case,  # 'current', 'historical', or 'speculative'
    year_range=(1990, 2025),
    max_past_years: int = 3,
    company_name=None,
):
    labels = new_label()
    labels['emb'] = 1
    labels['deriv'] = 1

    if use_case == 'current':
        labels['curr'] = 1
    elif use_case == 'historical':
        labels['hist'] = 1
    elif use_case == 'speculative':
        labels['spec'] = 1

    # Setup common variables
    if company_name is None:
        company_name = random.choice(company_names) if random.random() < 0.95 else "The Company"

    money_units = random.choice(money_unit_list)
    currency_code = random.choice(currency_codes)

    current_year = random.randint(year_range[0], year_range[1])
    reporting_year = current_year
    prev_year = current_year - 1
    num_past_years = random.randint(1, max_past_years)
    past_years = sorted(random.sample(range(current_year - 5, current_year), num_past_years))
    month = random.choice(months)
    end_day = random.randint(28, 31)

    # Embedded deriv specific variables
    amount = generate_value(False)
    prev_amount = generate_value(False)
    principal = generate_value(False, 1000000)
    embedded_fv = generate_value(False, int(principal/10)) if principal > 0 else 0

    # Select template pool
    if use_case == 'current':
        template_pool = sum(embedded_templates_for_ml['current_use'], [])
    elif use_case == 'historical':
        template_pool = sum(embedded_templates_for_ml['historical_use'], [])
    else: # speculative
        template_pool = sum(embedded_templates_for_ml['speculative'], [])

    if not template_pool:
        return None, None, None

    template = random.choice(template_pool)

    # Format sentence
    replacements = {
        "{company}": pick_company_name(company_name),
        "{currency_code}": currency_code,
        "{month}": month,
        "{end_day}": str(end_day),
        "{year}": str(current_year),
        "{prev_year}": str(prev_year),
        "{amount}": str(amount),
        "{prev_amount}": str(prev_amount),
        "{money_unit}": money_units,
        "{current_year}": str(current_year),
        "{settlement_year}": str(random.choice(past_years) if past_years else current_year - 1),
        "{currency_pair}": f"{random.choice(currency_codes)}/{random.choice(currency_codes)}",
        "{principal}": str(principal),
        "{embedded_fv}": str(embedded_fv),
        "{target}": random.choice(company_names),
        "{price}": str(generate_value(False, 100)),
        "{shares}": str(generate_value(False, 1000000)),
        "{expiry_year}": str(current_year + random.randint(1, 10)),
        "{quarter}": random.choice(quarters)
    }

    sentence = template
    for key, value in replacements.items():
        sentence = sentence.replace(key, value)

    all_sentences = [sentence]

    label = get_primary_label(labels)
    paragraph = cleanup(all_sentences, reporting_year)
    # If it has teh words shares or stock, mark it as equity
    if (
        paragraph.find("stock") != -1
        or paragraph.find("share") != -1
        or paragraph.find("equit") != -1
    ):
        labels["eq"] = 1
    return paragraph, labels, label


def generate_sec_noise():
    # Generate random data for placeholders
    company = random.choice(company_names)
    month = random.choice(months)
    year = random.randint(1990, 2025)
    currency_unit = random.choice(money_unit_list)
    reporting_year = year

    # Inner function to generate a line for the Table of Contents
    def generate_toc_line():
        template = random.choice(sec_toc_patterns)
        page_num = random.randint(1, 200)
        return template.format(page=page_num, company=pick_company_name(company))

    # Populate placeholders for the phrase templates
    placeholders = {
        "file_number": str(random.randint(1, 99999)).zfill(5),
        "section": random.choice(["13", "15(d)"]),
        "area_code": random.randint(100, 999),
        "phone_number": f"{random.randint(100, 999)}-{random.randint(1000, 9999)}",
        "month": month,
        "day": random.randint(28, 31),
        "day2": random.randint(28, 31),
        "year": year,
        "prev_year": year - 1,
        "next_year": year + 1,
        "company": company,
        "choice1": random.choice(["[x]", "[]"]),
        "choice2": random.choice(["[x]", "[]"]),
        "currency_unit": currency_unit,
        "market_value": f"{random.randint(10**6, 10**9):,}",
        "shares_outstanding": f"{random.randint(50_000_000, 200_000_000):,}",
        "date": f"{random.randint(1, 12)}/{random.randint(1, 28)}/{random.randint(2000, 2024)}",
    }

    # Format phrases from templates
    phrases = [p.format(**placeholders) for p in sec_phrases]

    # Generate gibberish filename
    gibberish = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=random.randint(6, 12))
    ) + random.choice([".htm", ".txt"])

    # Combine all parts and randomly sample
    chunks = random.sample(
        headers + phrases + [gibberish] + [generate_toc_line()], k=random.randint(8, 15)
    )

    # Create paragraph and labels for compatibility
    labels = new_label()
    labels["irr"] = 1
    label = get_primary_label(labels)

    # Cleanup and return
    return cleanup(chunks, reporting_year, fullCheck=False), labels, label


def generate_noise_paragraph(
    noise_type,
    year_range=(1990, 2025),
    max_past_years: int = 3,
    company_name=None,
):
    labels = new_label()
    labels['irr'] = 1

    # Setup common variables
    if company_name is None:
        company_name = random.choice(company_names) if random.random() < 0.95 else "The Company"

    money_units = random.choice(money_unit_list)
    currency_code = random.choice(currency_codes)
    major_currency = random.choice(all_currencies)

    current_year = random.randint(year_range[0], year_range[1])
    reporting_year = current_year
    num_past_years = random.randint(1, max_past_years)
    past_years = sorted(random.sample(range(current_year - 5, current_year), num_past_years))
    month = random.choice(months)
    end_day = random.randint(28, 31)
    quarter = random.choice(quarters)
    prev_year = current_year - 1

    # Specific variables for noise templates
    amount = generate_value(False)
    prev_amount = generate_value(False)
    shares = generate_value(False, 1000000)
    price = generate_value(False, 100)
    expiry_year = current_year + random.randint(1, 10)
    event = random.choice(warrant_events)
    net_shares = generate_value(False, int(shares/2)) if shares > 0 else 0
    pct = generate_value(False, 100)
    pct2 = generate_value(False, 100)
    outstanding = generate_value(False)
    debt_types = random.choice(debt_types_list)
    maturity_year = current_year + random.randint(3, 10)
    years = random.randint(3, 10)

    def generate_other_policy_update():
        sentences = []

        # ==============================
        # 1. ISSUANCE STATEMENT
        # ==============================
        template = random.choice(general_policy_templates)
        issuer = random.choice(shared_issuers)
        standard = random.choice(other_standards)
        topic = random.choice(other_topics)
        purpose = random.choice(shared_purposes)
        description = random.choice(general_descriptions)
        extra = random.choice(general_additional_features)

        issue_month = random.choice(months)
        issue_year = random.randint(current_year - 5, current_year)
        effective_year = issue_year + random.randint(2, 4)
        eff_month = random.choice(months)
        eff_day = random.randint(15, 31)

        issuance_sentence = template.format(
            month=issue_month,
            year=issue_year,
            issuer=issuer,
            standard=standard,
            topic=topic,
            standard_purpose=purpose,
            policy_description=description,
            policy_feature=extra,
            eff_month=eff_month,
            eff_day=eff_day,
            eff_year=effective_year,
            company=pick_company_name(company_name),
        )
        sentences.append(issuance_sentence)

        # Optional: Add effective date, transition, disclosure, expedient
        if random.random() < 0.3:
            eff_line = random.choice(shared_effective_date_templates).format(
                company=pick_company_name(company_name),
                month=eff_month,
                day=random.randint(1, 28),
                end_day=random.randint(15, 31),
                year=effective_year,
            )
            sentences.append(eff_line)

        if random.random() < 0.2:
            trans_line = random.choice(shared_transition_templates).format(
                company=pick_company_name(company_name),
                adoption_method=random.choice(shared_adoption_methods),
                transition_feature=random.choice(shared_transition_features),
            )
            sentences.append(trans_line)

        if random.random() < 0.25:
            disclosure_line = random.choice(shared_disclosure_change_templates).format(
                company=pick_company_name(company_name),
                disclosure_topic=random.choice(
                    [
                        "lease assets",
                        "revenue recognition policies",
                        "credit loss assumptions",
                    ]
                ),
                disclosure_topic2=random.choice(
                    ["disaggregation of revenue", "allowance methodology"]
                ),
                year=effective_year,
            )
            sentences.append(disclosure_line)

        if random.random() < 0.15:
            expedient_line = random.choice(shared_practical_expedient_templates).format(
                company=pick_company_name(company_name),
                expedient_description=random.choice(shared_transition_features),
            )
            sentences.append(expedient_line)

        # ==============================
        # 2. ADOPTION STATEMENT
        # ==============================
        adopt_template = random.choice(shared_adoption_status_templates)
        adopt_standard = random.choice(other_standards)
        adopt_method = random.choice(shared_adoption_methods)
        adopt_month = random.choice(months)
        adopt_day = random.randint(1, 28)
        adopt_year = random.randint(current_year - 8, current_year + 4)

        adoption_sentence = adopt_template.format(
            company=pick_company_name(company_name),
            standard=adopt_standard,
            adoption_method=adopt_method,
            month=adopt_month,
            day=adopt_day,
            year=adopt_year,
        )
        sentences.append(adoption_sentence)

        # Optional: Adoption impact
        if random.random() < 0.3:
            impact_line = random.choice(shared_adoption_impact_templates).format(
                company=pick_company_name(company_name),
                adoption_impact=random.choice(
                    [
                        "recognition of additional lease liabilities",
                        "a change in timing of revenue recognition",
                        "no material impact on consolidated results",
                    ]
                ),
            )
            sentences.append(impact_line)

        # ==============================
        # 3. EVALUATION STATEMENT
        # ==============================
        evaluation_sentence = random.choice(shared_evaluation_templates).format(
            company=pick_company_name(company_name)
        )
        sentences.append(evaluation_sentence)

        # Optional: Recently issued pronouncement
        if random.random() < 0.25:
            pronouncement = random.choice(shared_recent_pronouncement_templates).format(
                company=pick_company_name(company_name),
                issuer=random.choice(shared_issuers),
                standard=random.choice(other_standards),
                topic=random.choice(other_topics),
                month=random.choice(months),
                year=random.randint(current_year - 2, current_year),
                adoption_year=random.randint(current_year, current_year + 3),
            )
            sentences.append(pronouncement)

        # Risk
        materiality_choice = random.choice(materiality)
        template = random.choice(risk_templates)
        item = random.choice(risk_items_other)
        sentence = template.format(
            risk_item=item,
            company=pick_company_name(company_name),
            materiality=materiality_choice,
        )
        sentences.append(sentence)
        return sentences

    template_pool = []
    all_sentences = []
    if noise_type == "eq" or noise_type == "warr":  # ex. equity, warrant, stock
        labels["eq"] = 1
        template_pool.extend(sum(noise_templates["EQ"], []))
    elif noise_type == "cp":  # ex. inventory
        labels["cp"] = 1
        template_pool.extend(sum(noise_templates["CP"], []))
    elif noise_type == "ir":  # ex. debt
        labels["ir"] = 1
        template_pool.extend(sum(noise_templates["IR"], []))
    elif noise_type == "fx":  # ex. currency
        labels["fx"] = 1
        template_pool.extend(sum(noise_templates["FX"], []))
    elif noise_type == "deriv":  # ex. derivative lawsuits (irr)
        template_pool.extend(sum(noise_templates["LAW"], []))
    elif noise_type == "spec":  # ex. acct standards (irr)
        all_sentences = generate_other_policy_update()
    else:
        # Everything else can be mixed together
        template_pool.extend(other_templates)
    if not template_pool and not all_sentences:
        return None, None, None

    # Commodity setup
    commodity = random.choice(commodities)
    cp_list = [commodity if not commodity == "commodity" else commodity]
    for _ in range(2):
        cp_list.append(random.choice(commodities))
        if random.random() < 0.5:
            break
    selected_cps = (
        ", ".join(cp_list[:-1]) + " and " + cp_list[-1]
        if len(cp_list) > 1
        else cp_list[0]
    )
    selected_cps = selected_cps if random.random() < 0.85 else "commodity"

    replacements = {
        "{company}": pick_company_name(company_name),
        "{shares}": str(shares),
        "{shares1}": str(generate_value(False, 1000000)),
        "{shares2}": str(generate_value(False, 1000000)),
        "{currency_code}": currency_code,
        "{price}": str(price),
        "{price2}": str(generate_value(False, 100)),
        "{expiry_year}": str(expiry_year),
        "{month}": month,
        "{end_day}": str(end_day),
        "{year}": str(current_year),
        "{prev_year}": str(prev_year),
        "{prev_month}": random.choice(months),
        "{amount}": str(amount),
        "{prev_amount}": str(prev_amount),
        "{money_unit}": money_units,
        "{event}": event,
        "{value1}": str(generate_value(False)),
        "{value2}": str(generate_value(False)),
        "{net_shares}": str(net_shares),
        "{quarter}": quarter,
        "{financing_type}": random.choice(financing_types),
        "{days}": str(random.randint(30, 180)),
        "{pct}": str(pct),
        "{pct2}": str(pct2),
        "{asset_type}": random.choice(asset_types),
        "{debt_types_list}": random.choice(debt_types_list),
        "{service_type}": random.choice(service_types),
        "{commodities}": selected_cps,
        "{inventory_method}": random.choice(inventory_methods),
        "{reserve}": str(generate_value(False)),
        "{outstanding}": str(outstanding),
        "{debt_types}": debt_types,
        "{debt_type}": random.choice(debt_types_list),
        "{maturity_year}": str(maturity_year),
        "{years}": str(years),
        "{ratio}": str(random.randint(2, 5)),
        "{coverage}": str(random.randint(2, 5)),
        "{major_currency}": major_currency,
        "{currency2}": random.choice(all_currencies),
        "{currency3}": random.choice(all_currencies),
        "{location}": random.choice(balance_sheet_locations),
        "{reported_pct}": str(generate_value(False, 100)),
        "{low_price}": str(generate_value(False, 50)),
        "{high_price}": str(generate_value(False, 200)),
        "{unit}": random.choice(volume_units),
        "{volume}": str(generate_value(False, 100000)),
        "{cost}": str(generate_value(False, 100)),
        "{prev_cost}": str(generate_value(False, 100)),
        "{change}": str(generate_value(False)),
        # New specific placeholders
        "{bs_reason}": random.choice(balance_sheet_reasons),
        "{wc_reason}": random.choice(balance_sheet_reasons),
        "{ap_reason}": random.choice(balance_sheet_reasons),
        "{accrued_reason}": random.choice(accrued_reasons),
        "{asset_reason}": random.choice(other_asset_reasons),
        "{liability_reason}": random.choice(liability_reasons),
        "{equity_reason}": random.choice(equity_reasons),
        "{cfs_reason}": random.choice(cfs_reasons),
        "{capex_purpose}": random.choice(capex_purposes),
        "{restructuring_purpose}": random.choice(restructuring_purposes),
        "{restructuring_expense_type}": random.choice(restructuring_expense_types),
        "{acquisition_purpose}": random.choice(acquisition_purposes),
        "{acquisition_funding}": random.choice(acquisition_funding),
        "{guarantee_type}": random.choice(guarantee_types),
        "{intangible_type_examples}": random.choice(intangible_types),
        "{tax_sources_examples}": random.choice(tax_sources),
        "{litigation_examples}": random.choice(case_types),
        "{lawsuit_allegation}": random.choice(allegations),
        "{court_name}": random.choice(courts),
        "{standard_purpose}": random.choice(shared_purposes),
        "{standard_description}": random.choice(general_descriptions),
        "{policy_description}": random.choice(general_descriptions),
        "{policy_feature}": random.choice(general_additional_features),
        "{hedge_description}": random.choice(hedging_descriptions),
        "{hedge_feature}": random.choice(hedging_additional_features),
        "{competitive_characteristics}": random.choice(competitive_characteristics),
        "{competitive_factors}": random.choice(competitive_factors),
        "{competitive_pressure_reasons}": random.choice(competitive_pressure_reasons),
        "{competitive_advantages}": random.choice(competitive_advantages),
        "{regulatory_agencies}": random.choice(regulators),
        "{regulatory_areas}": random.choice(regulatory_areas),
        "{regulatory_approvals}": random.choice(regulatory_approvals),
        "{regulatory_matters}": random.choice(regulatory_matters),
        "{self_insured_risks}": random.choice(self_insured_risks),
        "{insurance_incident}": random.choice(insurance_incidents),
        "{insurance_coverage_types}": random.choice(coverage_types),
        "{adoption_method}": random.choice(shared_adoption_methods),
        "{transition_feature}": random.choice(shared_transition_features),
        "{adoption_impact}": random.choice(adoption_impacts),
    }

    for _ in range(3, 4):
        template = random.choice(template_pool)
        sentence = template
        all_placeholders = re.findall(r'{\w+}', sentence)
        for key in all_placeholders:
            value = replacements.get(key, "a relevant value")
            sentence = sentence.replace(key, str(value))
        all_sentences.append(sentence)
    # Fix any remaining placeholders
    for idx, _ in enumerate(all_sentences):
        for key, value in replacements.items():
            all_sentences[idx] = all_sentences[idx].replace(key, str(value))
    label = get_primary_label(labels)
    paragraph = cleanup(all_sentences, reporting_year, fullCheck=False)
    if paragraph.find("warrants") != -1: # Sometimes warrants will appear
        labels["warr"] = 1
    return paragraph, labels, label

def generate(size_per_label=100):
    """
    Generate the dataset. Fixed:
      - Ensure DataFrame columns match the tuple order appended to all_samples.
      - Convert the 'labels' dict column to JSON strings before sorting.
      - Add a defensive assertion that each item is (sentence, labels_dict, label_int).
    """
    all_samples = []
    swap_types = ["ir", "fx", "cp", "eq", "gen"]
    numSwaps = len(swap_types)
    count = size_per_label // numSwaps
    swap_counts = count * 3

    def submit_tasks(executor):
        futures = []
        # Parallel hedge generation
        for prefix in swap_types:
            for _ in range(swap_counts):
                futures.append(
                    executor.submit(
                        generate_hedge_paragraph,
                        has_active_derivative=True,
                        swapType=prefix,
                    )
                )
            for _ in range(swap_counts):
                futures.append(
                    executor.submit(
                        generate_hedge_paragraph,
                        has_active_derivative=False,
                        swapType=prefix,
                    )
                )
            for _ in range(count):
                futures.append(
                    executor.submit(
                        generate_hedge_paragraph,
                        has_active_derivative=None,
                        swapType=prefix,
                    )
                )
        for _ in range(count):
            futures.append(
                executor.submit(
                    generate_hedge_paragraph,
                    has_active_derivative=None,
                    swapType=None,
                )
            )

        # Warrant and Embedded Derivative Generation
        warr_emb_count = count * 2 
        for _ in range(warr_emb_count):
            futures.append(executor.submit(generate_warrant_paragraph, use_case='current'))
            futures.append(executor.submit(generate_warrant_paragraph, use_case='historical'))
            futures.append(executor.submit(generate_warrant_paragraph, use_case='speculative'))
            futures.append(executor.submit(generate_emb_paragraph, use_case='current'))
            futures.append(executor.submit(generate_emb_paragraph, use_case='historical'))
            futures.append(executor.submit(generate_emb_paragraph, use_case='speculative'))

        # Noise Generation
        noise_count = count * 2
        noise_types = ['eq', 'cp', 'ir', 'fx']
        for _ in range(noise_count):
            for noise_type in noise_types:
                futures.append(executor.submit(generate_noise_paragraph, noise_type=noise_type))
        for _ in range(size_per_label): # Any random noise
            futures.append(executor.submit(generate_noise_paragraph, noise_type=None))
        
        for _ in range(10):
            futures.append(executor.submit(generate_sec_noise))
        return futures

    # --- Parallel execution with tqdm progress bar ---
    with ThreadPoolExecutor(max_workers=max(mp.cpu_count() * 2, 8)) as executor:
        futures = submit_tasks(executor)
        for future in tqdm(
            as_completed(futures),
            total=len(futures),
            desc="Generating samples",
        ):
            result = future.result()
            if result and result[0] is not None:
                paragraph, labels, label = result
                # Defensive checks to catch wrong tuple order early
                assert isinstance(paragraph, str), "expected paragraph string as first item"
                assert isinstance(labels, dict), "expected labels dict as second item"
                assert isinstance(label, int), "expected integer label as third item"
                all_samples.append((paragraph, labels, label))

    # --- Create and sort DataFrame ---
    # IMPORTANT: tuple order is (sentence, labels_dict, label_int) so columns must match that order
    df_new = pd.DataFrame(all_samples, columns=["sentence", "labels", "label"])

    # Convert labels dicts → JSON strings for Excel compatibility
    df_new["labels"] = df_new["labels"].apply(json.dumps)

    # Sort by numeric label and sentence text (both are hashable/scalar)
    df_new.sort_values(by=["label", "sentence"], ascending=[True, True], inplace=True)
    df_new.reset_index(drop=True, inplace=True)

    # --- Write or append to Excel ---
    try:
        book = load_workbook(output_file)
        with pd.ExcelWriter(
            output_file, engine="openpyxl", mode="a", if_sheet_exists="overlay"
        ) as writer:
            df_new.to_excel(writer, sheet_name="Generated_Data", index=False)
    except FileNotFoundError:
        df_new.to_excel(output_file, sheet_name="Generated_Data", index=False)

    print(f"\n{len(all_samples)} samples written/appended to {output_file} (sorted)")

generate(1000)
