# %%
import random
import pandas as pd
from openpyxl import load_workbook
import re
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import json

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
pattern_dots = re.compile(r"\.+")

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


def cleanup(all_sentences: list[str], reporting_year: int, checkBracket: bool = True):
    """
    Join sentences into a paragraph and apply sanitizing regexes.
    Fixed: assign results of regex.sub back to paragraph so substitutions take effect.
    """
    paragraph = ""
    try:
        paragraph = ". ".join(all_sentences)
    except:
        print(all_sentences)

    # Apply substitutions and assign back to paragraph
    paragraph = pattern_we_s.sub("Our", paragraph)
    paragraph = pattern_we_is.sub("We are", paragraph)

    if random.random() < 0.25:  # Chance to replace values with nil
        paragraph = pattern_nil.sub(
            random.choice([" nil", " 0", " 0.0", " 0.00"]), paragraph
        )

    if random.random() < 0.5:
        paragraph = pattern_notional.sub("", paragraph)

    paragraph = pattern_spaces.sub(" ", paragraph)  # Remove extra whitespace
    paragraph = pattern_dots.sub(".", paragraph)  # Remove double periods

    if (
        paragraph.find("{") != -1
        or paragraph.find("..") != -1
        or (paragraph.find("[") != -1 and checkBracket)
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
        return 3

    # --- Derivative Warrants ---
    if labels.get("warr"):
        return 5 if labels.get("hist") else 4

    # --- Embedded Derivatives ---
    if labels.get("emb"):
        return 7 if labels.get("hist") else 6

    # --- Hedge types mapping ---
    hedge_map = {
        "ir": (8, 9, 14),
        "fx": (10, 11, 15),
        "cp": (12, 13, 16),
        "eq": (0, 1, 2),
        "gen": (0, 1, 2),
    }

    # Check actual use first
    for hedge_type in ["ir", "fx", "cp", "eq", "gen"]:
        if labels.get(f"{hedge_type}_use"):
            curr_id, hist_id, spec_id = hedge_map[hedge_type]
            if labels.get("curr"):
                return curr_id
            if labels.get("hist"):
                return hist_id
            if labels.get("spec"):
                return spec_id
            # Default fallback to current if only _use is flagged
            return curr_id

    # Check speculative mention without actual use
    for hedge_type in ["ir", "fx", "cp", "eq", "gen"]:
        if labels.get(hedge_type) and labels.get("spec"):
            return hedge_map[hedge_type][2]

    # Check context only (no actual use)
    for hedge_type in ["ir", "fx", "cp", "eq", "gen"]:
        if labels.get(hedge_type):
            return hedge_map[hedge_type][0]  # default to current

    # Default fallback to irrelevant
    return 3


def new_label():
    return {
        # -----------------
        # Context / Mention flags
        # -----------------
        "ir": 0,  # Interest rate derivative mentioned
        "fx": 0,  # FX derivative mentioned
        "cp": 0,  # Commodity derivative mentioned
        "eq": 0,  # Equity derivative mentioned
        "gen": 0,  # Generic derivative mention (not type-specific)
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
    has_active_derivative,
    swapType=None,
    year_range=(1990, 2025),
    max_past_years=3,
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
    labels[swapType] = 1  # Context for the specific hedge type

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
        swap_type = random.choice(swap_types)
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
        swap_type = random.choice(swap_types)
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

    # Main Execution
    if has_active_derivative is None:
        if swapType is not None:
            # Specific hedge type policy
            all_sentences.extend(hedge_type_policy())
        else:
            # Generic policy if no hedge type is given
            all_sentences.extend(hedge_policy())
    else:
        all_sentences.extend(generate_derivative_sentences())
        # Chance to include policy
        if include_policy:
            all_sentences.extend(hedge_type_policy())

    label = get_primary_label(labels)
    return cleanup(all_sentences, current_year), labels, label


def generate(size_per_label=100, max_workers=8):
    """
    Generate the dataset. Fixed:
      - Ensure DataFrame columns match the tuple order appended to all_samples.
      - Convert the 'labels' dict column to JSON strings before sorting.
      - Add a defensive assertion that each item is (sentence, labels_dict, label_int).
    """
    all_samples = []
    swap_types = ["ir", "fx", "cp", "gen"]
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

        return futures

    # --- Parallel execution with tqdm progress bar ---
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = submit_tasks(executor)
        for future in tqdm(
            as_completed(futures),
            total=len(futures),
            desc="Generating samples",
        ):
            paragraph, labels, label = future.result()
            # Defensive checks to catch wrong tuple order early
            assert isinstance(paragraph, str), "expected paragraph string as first item"
            assert isinstance(labels, dict), "expected labels dict as second item"
            assert isinstance(label, (int,)), "expected integer label as third item"
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
