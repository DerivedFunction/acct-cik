# %%
import random
import pandas as pd
from openpyxl import load_workbook
import re
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from template.hedges import *
from template.common import *
from template.other import *

output_file = "./training_data.xlsx"
company_name_file = "./names.xlsx"
parquet_file = "./training_data.parquet"
# Precompile regex patterns
pattern_we_s = re.compile(r"We's", flags=re.IGNORECASE)
pattern_we_is = re.compile(r"We is", flags=re.IGNORECASE)
pattern_nil = re.compile(r" (0|0.0) (thousand|million|billion)", flags=re.IGNORECASE)
pattern_notional = re.compile(f"notional", flags=re.IGNORECASE)
pattern_spaces = re.compile(r"\s+")
pattern_dots = re.compile(r"\.\.")

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
    value = 0.0 if random.random() < chance else (1
    if upperlimit <= 1 else random.randint(1, upperlimit))

    if random.random() < 0.5:
        divisor = random.choice([10, 100])
        decimals = random.randint(1, 2)
        value = round(value / divisor, decimals)

    # Cast to int if it's a whole number with 50% chance
    if isinstance(value, float) and value.is_integer() and random.random() < 0.5:
        value = int(value)

    return value


def cleanup(all_sentences: list[str], reporting_year: int, checkBracket: bool = True):
    paragraph = ". ".join(all_sentences)
    pattern_we_s.sub("Our", paragraph)
    paragraph = pattern_we_is.sub("We are", paragraph)
    if random.random() < 0.25:  # Chance to replace values with nil
        paragraph = pattern_nil.sub(
            random.choice([" nil", " 0", " 0.0", " 0.00"]), paragraph
        )

    if random.random() < 0.5:
        paragraph = pattern_notional.sub("", paragraph)
    paragraph = pattern_spaces.sub(" ", paragraph)  # Remove extra whitespace
    paragraph = pattern_dots.sub("", paragraph)  # Remove double periods

    if paragraph.find("{") != -1 or (paragraph.find("[") != -1 and checkBracket):
        print("Error in format", paragraph)
    paragraph = (
        f"<reportingYear>{reporting_year}</reportingYear> "
        + ". ".join(selected_sentences)
        + "."
    )
    return paragraph
def new_label():
    return {
        "deriv": 0,  # Derivative mention
        "gen": 0,  # Hedge User
        "curr": 0,  # Current Der. user
        "hist": 0,  # Historic/Past Der. User
        "spec": 0,  # Der. Speculative mention
        "ir": 0,  # IR/Debt Context
        "fx": 0,  # FX Context
        "cp": 0,  # CP Context
        "eq": 0,  # EQ Context
        "emb": 0,  # Embedded Der. user
        "irr": 0,  # Irrelevant
    }


