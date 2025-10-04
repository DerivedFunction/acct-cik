# =============================================================================
# COMPLETE OPTIMIZED CODE
# =============================================================================

import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
import json
import sqlite3
from typing import List
import random
import re
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import multiprocessing as mp
from pathlib import Path

# Importing required module
import subprocess

# =============================================================================
# CONFIGURATION - DEFAULT
# =============================================================================
DEBUG = False
ALL_FIRMS_DATA = "derivatives_data.csv"
REPORT_CSV_PATH = "report_data_to_process.csv"
DB_PATH = "web_data.db"
SEC_RATE = 9  # requests per second
SEC_RATE_LIMIT =  1 / SEC_RATE # requests per second
CHUNK_SIZE = 500

# =============================================================================
# COLAB CONFIGURATION
# =============================================================================
DRIVE_PATH = "./drive/MyDrive/db"
LOAD_SHELL_CMD = f"cp {DB_PATH} {DRIVE_PATH}/{DB_PATH} ."
SAVE_SHELL_CMD = f"cp {DB_PATH} {DRIVE_PATH}/."
IS_COLAB = False

# Auto-detect system capabilities
def get_system_config():
    total_cores = max(mp.cpu_count() - 1, 1)
    total_fetchers = min(5, total_cores)
    if IS_COLAB and not Path(DB_PATH).exists():
        print("Loading database from Google Drive. Run again after it is loaded.")
        subprocess.run(LOAD_SHELL_CMD, shell=True)
        exit(0)
    return {
        "num_fetchers": total_fetchers,
        "num_parsers": total_cores,
        "chunk_size": CHUNK_SIZE * (5 if IS_COLAB else 1),
    }


CONFIG = get_system_config()
total_cores = mp.cpu_count()

print(f"🖥️  Detected: {total_cores} CPU cores")
print(
    f"⚙️  Configuration: {CONFIG['num_fetchers']} fetchers, {CONFIG['num_parsers']} parsers"
)
print(f"📦 Chunk size: {CONFIG['chunk_size']} reports per batch")


# =============================================================================
# REGEX PATTERNS AND KEYWORDS
# =============================================================================

IGNORE_KEYWORDS = {
    "table of contents",
    "consolidated",
    "balance sheet",
    "BEGIN PRIVACY-ENHANCED MESSAGE",
    "us-gaap:",
}

FILING_TYPES = {
    "10-K",
    "10-KT",
    "20-F",
    "40-F",
    "10-K405",
    "10KSB",
    "10KSB40",
}

PLACEHOLDERS = {
    "€": "__EURO__",
    "£": "__POUND__",
    "¥": "__YEN__",
    "¢": "__CENTS__",
}

REPLACE_HOLDERS = PLACEHOLDERS | {
    "•": "*",
    "—": "--",
    """: '"',
    """: '"',
    "'": "'",
    "'": "'",
}

# Compile regex patterns once
NON_ASCII_PATTERN = re.compile(r"[^\x00-\x7F]+")
BULLET_PATTERN = re.compile(r"^[-*•]\s*")
NUMBERED_PATTERN = re.compile(r"^\(?\d+[\.\)]\s+")
PUNCTUATION_END_PATTERN = re.compile(r"[.!?;:•)]$")
SENTENCE_SPLIT_PATTERN = re.compile(r"(?<![A-Z0-9])\s*\.\s*(?![a-zA-Z0-9])")

CRUNCHED_TEXT_PATTERNS = [
    (re.compile(r"([a-z])([A-Z])"), r"\1 \2"),
    (re.compile(r"([a-zA-Z])(\d+)"), r"\1 \2"),
    (re.compile(r"(\d+)([a-zA-Z])"), r"\1 \2"),
    (re.compile(r"([a-zA-Z0-9])(\$)"), r"\1 \2"),
]

CLEANUP_PATTERNS = [
    (re.compile(r"\s+"), " "),
    (re.compile(r"\(\s*"), "("),
    (re.compile(r"\s*\)"), ")"),
    (re.compile(r"\s*,"), ","),
    (re.compile(r"(-{3,}|={3,}|\.{3,})"), ""),
    (re.compile(r"<.*?>"), ""),
    (re.compile(r"table of contents", re.IGNORECASE), ""),
    (re.compile(r"F-\d+"), ""),
]

