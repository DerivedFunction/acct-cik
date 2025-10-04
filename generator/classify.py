# =============================================================================
# Model Classification Script
# =============================================================================

import pandas as pd
import requests
import json
import sqlite3
from typing import List
import random
import re
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from collections import Counter
from openpyxl import load_workbook
import subprocess
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

DB_PATH = "webpage.db"
REPORT_URLS_PATH = "./report_data.csv"
SERVER_EXCEL_PATH = "./server_results.xlsx"
SENTENCE_PATH = "./sentence_labels.xlsx"
NUM_THREADS = 6
SERVER_URL = "http://127.0.0.1:5000/predict"
KEYWORDS_FILE = "./keywords_labels.json"

# =============================================================================
# COLAB CONFIGURATION
# =============================================================================
DRIVE_PATH = "./drive/MyDrive/db"
LOAD_SHELL_CMD = f"cp {DRIVE_PATH}/{DB_PATH} ."
SAVE_SHELL_CMD = f"cp {DB_PATH} {DRIVE_PATH}/."
IS_COLAB = Path(DRIVE_PATH).exists()

if IS_COLAB:
    print("Running in Google Colab environment")
    if not Path(DB_PATH).exists():
        print("Loading database from Google Drive...")
        subprocess.run(LOAD_SHELL_CMD, shell=True)
else:
    print("Running in local environment")

# =============================================================================
# LOAD DATA
# =============================================================================

existing_report_df = pd.read_csv(REPORT_URLS_PATH)

# Mapping IDs to labels
with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
    keyword_data = json.load(f)

id2label = {int(id): label for id, label in keyword_data["id2label"].items()}
label2id = {label: int(id) for id, label in id2label.items()}

debug = False  # Debug printing


def debug_print(*args):
    if debug:
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
            CREATE TABLE IF NOT EXISTS server_result (
                url TEXT PRIMARY KEY,
                server_response TEXT,
                FOREIGN KEY (url) REFERENCES report_data (url)
            )
        """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS fail_results (
                cik INTEGER,
                year INTEGER,
                url TEXT PRIMARY KEY
            )
        """
        )
        c.execute(
            """
            CREATE INDEX IF NOT EXISTS url_idx ON server_result (url)
            """
        )
    except sqlite3.IntegrityError:
        debug_print("Something went wrong creating the database")
    finally:
        conn.commit()
        conn.close()


def get_matches(url):
    """
    Fetch matches from webpage_result, which has (url, matches).
    Return: a list
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM webpage_result WHERE url=?", (url,))
    columns = [col[0] for col in c.description]
    result = c.fetchone()
    conn.close()
    if not result:
        return []
    data = pd.DataFrame([result], columns=columns)
    matches = json.loads(data.matches.iloc[0])
    return matches


def fetch_server_results():
    """
    Fetch results from server_result
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM server_result")
    columns = [col[0] for col in c.description]
    rows = c.fetchall()
    pre_data = pd.DataFrame(rows, columns=columns)
    conn.close()
    return pre_data


def get_processed_server_urls() -> set:
    """
    Return a set of URLs that are already processed in `server_result`.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT url FROM server_result")
    rows = c.fetchall()
    conn.close()
    return set(url for (url,) in rows)


def save_process_result(df):
    """
    Inserts a new item into the server_result table
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT OR REPLACE INTO server_result (url, server_response) VALUES (?, ?)",
            (df.url, json.dumps(df.server_response)),
        )
    except sqlite3.Error as e:
        debug_print(f"DB error on {df.url}: {e}")
        # Get cik and year from report_data for fail_results
        c.execute("SELECT cik, year FROM report_data WHERE url=?", (df.url,))
        result = c.fetchone()
        if result:
            cik, year = result
            c.execute(
                "INSERT OR IGNORE INTO fail_results (cik, year, url) VALUES (?, ?, ?)",
                (cik, year, df.url),
            )

    conn.commit()
    conn.close()


# =============================================================================
# SERVER COMMUNICATION
# =============================================================================