def generate_hedge_paragraph(has_active_derivative, swapType=None, year_range=(1990, 2025),
    max_past_years=3, include_policy=None, company_name=None):
    labels = new_label()
    # Decide whether to include policy statements
    if include_policy is None and random.random() < 0.15:
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
    else:
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
    if swapType == "cp": # A various number of commodities
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
    # Assign multi-labels
    # =====================
    labels["deriv"] = 1  # Always a derivative mention
    if swapType in ["ir", "fx", "cp", "eq"]:
        labels[swapType] = 1  # Mark the hedge context
        labels["gen"] = 1  # Always a hedge user

    # Current / Historic / Speculative
    if has_active_derivative is True:
        labels["curr"] = 1
    if has_active_derivative is False:
        labels["hist"] = 1

    if include_policy is True:
        labels["spec"] = 1

    def generate_debt():
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
        return sentence

    def generate_derivative_sentences(positionOnly=False):
        """Generate derivative-related sentences for FX, IR, CP, or generic types."""
        sentences = []

        # --- Common fields ---
        verb = random.choice(hedge_use_verbs)
        swap_type = random.choice(swap_types)
        cost_type = random.choice(cost_types)
        hedge_type = random.choice(hedge_types)
        month = random.choice(months)
        end_day = random.randint(28, 31)
        quarter = random.choice(quarters)

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
            sentences.append(generate_debt())

        template = random.choice(hedge_position_templates[swapType])
        # --- Time logic ---
        year = current_year if has_active_derivative else current_year - 1
        prev_year, prev2_year = year - 1, year - 2
        old_year = random.choice(past_years) - 1 if past_years else prev_year
        future_year = (
            random.randint(current_year + 1, current_year + 5)
            if has_active_derivative
            else random.randint(old_year - 1, prev_year)
        )

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
            swap_types=selected_swap_list,
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
        if not has_active_derivative:
            sentences.extend(expire_hedge())
        # --- Chance of payment
        if random.random() < 0.15:
            sentences.extend(hedge_payment())
        return sentences

    def expire_hedge():
        labels["hist"] = 1
        # pick a random template from termination
        template = random.choice(hedge_termination_templates)
        swap_type = random.choice(swap_types)
        term_year = random.choice(past_years) if past_years else current_year
        verb = random.choice(hedge_use_verbs)
        sentence = template.format(
            company=pick_company_name(company_name),
            swap_type=swap_type,
            month=random.choice(months),
            year=term_year,
            end_day=random.randint(28, 31),
            verb=verb,
        )
        return [sentence]

    def hedge_payment():
        # pick a random template from payment
        template = random.choice(hedge_payment_templates)
        swap_type = random.choice(swap_types)
        notional = generate_value(False)
        sentence = template.format(
            company=pick_company_name(company_name),
            swap_type=swap_type,
            notional=notional,
            currency_code=currency_code,
            money_unit=money_units,
        )
        return [sentence]

    def hedge_policy():
        sentences = []
        # Accounting policy (always)
        act_template = random.choice(hedge_policy_templates)
        swap_type = (
            random.choice(swap_types) if random.random() < 0.5 else "derivatives"
        )
        hedge_type = random.choice(hedge_types)
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
                doc_template.format(
                    company=pick_company_name(company_name), hedge_type=hedge_type
                )
            )
        # Chance of hedge effectiveness or hedge ineffectiveness (frequency, verb, swap_type, method, metric, standard)
        if random.random() < 0.5:
            eff_template = random.choice(hedge_effectiveness_templates)
            verb = random.choice(assessment_verbs)
            swap_type = random.choice(swap_types)
            method = random.choice(hedge_methods)
            metric = random.choice(hedge_metrics)
            standard = random.choice(hedge_standards)
            sentences.append(
                eff_template.format(
                    company=pick_company_name(company_name),
                    verb=verb,
                    swap_type=swap_type,
                    method=method,
                    metric=metric,
                    standard=standard,
                )
            )
        else: # company, freqency
            ineff_template = random.choice(hedge_ineffectiveness_templates)
            frequency = random.choice(frequencies)
            sentences.append(
                ineff_template.format(
                    company=pick_company_name(company_name),
                    frequency=frequency,
                )
            )
        return sentences

    def hedge_type_policy():
        sentences = []
        # begin context template (company, verb)
        beg_ctx_template = random.choice(hedge_begin_context_templates[swapType])
        verb = random.choice(hedge_use_verbs) if has_active_derivative else random.choice(hedge_may_use_verbs)
        sentences.append(
            beg_ctx_template.format(
                company=pick_company_name(company_name),
                verb=verb,
            )
        )
        # mitigation template
        ctx_template = random.choice(hedge_mitigation_templates[swapType])
        sentences.append(
            ctx_template.format(
                company=pick_company_name(company_name),
                verb=verb,
            )
        )

    # Main Execution
    if has_active_derivative is None:
        all_sentences.extend(hedge_policy())
    else:
        all_sentences.extend(generate_derivative_sentences())
        # Chance to include policy
        if include_policy:
            all_sentences.extend(hedge_type_policy())

    return cleanup(all_sentences, current_year)