SEPARATOR_PATTERN = re.compile(r"[-=\s]+")
CAPTION_PATTERN = re.compile(r"<CAPTION>", re.IGNORECASE)
COLUMN_SPLIT_PATTERN = re.compile(r"\s{2,}")
TABLE_SPLIT_PATTERN = re.compile(r"(<TABLE>.*?</TABLE>)", re.DOTALL | re.IGNORECASE)

# Category regex patterns
IR_REGEX = re.compile(
    r"\binterest rate (contract|derivative|instrument|forward|future|collar|swap|option|cap|floor|lock)"
    r"|zero coupon swap|single currency basis swap|swaption\b",
    flags=re.IGNORECASE,
)

FX_REGEX = re.compile(
    r"\b(forward rate (agreement|contract|option)"
    r"|((foreign exchange|currency|cross-currency)( rate)? (contract|derivative|instrument|forward|future|swap|option|cap|floor|collar))"
    r"|forward foreign exchange)\b",
    flags=re.IGNORECASE,
)

CP_REGEX = re.compile(
    r"\bcommodity( price)? (contract|derivative|instrument|forward|future|option|cap|floor|collar|swap)\b",
    flags=re.IGNORECASE,
)

GEN_REGEX = re.compile(
    r"\b(derivative (contract|instrument|financial instrument|position|asset|liability|expense|gain|loss)"
    r"|change in fair value of derivative"
    r"|(gain|loss) on derivative"
    r"|embedded derivative"
    r"|(hedg(e|ing)|hedge(s|d)) (of|instrument|contract|derivative|relationship|accounting|program|transaction|activity)"
    r"|designated as (a |an )?((cash flow|fair value|net investment) )?hedg(e|ing)(s)?"
    r"|(instruments|contracts) are designated"
    r"|(cash flow|fair value|net investment) hedg(e|ing)"
    r"|ineffective portion"
    r"|notional (amount|value|principal|contract|exposure)?"
    r"|(forward|futures) contract"
    r"|(call|put) (option|contract)"
    r"|option contract"
    r"|(interest rate |currency |commodity |equity |credit )?swap( contract| agreement| transaction)?"
    r"|swaption"
    r"|(cap|floor|collar|lock) agreement)\b",
    flags=re.IGNORECASE,
)

SPEC_REGEX = re.compile(
    r"\b(financial derivative|may use derivatives|over[- ]the[- ]counter derivative|otc derivative|a\.s\.c\.? 815|asc 815)\b",
    flags=re.IGNORECASE,
)

CATEGORY_REGEX_ORDER = [
    ("ir", IR_REGEX),
    ("fx", FX_REGEX),
    ("cp", CP_REGEX),
    ("spec", SPEC_REGEX),
    ("gen", GEN_REGEX),
]

# =============================================================================
# LOAD DATA
# =============================================================================

all_derivatives_df = pd.read_csv(ALL_FIRMS_DATA)

# =============================================================================
# DEBUG UTILITIES
# =============================================================================

def debug_print(*args):
    global DEBUG
    if DEBUG:
        print(*args)

# =============================================================================
# DATABASE FUNCTIONS
# =============================================================================


def create_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS report_data (
                cik INTEGER,
                year INTEGER,
                url TEXT
            )
        """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS names (
                cik INTEGER,
                name TEXT
            )
        """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS webpage_result (
                url TEXT,
                matches TEXT,
                FOREIGN KEY (url) REFERENCES report_data(url)
            )
        """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS fail_results (
                cik INTEGER,
                year INTEGER,
                url TEXT,
                reason TEXT
            )
        """
        )
        c.execute("CREATE INDEX IF NOT EXISTS url_idx ON report_data (url)")
        c.execute("CREATE INDEX IF NOT EXISTS url_idx ON webpage_result (url)")
        c.execute("CREATE INDEX IF NOT EXISTS name_idx ON names (name)")
    except sqlite3.IntegrityError:
        print("Something went wrong creating the database")
    finally:
        conn.commit()
        conn.close()