def get_result_from_server(sentences, batch_size=128):
    predictions = []
    headers = {"Content-Type": "application/json"}

    for i in range(0, len(sentences), batch_size):
        batch = sentences[i : i + batch_size]
        payload = {"texts": batch}
        try:
            response = requests.post(
                SERVER_URL, headers=headers, data=json.dumps(payload)
            )
            response.raise_for_status()
            resp_json = response.json()
            preds = resp_json.get("predictions")
            if not isinstance(preds, list):
                preds = []
            if len(preds) != len(batch):
                debug_print(
                    f"Warning: batch size {len(batch)} vs response {len(preds)} mismatch"
                )
                return [-1] * len(batch)
            predictions.extend(preds)
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with server: {e}")
            predictions.extend([-1] * len(batch))
    return predictions


def process_report_fully(report):
    """
    Processes a single report completely:
    1. Loads content (from cache or web).
    2. Gets analysis from the server for those sentences from `matches`.
    3. Saves the result to the server_result table.
    """
    if report.url in processed_set:
        debug_print(f"Skipping already processed: {report.url}")
        return None

    # Get the report's `matches`
    matches = get_matches(report.url)
    server_predictions = []
    
    # Prepend <reportYear> to each sentence
    if matches:
        matches_with_year = [
            f"<reportYear>{report.year}</reportYear> {s}" for s in matches
        ]
        # Get sentence analysis from the server
        server_predictions = get_result_from_server(matches_with_year)
    else:
        server_predictions = []

    # Prepare the final result row for the database
    result_row = pd.Series(
        {
            "url": report.url,
            "server_response": server_predictions,
        }
    )

    # Save the complete result
    save_process_result(result_row)
    return result_row


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def parse_json(json_str):
    """Helper function to parse JSON strings safely"""
    try:
        return json.loads(json_str) if isinstance(json_str, str) else json_str
    except (json.JSONDecodeError, TypeError):
        return []


def get_final_results():
    """Get all processed results from the database, joined with report_data for cik/year"""
    conn = sqlite3.connect(DB_PATH)
    
    # Join server_result with report_data to get cik and year
    query = """
        SELECT 
            r.cik,
            r.year,
            s.url,
            s.server_response
        FROM server_result s
        JOIN report_data r ON s.url = r.url
    """
    
    wr = pd.read_sql(query, conn)
    conn.close()
    
    if wr.empty:
        print("No results found in server_result table")
        return pd.DataFrame()

    # Parse JSON columns
    wr["server_response"] = wr["server_response"].apply(parse_json)

    return wr


