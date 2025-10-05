# =============================================================================
# Model Classification Script - Chunked Processing
# =============================================================================

import pandas as pd
import requests
import json
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from collections import Counter
import subprocess
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

DB_PATH = "web_data.db"
REPORT_CSV_PATH = "./report_data.csv"
SERVER_EXCEL_PATH = "./server_results.xlsx"
SENTENCE_PATH = "./sentence_labels.xlsx"
SERVER_URL = "http://127.0.0.1:5000/predict"
KEYWORDS_FILE = "./keywords_find.json"
DEBUG = False  # Debug printing

# =============================================================================
# COLAB CONFIGURATION
# =============================================================================
DRIVE_PATH = "./drive/MyDrive/db"
LOAD_SHELL_CMD = f"cp {DRIVE_PATH}/{DB_PATH} ."
SAVE_SHELL_CMD = f"cp {DB_PATH} {DRIVE_PATH}/."
IS_COLAB = Path(DRIVE_PATH).exists()

# Chunking configuration
CHUNK_SIZE = 1000 * (1 if not IS_COLAB else 5)
NUM_THREADS = 2 * (1 if not IS_COLAB else 5)

if IS_COLAB:
    print("Running in Google Colab environment")
    if not Path(DB_PATH).exists():
        print("Loading database from Google Drive...")
        subprocess.run(LOAD_SHELL_CMD, shell=True)
else:
    print("Running in local environment")

# =============================================================================
# DEBUG UTILITIES
# =============================================================================


def debug_print(*args):
    global DEBUG
    if DEBUG:
        print(*args)


def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    elif minutes > 0:
        return f"{int(minutes)}m {int(seconds)}s"
    else:
        return f"{int(seconds)}s"


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


def save_batch_results(results_buffer):
    """
    Batch insert multiple results into the server_result table
    """
    if not results_buffer:
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    success_count = 0
    fail_count = 0

    try:
        # Prepare batch data
        batch_data = []
        fail_data = []

        for result in results_buffer:
            try:
                batch_data.append((result.url, json.dumps(result.server_response)))
            except Exception as e:
                debug_print(f"Error preparing data for {result.url}: {e}")
                # Get cik and year from report_data for fail_results
                c.execute(
                    "SELECT cik, year FROM report_data WHERE url=?", (result.url,)
                )
                db_result = c.fetchone()
                if db_result:
                    cik, year = db_result
                    fail_data.append((cik, year, result.url))
                fail_count += 1

        # Batch insert successful results
        if batch_data:
            c.executemany(
                "INSERT OR REPLACE INTO server_result (url, server_response) VALUES (?, ?)",
                batch_data,
            )
            success_count = len(batch_data)

        # Batch insert failures
        if fail_data:
            c.executemany(
                "INSERT OR IGNORE INTO fail_results (cik, year, url) VALUES (?, ?, ?)",
                fail_data,
            )

        conn.commit()
        debug_print(f"Batch saved: {success_count} success, {fail_count} failures")

    except sqlite3.Error as e:
        print(f"Batch DB error: {e}")
        conn.rollback()
    finally:
        conn.close()

    return success_count, fail_count