def save_batch_report_urls(df):
    with sqlite3.connect(DB_PATH) as conn:
        try:
            name = df[["cik", "name"]].drop_duplicates()
            name = name.dropna()
            name["name"] = name["name"].str.title()
            name.to_sql("names", conn, if_exists="append", index=False)
        except:
            pass
        try:
            report = df[["cik", "year", "url"]]
            report.to_sql("report_data", conn, if_exists="append", index=False)
            return True
        except sqlite3.IntegrityError:
            debug_print(df.head())
            df = df[["cik", "year", "url"]]
            df["reason"] = "Error submitting batch"
            df.to_sql("fail_results", conn, if_exists="append", index=False)
            return False


def fetch_report_data(valid=True):
    try:
        return pd.read_csv(REPORT_CSV_PATH)
    except:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        if valid:
            c.execute("SELECT * FROM report_data WHERE NOT url =''")
        else:
            c.execute("SELECT * FROM report_data WHERE url =''")
        columns = [col[0] for col in c.description]
        rows = c.fetchall()
        pre_data = pd.DataFrame(rows, columns=columns)
        conn.close()
        return pre_data


def fetch_webpage_results():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM webpage_result")
    columns = [col[0] for col in c.description]
    rows = c.fetchall()
    pre_data = pd.DataFrame(rows, columns=columns)
    conn.close()
    return pre_data


def get_processed_urls() -> set:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT url FROM webpage_result")
    rows = c.fetchall()
    conn.close()
    return set(rows)


def save_process_result(df):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO webpage_result (url, matches) VALUES (?, ?)",
        (df.url, json.dumps(df.matches)),
    )
    conn.commit()
    conn.close()


# =============================================================================
# FETCH SEC FILINGS
# =============================================================================


def fetch_json(url: str) -> dict | None:
    global SEC_RATE_LIMIT
    headers = {
        "User-Agent": f"{random.randint(1000,9999)}-{random.randint(1000,9999)}@{random.randint(1000,9999)}.com"
    }
    time.sleep(SEC_RATE_LIMIT)
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        debug_print("Fetching", url)
        if resp.status_code == 429:
            print(f"Rate Limited {resp.status_code} fetching {url}")
            return None
        if resp.status_code != 200:
            print(f"Error {resp.status_code} fetching {url}")
            return None
        return resp.json()
    except Exception as e:
        print(f"Exception fetching {url}: {e}")
        return None


def extract_filings(data: dict, cik: str, name: str, ticker: str) -> List[dict]:
    links = []
    forms = data.get("form", [])
    accession_numbers = data.get("accessionNumber", [])
    primary_docs = data.get("primaryDocument", [])
    filing_dates = data.get("filingDate", [])
    report_dates = data.get("reportDate", [])

    for i, f_type in enumerate(forms):
        if f_type in FILING_TYPES:
            accession = accession_numbers[i].replace("-", "")
            doc = primary_docs[i]
            if not doc or doc.endswith("txt"):
                doc = f"{accession[:10]}-{accession[10:12]}-{accession[12:]}.txt"
            link = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{doc}"
            links.append(
                {
                    "name": name,
                    "filing_date": filing_dates[i],
                    "report_date": report_dates[i],
                    "url": link,
                    "ticker": ticker,
                    "type": f_type,
                }
            )
    return links


def get_cik_filings(cik: str) -> List[dict]:
    cik = str(cik).zfill(10)
    url_main = f"https://data.sec.gov/submissions/CIK{cik}.json"

    data = fetch_json(url_main)
    if not data:
        return None

    name = data.get("name", "")
    ticker = data.get("tickers", [])[0] if data.get("tickers", []) else cik

    recent = data.get("filings", {}).get("recent", {})
    links = extract_filings(recent, cik, name, ticker)

    older_files = data.get("filings", {}).get("files", [])
    for f in older_files:
        older_data = fetch_json(f"https://data.sec.gov/submissions/{f.get('name')}")
        if isinstance(older_data, dict):
            links.extend(extract_filings(older_data, cik, name, ticker))

    return links


