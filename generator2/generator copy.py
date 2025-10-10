# %%
import random
import pandas as pd
from openpyxl import load_workbook
import re
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from template.hedges import *

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

# company_name_df = pd.read_excel(company_name_file)
# company_names = list(company_name_df["name"])


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


def cleanup(paragraph: str, reporting_year: int, checkBracket: bool = True):
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
        "deriv": 0, # Derivative mention
        "ir": 0, # IR Hedge user
        "fx": 0, # FX Hedge user
        "cp": 0, # CP Hedge user
        "equity": 0, # EQ Hedge user
        "embed": 0, # Embedded Der. user
        "curr": 0, # Current Der. user
        "hist": 0, # Historic/Past Der. User
        "spec": 0, # Der. Speculative mention
        "debt_ctx": 0, # Debt/IR context
        "fx_ctx": 0, # FX context
        "eq_ctx": 0, # EQ context (ex. stocks)
        "comm_ctx": 0, # CP context (ex. fuel)
        "emb_ctx": 0, # Embedded Der. context
        "gen_ctx": 0, # Generic/ Der. context
        "irrelevant": 0, # Irrelevant
    }
# Already imported
# ir_position_templates = generate_hedge_position_templates("ir")
# fx_position_templates = generate_hedge_position_templates("fx")
# cp_position_templates = generate_hedge_position_templates("cp")
# eq_position_templates = generate_hedge_position_templates("eq")
# gen_position_templates = generate_hedge_position_templates("gen")
# derivative_keywords