def get_sentence_analysis():
    """Get sentence analysis with server predictions and save to Excel."""
    wr = get_final_results()
    if wr.empty:
        print("No processed results found for sentence analysis")
        return pd.DataFrame()

    # Expand server responses
    analysis_data = []
    for _, row in wr.iterrows():
        predictions = row["server_response"]
        if not isinstance(predictions, list):
            continue

        # Map IDs → labels
        predicted_labels = [id2label.get(pid, "Unknown") for pid in predictions]
        pred_counts = Counter(predicted_labels)

        analysis_data.append(
            {
                "cik": row["cik"],
                "year": row["year"],
                "url": row["url"],
                "total_sentences": len(predictions),
                **pred_counts,
            }
        )

    sa = pd.DataFrame(analysis_data)
    # Fill missing numeric cols with 0
    sa = sa.fillna({col: 0 for col in sa.select_dtypes("number").columns})

    print(f"Sentence analysis for {len(sa)} reports:")

    # Excel writer
    with pd.ExcelWriter(SERVER_EXCEL_PATH, engine="openpyxl") as writer:

        # --- Main sheet ---
        sa.to_excel(writer, sheet_name="all_reports", index=False)

        # --- Define label groups ---
        hedge_labels_current = [
            id2label[0],  # General/Unknown Hedge Der.
            id2label[8],  # IR Hedge
            id2label[10], # FX Hedge
            id2label[12], # CP Hedge
        ]

        hedge_labels_historic = [
            id2label[1],  # General/Unknown Hedge Der. Historic
            id2label[9],  # IR Hedge Historic
            id2label[11], # FX Hedge Historic
            id2label[13], # CP Hedge Historic
        ]

        # --- Firms with any current hedge ---
        firms_current_hedge = sa.groupby("cik").filter(
            lambda g: g[hedge_labels_current].sum().sum() > 0
        )
        firms_current_hedge.to_excel(writer, sheet_name="Current Hedging", index=False)

        # --- Firms with only historical hedges and no current hedge ---
        firms_historic_only = sa.groupby("cik").filter(
            lambda g: g[hedge_labels_historic].sum().sum() > 0
            and g[hedge_labels_current].sum().sum() == 0
        )
        firms_historic_only.to_excel(writer, sheet_name="Hedging Past Year", index=False)

        # --- Firms with only speculative mentions (label 2) ---
        exclude_cols = [id2label[i] for i in id2label if i != 2]
        firms_label2_only = sa.groupby("cik").filter(
            lambda g: g[id2label[2]].sum() > 0
            and g[exclude_cols].sum().sum() < g[id2label[2]].sum()
        )
        firms_label2_only.to_excel(writer, sheet_name="Speculation Only", index=False)

        # --- Firms with liabilities/warrants (labels 4 or 5) ---
        firms_liabilities = sa.loc[
            (sa[id2label[4]] > 0) | (sa[id2label[5]] > 0)
        ]
        firms_liabilities.to_excel(writer, sheet_name="Derivative Liabilities/Warrants", index=False)

        # --- Firms with Embedded Derivatives (labels 6 or 7) ---
        embedded_derivatives = sa.loc[
            (sa[id2label[6]] > 0) | (sa[id2label[7]] > 0)
        ]
        embedded_derivatives.to_excel(writer, sheet_name="Embedded Derivatives", index=False)

        # --- Unique firms per label/year ---
        label_cols = [id2label[i] for i in id2label]
        unique_counts = (
            sa.melt(id_vars=["cik", "year"], value_vars=label_cols)
            .query("value > 0")
            .drop_duplicates(["cik", "year", "variable"])
            .groupby(["year", "variable"])["cik"]
            .nunique()
            .reset_index(name="unique_firms")
        )
        unique_counts.to_excel(writer, sheet_name="unique_per_year", index=False)

        # --- Label co-occurrence ---
        cooc = sa[label_cols].gt(0).astype(int).T.dot(sa[label_cols].gt(0).astype(int))
        cooc.to_excel(writer, sheet_name="label_cooccurrence")

        # --- Hedging by Type ---
        hedge_types = {
            "General": [id2label[0], id2label[1]],
            "IR": [id2label[8], id2label[9]],
            "FX": [id2label[10], id2label[11]],
            "CP": [id2label[12], id2label[13]],
        }

        hedge_type_records = []
        for hedge_name, labels in hedge_types.items():
            temp = (
                sa.groupby(["cik", "year"])
                .filter(lambda g: g[labels].sum().sum() > 0)
                .assign(hedge_type=hedge_name)
            )
            hedge_type_records.append(temp)

        if hedge_type_records:
            hedge_by_type = pd.concat(hedge_type_records, ignore_index=True)
            hedge_by_type.to_excel(writer, sheet_name="Hedging by Type", index=False)
        else:
            pd.DataFrame(columns=["cik", "year", "hedge_type"]).to_excel(
                writer, sheet_name="Hedging by Type", index=False
            )

        # --- Hedge Type Cross-Analysis ---
        hedge_flags = sa.groupby("cik")[[
            id2label[0], id2label[8], id2label[10], id2label[12],
            id2label[1], id2label[9], id2label[11], id2label[13],
        ]].sum().gt(0).astype(int)

        # Map to current hedge categories only (merge historic)
        hedge_flags_simple = pd.DataFrame({
            "General": hedge_flags[[id2label[0], id2label[1]]].max(axis=1),
            "IR": hedge_flags[[id2label[8], id2label[9]]].max(axis=1),
            "FX": hedge_flags[[id2label[10], id2label[11]]].max(axis=1),
            "CP": hedge_flags[[id2label[12], id2label[13]]].max(axis=1),
        })

        hedge_cross = hedge_flags_simple.T.dot(hedge_flags_simple)
        hedge_cross.to_excel(writer, sheet_name="Hedge Type Cross", index=True)

    print(f"Sentence analysis saved to: {SERVER_EXCEL_PATH}")
    
    # Save to Google Drive if in Colab
    if IS_COLAB:
        print("Saving results to Google Drive...")
        subprocess.run(f"cp {SERVER_EXCEL_PATH} {DRIVE_PATH}/.", shell=True)

    return sa