# =============================================================================
# CONTENT EXTRACTION
# =============================================================================


def extract_content(data: str, asHTML=True, max_len=2000) -> str:
    if not data:
        return ""

    if asHTML:
        soup = BeautifulSoup(data, "html.parser")
        text = soup.get_text(separator="\n\n", strip=True)
        text = keep_allowed_chars(text, True)
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        merged_paragraphs = []

        i = 0
        while i < len(paragraphs):
            line = paragraphs[i]

            if BULLET_PATTERN.match(line):
                if len(line.strip()) == 1 and i + 1 < len(paragraphs):
                    line = f"{line} {paragraphs[i + 1]}"
                    i += 1

                if merged_paragraphs and BULLET_PATTERN.match(merged_paragraphs[-1]):
                    merged_paragraphs[-1] += f"\n{line}"
                else:
                    merged_paragraphs.append(line)

            elif NUMBERED_PATTERN.match(line):
                if merged_paragraphs and NUMBERED_PATTERN.match(merged_paragraphs[-1]):
                    merged_paragraphs[-1] += f"\n{line}"
                else:
                    merged_paragraphs.append(line)

            elif merged_paragraphs and not PUNCTUATION_END_PATTERN.search(
                merged_paragraphs[-1]
            ):
                merged_paragraphs[-1] += f" {line}"
            else:
                merged_paragraphs.append(line)

            i += 1

        final_paragraphs = []
        for para in merged_paragraphs:
            if len(para) <= max_len:
                final_paragraphs.append(para)
            else:
                parts = SENTENCE_SPLIT_PATTERN.split(para)
                current_chunk = ""

                for part in parts:
                    if len(current_chunk) + len(part) + 1 <= max_len:
                        current_chunk += f" {part}" if current_chunk else part
                    else:
                        if current_chunk:
                            final_paragraphs.append(current_chunk)
                        current_chunk = part

                if current_chunk:
                    final_paragraphs.append(current_chunk)

        paragraphs = final_paragraphs

    else:
        text = keep_allowed_chars(data)
        parts = TABLE_SPLIT_PATTERN.split(text)
        paragraphs = []

        for part in parts:
            if part.strip().lower().startswith("<table>"):
                rows = parse_plain_text_table_fixed(part)
                table_text = "\n".join(["\t".join(row) for row in rows])
                paragraphs.append(table_text)
            else:
                sub_paras = [p for p in re.split(r"\n\s*\n", part) if p.strip()]
                paragraphs.extend(sub_paras)

    cleaned_paragraphs = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        is_list_item = BULLET_PATTERN.match(para) or NUMBERED_PATTERN.match(para)
        if not is_list_item:
            para = re.sub(r"\n+", " ", para)

        for pattern, replacement in CRUNCHED_TEXT_PATTERNS:
            para = pattern.sub(replacement, para)

        for pattern, replacement in CLEANUP_PATTERNS:
            para = pattern.sub(replacement, para)

        para = para.strip()

        if len(para) < 15 and cleaned_paragraphs:
            cleaned_paragraphs[-1] = f"{cleaned_paragraphs[-1]} {para}"
        elif para:
            cleaned_paragraphs.append(para)

    return "\n\n".join(cleaned_paragraphs)


def keep_allowed_chars(text, asHTML=False):
    if not isinstance(text, str):
        return text

    if asHTML:
        try:
            text = text.encode("utf-8").decode("unicode_escape")
        except Exception:
            pass

    for sym, ph in REPLACE_HOLDERS.items():
        text = text.replace(sym, ph)

    text = NON_ASCII_PATTERN.sub("", text)

    for sym, ph in PLACEHOLDERS.items():
        text = text.replace(ph, sym)
    return text