def fetch_report_data(valid=True):
    global REPORT_CSV_PATH
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
    3. Returns the result (does NOT save to database immediately).
    """
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

    # Prepare the final result row (return, don't save yet)
    result_row = pd.Series(
        {
            "url": report.url,
            "server_response": server_predictions,
        }
    )

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
            id2label[10],  # FX Hedge
            id2label[12],  # CP Hedge
        ]

        hedge_labels_historic = [
            id2label[1],  # General/Unknown Hedge Der. Historic
            id2label[9],  # IR Hedge Historic
            id2label[11],  # FX Hedge Historic
            id2label[13],  # CP Hedge Historic
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
        firms_historic_only.to_excel(
            writer, sheet_name="Hedging Past Year", index=False
        )

        # --- Firms with only speculative mentions (label 2) ---
        exclude_cols = [id2label[i] for i in id2label if i != 2]
        firms_label2_only = sa.groupby("cik").filter(
            lambda g: g[id2label[2]].sum() > 0
            and g[exclude_cols].sum().sum() < g[id2label[2]].sum()
        )
        firms_label2_only.to_excel(writer, sheet_name="Speculation Only", index=False)

        # --- Firms with liabilities/warrants (labels 4 or 5) ---
        firms_liabilities = sa.loc[(sa[id2label[4]] > 0) | (sa[id2label[5]] > 0)]
        firms_liabilities.to_excel(
            writer, sheet_name="Derivative Liabilities/Warrants", index=False
        )

        # --- Firms with Embedded Derivatives (labels 6 or 7) ---
        embedded_derivatives = sa.loc[(sa[id2label[6]] > 0) | (sa[id2label[7]] > 0)]
        embedded_derivatives.to_excel(
            writer, sheet_name="Embedded Derivatives", index=False
        )

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
        hedge_flags = (
            sa.groupby("cik")[
                [
                    id2label[0],
                    id2label[8],
                    id2label[10],
                    id2label[12],
                    id2label[1],
                    id2label[9],
                    id2label[11],
                    id2label[13],
                ]
            ]
            .sum()
            .gt(0)
            .astype(int)
        )

        # Map to current hedge categories only (merge historic)
        hedge_flags_simple = pd.DataFrame(
            {
                "General": hedge_flags[[id2label[0], id2label[1]]].max(axis=1),
                "IR": hedge_flags[[id2label[8], id2label[9]]].max(axis=1),
                "FX": hedge_flags[[id2label[10], id2label[11]]].max(axis=1),
                "CP": hedge_flags[[id2label[12], id2label[13]]].max(axis=1),
            }
        )

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
# CHUNKED PROCESSING
# =============================================================================


def process_reports_in_chunks():
    """Process reports in chunks with periodic saves and statistics."""
    global existing_report_df

    processed_set = get_processed_server_urls()

    # Only process reports not already in server_result
    reports_to_process = [
        r
        for r in existing_report_df.itertuples(index=False)
        if r.url not in processed_set
    ]

    total_reports = len(reports_to_process)
    print(f"Processing {total_reports:,} new reports")
    print(f"Already processed: {len(processed_set):,} reports")

    # Create chunks
    chunks = [
        reports_to_process[i : i + CHUNK_SIZE]
        for i in range(0, total_reports, CHUNK_SIZE)
    ]

    print(f"\nProcessing in {len(chunks)} chunks of {CHUNK_SIZE} reports each")
    print("=" * 70)

    chunk_times = []
    total_time = 0
    total_results = 0
    total_empty = 0

    for chunk_idx, chunk in enumerate(chunks, 1):
        start_chunk_time = time.time()
        print(f"\n📦 Chunk {chunk_idx}/{len(chunks)} ({len(chunk)} reports)")

        chunk_results = 0
        chunk_empty = 0
        results_buffer = []

        # Process chunk with ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            future_to_report = {
                executor.submit(process_report_fully, r): r for r in chunk
            }

            for future in tqdm(
                as_completed(future_to_report),
                total=len(future_to_report),
                desc=f"  Processing chunk {chunk_idx}",
                leave=False,
            ):
                try:
                    res = future.result()
                    if res is not None:
                        chunk_results += 1
                        results_buffer.append(res)
                    else:
                        chunk_empty += 1
                except Exception as e:
                    debug_print(f"Error processing {future_to_report[future].url}: {e}")
                    chunk_empty += 1
        # Flush the results buffer
        save_batch_results(results_buffer)
        results_buffer.clear()
        
        chunk_time = time.time() - start_chunk_time
        chunk_times.append(chunk_time)
        total_time += chunk_time
        total_results += chunk_results
        total_empty += chunk_empty

        # Calculate statistics
        avg_chunk_time = sum(chunk_times) / len(chunk_times)
        remaining_chunks = len(chunks) - chunk_idx
        est_time_remaining = avg_chunk_time * remaining_chunks

        print(f"  ✓ Processed {chunk_results} reports successfully")
        print(f"  ✗ Empty/failed: {chunk_empty} reports")
        print(f"  Time taken: {format_time(chunk_time)}")
        print(f"  Avg chunk time: {format_time(avg_chunk_time)}")
        print(f"  Est. time remaining: {format_time(est_time_remaining)}")
        print(f"  Total time: {format_time(total_time)}")

        # Save to Google Drive if in Colab
        if IS_COLAB:
            print(f"  → Saving to Google Drive...")
            subprocess.run(SAVE_SHELL_CMD, shell=True)

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

    return total_results


# =============================================================================
# INITIALIZATION
# =============================================================================

create_db()
existing_report_df = fetch_report_data()
print(f"Found {len(existing_report_df)} reports in database")
with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
    keyword_data = json.load(f)

id2label = {int(id): label for id, label in keyword_data["id2label"].items()}
label2id = {label: int(id) for id, label in id2label.items()}

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Model Classification and Analysis Script")
    print("=" * 70)

    # Initialize database
    create_db()

    # Process reports in chunks
    print("\nProcessing reports with server predictions...")
    total_processed = process_reports_in_chunks()

    print(f"\nProcessed {total_processed} new reports in chunked parallel mode.")

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