def build_sentence_label_excel():
    # Load both DB tables with a join to get cik and year
    conn = sqlite3.connect(DB_PATH)
    
    query = """
        SELECT 
            r.cik,
            r.year,
            w.url,
            w.matches,
            s.server_response
        FROM webpage_result w
        JOIN report_data r ON w.url = r.url
        JOIN server_result s ON w.url = s.url
    """
    
    combined_df = pd.read_sql(query, conn)
    conn.close()

    all_rows = []

    for _, row in combined_df.iterrows():
        # Parse arrays
        matches = json.loads(row["matches"])
        predictions = json.loads(row["server_response"])

        # Defensive check: align lengths
        min_len = min(len(matches), len(predictions))

        for i in range(min_len):
            sentence = matches[i]
            pred = predictions[i]
            label = id2label.get(pred, "Unknown")

            all_rows.append(
                {
                    "cik": row["cik"],
                    "year": row["year"],
                    "url": row["url"],
                    "sentence": sentence,
                    "label_id": pred,
                    "label": label,
                }
            )

    # Build final DataFrame
    final_df = pd.DataFrame(all_rows)

    # Save to Excel
    final_df.to_excel(SENTENCE_PATH, index=False)
    print(f"Saved sentence-label mapping to {SENTENCE_PATH}")
    
    # Save to Google Drive if in Colab
    if IS_COLAB:
        print("Saving sentence labels to Google Drive...")
        subprocess.run(f"cp {SENTENCE_PATH} {DRIVE_PATH}/.", shell=True)

    return final_df


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Model Classification and Analysis Script")
    print("=" * 70)
    
    # Initialize database
    create_db()
    
    # Process reports
    print("\nProcessing reports with server predictions...")
    results = []
    processed_set = get_processed_server_urls()

    # Only process reports not already in server_result
    reports_to_process = [
        r
        for r in existing_report_df.itertuples(index=False)
        if r.url not in processed_set
    ]

    print(f"Found {len(reports_to_process)} reports to process")
    print(f"Already processed: {len(processed_set)} reports")

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        future_to_report = {
            executor.submit(process_report_fully, r): r for r in reports_to_process
        }

        for future in tqdm(as_completed(future_to_report), total=len(future_to_report)):
            try:
                res = future.result()
                if res is not None:
                    results.append(res)
            except Exception as e:
                debug_print(f"Error processing {future_to_report[future].url}: {e}")

    print(f"Processed {len(results)} new reports in parallel.")
    
    # Generate analysis
    print("\n" + "=" * 70)
    print("Generating sentence analysis...")
    print("=" * 70)
    sa = get_sentence_analysis()
    print(f"\nFirst 10 rows of analysis:")
    print(sa.head(10))
    
    # Build sentence-label mapping
    print("\n" + "=" * 70)
    print("Building sentence-label Excel file...")
    print("=" * 70)
    sentence_label_df = build_sentence_label_excel()
    print(f"\nFirst 10 rows of sentence labels:")
    print(sentence_label_df.head(10))
    
    # Final save to Drive if in Colab
    if IS_COLAB:
        print("\nFinal database sync to Google Drive...")
        subprocess.run(SAVE_SHELL_CMD, shell=True)
    
    print("\n" + "=" * 70)
    print("All done!")
    print("=" * 70)