def parse_plain_text_table_fixed(block: str):
    rows = []
    first_col_buffer = ""
    first_col_active = True

    lines = [line.rstrip() for line in block.splitlines() if line.strip()]

    for line in lines:
        if SEPARATOR_PATTERN.fullmatch(line) or CAPTION_PATTERN.match(line.strip()):
            continue

        if "<S>" in line:
            first_col_active = False
            line = line.replace("<S>", "").lstrip()

        if first_col_active:
            first_col_buffer = f"{first_col_buffer} {line.strip()}".strip()
            continue

        cols = [col.strip() for col in COLUMN_SPLIT_PATTERN.split(line)]

        if first_col_buffer:
            rows.append([first_col_buffer] + cols)
            first_col_buffer = ""
        else:
            rows.append(cols)

    return rows


def fetch_url(url: str, timeout: int = 10) -> str | None:
    global SEC_RATE_LIMIT
    if not url:
        return None
    try:
        time.sleep(SEC_RATE_LIMIT)
        debug_print("Fetching", url)
        resp = requests.get(
            url, timeout=timeout, headers={"User-Agent": "sync-fetch@example.com"}
        )
        if resp.status_code == 429:
            print(f"Rate Limited {resp.status_code} for {url}")
            return None
        if resp.status_code != 200:
            print(f"Error {resp.status_code} for {url}")
            return None
        return resp.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def process_url(url: str):
    raw_text = fetch_url(url)
    if not raw_text:
        debug_print(f"Error fetching {url}: No text found")
        return ""

    if url.endswith("htm"):
        debug_print("Processing as html")
        content = extract_content(raw_text, True)
    else:
        debug_print("Processing as text")
        content = extract_content(raw_text, False)
    return content


# =============================================================================
# KEYWORD FILTERING (OPTIMIZED VERSION)
# =============================================================================


def filter_by_keywords(
    content: str, min_char_length: int = 400, max_char_length=2000
) -> dict:
    """
    OPTIMIZED: Pre-filter sentences by category before expansion.
    """
    ignore_keywords = [kw.lower() for kw in IGNORE_KEYWORDS]

    def get_keyword_category(text: str) -> str:
        for category, regex in CATEGORY_REGEX_ORDER:
            if regex.search(text):
                return category
        return None

    def clean_sentence(sentence: str) -> str:
        return re.sub(r"\s+", " ", sentence.strip())

    def measure_merged_length(sentences: list) -> int:
        return len(". ".join(sentences).strip() + ".")

    def should_ignore(text: str) -> bool:
        normalized = text.lower()
        return any(kw in normalized for kw in ignore_keywords)

    def expand_context(
        all_sentences: list, target_idx: int, target_category: str
    ) -> str:
        random.seed(target_idx)
        dynamic_min = random.randint(
            int(min_char_length * 0.75), int(min_char_length * 1.25)
        )

        merged = [all_sentences[target_idx]]
        left_idx = target_idx - 1
        right_idx = target_idx + 1

        while True:
            current_length = measure_merged_length(merged)
            if current_length >= dynamic_min:
                break

            added = False

            if left_idx >= 0:
                left_sentence = all_sentences[left_idx]
                left_category = get_keyword_category(left_sentence)

                if left_category is None or left_category == target_category:
                    candidate = [left_sentence] + merged
                    if measure_merged_length(candidate) <= max_char_length:
                        merged.insert(0, left_sentence)
                        left_idx -= 1
                        added = True
                    else:
                        left_idx = -1
                else:
                    left_idx = -1

            if right_idx < len(all_sentences):
                right_sentence = all_sentences[right_idx]
                right_category = get_keyword_category(right_sentence)

                if right_category is None or right_category == target_category:
                    candidate = merged + [right_sentence]
                    if measure_merged_length(candidate) <= max_char_length:
                        merged.append(right_sentence)
                        right_idx += 1
                        added = True
                    else:
                        right_idx = len(all_sentences)
                else:
                    right_idx = len(all_sentences)

            if not added:
                break

        final_text = ". ".join(merged).strip() + "."
        if len(final_text) > max_char_length:
            excess = len(final_text) - max_char_length
            trim_left = excess // 2
            trim_right = excess - trim_left
            final_text = final_text[trim_left : len(final_text) - trim_right].strip()

        return final_text

    text = re.sub(r"\s+", " ", content.strip())
    raw_sentences = [
        s.strip()
        for s in re.split(r"(?<![A-Z0-9])\s*\.\s*(?![a-zA-Z0-9])", text)
        if s.strip()
    ]

    all_sentences = [clean_sentence(sentence) for sentence in raw_sentences]

    # Pre-categorize all sentences (KEY OPTIMIZATION)
    sentence_categories = []
    for i, sentence in enumerate(all_sentences):
        if len(sentence.split()) < 4:
            sentence_categories.append((i, None))
            continue

        category = get_keyword_category(sentence)
        sentence_categories.append((i, category))

    categorized_matches = {"ir": [], "fx": [], "cp": [], "spec": [], "gen": []}
    seen_matches = {"ir": set(), "fx": set(), "cp": set(), "spec": set(), "gen": set()}
    seen_sentences_global = set()
    # First pass: specific categories
    for i, category in sentence_categories:
        if category and category != "gen":
            if i in seen_sentences_global:
                continue

            final_sentence = expand_context(all_sentences, i, category)
            normalized = final_sentence.lower().strip()

            if should_ignore(normalized):
                continue

            if normalized not in seen_matches[category]:
                seen_matches[category].add(normalized)
                categorized_matches[category].append(final_sentence)
                seen_sentences_global.add(i)

    # Second pass: generic
    for i, category in sentence_categories:
        if category == "gen":
            if len(all_sentences[i].split()) < 6 or i in seen_sentences_global:
                continue

            final_sentence = expand_context(all_sentences, i, category)
            normalized = final_sentence.lower().strip()

            if should_ignore(normalized):
                continue

            if normalized not in seen_matches["gen"]:
                seen_matches["gen"].add(normalized)
                categorized_matches["gen"].append(final_sentence)

    debug_print(
        "Done generating sentences", sum(len(v) for v in categorized_matches.values())
    )

    return categorized_matches


# =============================================================================
# PARALLEL PROCESSING FUNCTIONS (OPTIMIZED FOR PARALLEL CORES)
# =============================================================================


def filter_by_fyear(filings: list[dict], fyear: int) -> list[dict]:
    return [
        f
        for f in filings
        if f.get("report_date") and f.get("report_date").startswith(str(fyear))
    ]


def fetch_all_grouped(saveIteration: int = 100):
    """
    Fetch filings using ProcessPoolExecutor for parallelism.
    """
    global existing_report_df, all_derivatives_df

    records = []

    if existing_report_df is None or existing_report_df.empty:
        existing_report_df = pd.DataFrame(columns=["cik", "year"])

    already_done = set(zip(existing_report_df["cik"], existing_report_df["year"]))
    cik_groups = all_derivatives_df.groupby("cik")["year"].apply(list).reset_index()

    def process_cik(row):
        cik = row.cik
        years = row.year
        cik_records = []

        years_to_fetch = [y for y in years if (cik, y) not in already_done]
        if not years_to_fetch:
            return cik_records

        debug_print("Fetching", years_to_fetch)
        filings = get_cik_filings(cik)
        if filings is None:
            print("Error fetching filings for", cik)
            return cik_records

        for fyear in years_to_fetch:
            year_filings = filter_by_fyear(filings, fyear)
            for filing in year_filings:
                cik_records.append({"cik": cik, "year": fyear, **filing})

        for year in years:
            if (cik, year) not in already_done:
                cik_records.append({"cik": cik, "year": year, "url": ""})

        return cik_records

    # Use fewer workers for SEC API to avoid rate limiting
    with ProcessPoolExecutor(max_workers=5) as executor:
        future_to_cik = {
            executor.submit(process_cik, row): i
            for i, row in enumerate(cik_groups.itertuples(index=False), start=1)
        }

        for future in tqdm(as_completed(future_to_cik), total=len(future_to_cik)):
            i = future_to_cik[future]
            try:
                cik_records = future.result()
                records.extend(cik_records)

                if i % saveIteration == 0 and records:
                    save_batch_report_urls(pd.DataFrame(records))
                    debug_print(f"Saved {len(records)} urls to database")
                    records = []
            except Exception as exc:
                print(f"CIK processing generated an exception: {exc}")

    if records:
        save_batch_report_urls(pd.DataFrame(records))
        print(f"Saved {len(records)} urls to database")

    return fetch_report_data()


def fetch_content_only(url: str):
    """
    Fetch and extract content only (I/O bound).
    Runs in fetcher pool with 5 workers.
    """
    # Check if already processed
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM webpage_result WHERE url = ?", (url,))
    exists = c.fetchone()
    conn.close()

    if exists:
        return None

    try:
        raw_text = fetch_url(url)
        if not raw_text:
            # Cooldown after having nothing
            time.sleep(SEC_RATE_LIMIT)
            return None

        # Extract content
        if url.endswith("htm"):
            content = extract_content(raw_text, True)
        else:
            content = extract_content(raw_text, False)

        return (url, content) if content else None
    except Exception as e:
        print(f"Fetch error for {url}: {e}")
        return None


def parse_content_only(data):
    """
    Parse pre-fetched content (CPU bound).
    Runs in parser pool with 35 workers.
    """
    if data is None:
        return None

    url, content = data

    try:
        # CPU-intensive parsing
        sentences = filter_by_keywords(content, 2000)
        matches = []
        matches.extend(sentences["ir"])
        matches.extend(sentences["fx"])
        matches.extend(sentences["cp"])
        matches.extend(sentences["spec"])
        matches.extend(sentences["gen"])

        result_row = pd.Series({"url": url, "matches": matches})

        save_process_result(result_row)
        return True
    except Exception as e:
        print(f"Parse error for {url}: {e}")
        return None


def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    elif minutes > 0:
        return f"{int(minutes)}m {int(seconds)}s"
    else:
        return f"{int(seconds)}s"


def calculate_rate_limit(num_fetchers, max_requests_per_sec=SEC_RATE):
    """
    Calculate per-worker delay to stay under global rate limit

    Examples:
        - 1 worker,  4.5 req/sec: each waits 0.22s → 4.5 req/sec total ✓
        - 3 workers, 4.5 req/sec: each waits 0.67s → 4.5 req/sec total ✓
        - 5 workers, 4.5 req/sec: each waits 1.11s → 4.5 req/sec total ✓
    """
    return num_fetchers / max_requests_per_sec


def process_all_reports_fully():
    global SEC_RATE_LIMIT

    processed_set = get_processed_urls()

    reports_to_process = [
        (r.url)
        for r in existing_report_df.itertuples(index=False)
        if (r.url,) not in processed_set and r.url
    ]

    total_reports = len(reports_to_process)
    print(f"Processing {total_reports:,} new reports")
    print(f"Already processed: {len(processed_set):,} reports")

    CHUNK_SIZE = CONFIG["chunk_size"]
    NUM_FETCHERS = CONFIG["num_fetchers"]
    NUM_PARSERS = CONFIG["num_parsers"]
    SEC_RATE_LIMIT = calculate_rate_limit(NUM_FETCHERS)
    print(f"\n⚙️  Rate Limiting Configuration:")
    print(f"  • {NUM_FETCHERS} parallel fetchers")
    print(f"  • Each worker waits {SEC_RATE_LIMIT:.2f}s between requests")
    print(f"  • Effective rate: ~{NUM_FETCHERS / SEC_RATE_LIMIT:.2f} req/sec")
    print(f"  • Target limit: {SEC_RATE_LIMIT:.2f} req/sec")
    total_results = 0
    total_empty = 0

    chunks = [
        reports_to_process[i : i + CHUNK_SIZE]
        for i in range(0, total_reports, CHUNK_SIZE)
    ]

    print(f"\nProcessing in {len(chunks)} chunks of {CHUNK_SIZE} reports each")
    print("=" * 70)

    chunk_times = []
    total_time = 0

    for chunk_idx, chunk in enumerate(chunks, 1):
        current_time = time.time()
        print(f"\n📦 Chunk {chunk_idx}/{len(chunks)} ({len(chunk)} reports)")

        # Stage 1: Fetch this chunk
        print(f"  → Fetching with {NUM_FETCHERS} workers...")
        fetched_data = []

        with ProcessPoolExecutor(max_workers=NUM_FETCHERS) as fetch_executor:
            fetch_futures = [
                fetch_executor.submit(fetch_content_only, url)
                for url in chunk
            ]

            for future in tqdm(
                as_completed(fetch_futures),
                total=len(fetch_futures),
                desc=f"  Fetching chunk {chunk_idx}",
                leave=False,
            ):
                try:
                    result = future.result()
                    if result:
                        fetched_data.append(result)
                        debug_print(result)
                except Exception as e:
                    print(f"Fetch error: {e}")

        chunk_time = time.time() - current_time
        chunk_times.append(chunk_time)
        total_time += chunk_time
        avg_chunk_time = sum(chunk_times) / len(chunk_times)
        remaining_chunks = len(chunks) - chunk_idx
        est_time_remaining = avg_chunk_time * remaining_chunks

        print(f"  ✓ Fetched {len(fetched_data)} reports.")

        # Stage 2: Parse this chunk
        print(f"  → Parsing with {NUM_PARSERS} workers...")
        chunk_results = 0
        chunk_empty = 0

        with ProcessPoolExecutor(max_workers=NUM_PARSERS) as parse_executor:
            parse_futures = [
                parse_executor.submit(parse_content_only, data) for data in fetched_data
            ]

            for future in tqdm(
                as_completed(parse_futures),
                total=len(parse_futures),
                desc=f"  Parsing chunk {chunk_idx}",
                leave=False,
            ):
                try:
                    result = future.result()
                    if result:
                        debug_print("Parse successful")
                        chunk_results += 1
                    else:
                        chunk_empty += 1
                        debug_print("Error with processing")
                        time.sleep(SEC_RATE_LIMIT)
                except Exception as e:
                    print(f"Parse error: {e}")
                    chunk_empty += 1

        total_results += chunk_results
        total_empty += chunk_empty

        print(f"  ✓ Parsed {chunk_results} reports successfully")
        print(f"  Time taken: {format_time(chunk_time)}")
        print(f"  Avg chunk time: {format_time(avg_chunk_time)}")
        print(f"  Est. time remaining: {format_time(est_time_remaining)}")
        print(f"  Total time: {format_time(total_time)}")

        # Clear memory
        del fetched_data
        import gc

        gc.collect()
        if IS_COLAB:
            subprocess.Popen(SAVE_SHELL_CMD, shell=True)
            print(f"  → Saving to database.")

        # Progress summary
        processed_so_far = chunk_idx * CHUNK_SIZE
        percent_complete = (processed_so_far / total_reports) * 100
        print(
            f"  📊 Overall: {total_results:,}/{min(processed_so_far, total_reports):,} ({percent_complete:.1f}% complete)"
        )

    print("\n" + "=" * 70)
    print(f"🎉 FINAL RESULTS:")
    print(f"  ✓ Successfully processed: {total_results:,} reports")
    print(f"  ✗ Empty/failed: {total_empty:,} reports")
    if total_results + total_empty > 0:
        print(
            f"  📈 Success rate: {(total_results/(total_results+total_empty)*100):.1f}%"
        )
    print("=" * 70)


# =============================================================================
# INITIALIZATION
# =============================================================================

create_db()
existing_report_df = fetch_report_data()
print(f"Found {len(existing_report_df)} reports in database")

# =============================================================================
# MAIN EXECUTION
# =============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("STEP 1: Fetch all 10-K report URLs from SEC")
    print("=" * 70)
    # Uncomment to run:
    # fetch_all_grouped()

    print("\n" + "=" * 70)
    print(f"STEP 2: Perform keyword extraction in parallel")
    print("=" * 70)
    # Uncomment to run:
    process_all_reports_fully()

    print("\n" + "=" * 70)
    print("Setup complete! Uncomment the function calls above to execute.")
    print("=" * 70)
