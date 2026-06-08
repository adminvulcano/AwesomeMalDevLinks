"""
Mirror valid GitHub repository links from a CSV database to a mirroring service.

This script reads a CSV file containing GitHub repository URLs and their validation status,
filters for those marked as 'valid' and not yet mirrored, and sends them to a mirroring
service via HTTP POST. It then updates the CSV with a 'mirrored' status column.
"""
import argparse
import csv
import os
import sys
import time
import requests

DEFAULT_DB_PATH = "githublinks.csv"
MIRROR_URL = "https://gitadd.r00ted.ch"


def main():
    parser = argparse.ArgumentParser(
        description="Mirror valid GitHub repositories from a CSV database."
    )
    parser.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"Path to the CSV database file (default: {DEFAULT_DB_PATH})",
    )
    parser.add_argument(
        "--password",
        required=True,
        help="Access password for the mirroring service",
    )
    parser.add_argument(
        "--delay",
        type=int,
        default=20,
        help="Delay in seconds between requests (default: 20)",
    )
    args = parser.parse_args()

    if not os.path.exists(args.db):
        print(f"❌ Error: Database file '{args.db}' not found.", file=sys.stderr)
        sys.exit(1)

    rows = []
    
    try:
        with open(args.db, "r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            for i, row in enumerate(reader):
                # Skip header if it exists
                if i == 0 and len(row) >= 1 and row[0].strip().lower() == "url":
                    continue
                
                if len(row) >= 2:
                    url = row[0].strip()
                    status = row[1].strip().lower()
                    mirrored = row[2].strip().lower() if len(row) > 2 else ""
                    rows.append({"url": url, "status": status, "mirrored": mirrored})
                elif len(row) == 1:
                    url = row[0].strip()
                    if url:
                        rows.append({"url": url, "status": "unchecked", "mirrored": ""})
    except Exception as e:
        print(f"❌ Error reading CSV: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"📡 Found {len(rows)} entries in {args.db}")

    # Filter valid and not yet mirrored
    to_mirror = [
        row for row in rows 
        if row.get("status", "").strip().lower() == "valid" 
        and row.get("mirrored", "").strip().lower() != "yes"
    ]
    
    if not to_mirror:
        print("✅ No new valid repositories to mirror.")
        return

    print(f"🔄 Attempting to mirror {len(to_mirror)} repositories...")

    with requests.Session() as session:
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

        for row in to_mirror:
            url = row["url"].strip()
            print(f"Mirroring: {url}", end=" ", flush=True)
            
            form_data = {
                "github_url": url,
                "access_password": args.password
            }
            
            try:
                response = session.post(MIRROR_URL, data=form_data, timeout=30)
                if response.status_code == 200:
                    row["mirrored"] = "yes"
                    print("✅ Success")
                else:
                    row["mirrored"] = f"failed ({response.status_code})"
                    print(f"❌ Failed: HTTP {response.status_code}")
            except requests.RequestException as e:
                row["mirrored"] = f"failed ({e})"
                print(f"❌ Failed: {e}")
            
            # Write back to CSV after each attempt to ensure progress is saved
            try:
                with open(args.db, "w", encoding="utf-8", newline="") as f:
                    writer = csv.writer(f, delimiter=";")
                    writer.writerow(["url", "status", "mirrored"])
                    for r in rows:
                        writer.writerow([r["url"], r["status"], r["mirrored"]])
                #print(f"💾 Updated database saved to {args.db}")
            except Exception as e:
                print(f"❌ Error writing CSV: {e}", file=sys.stderr)
            
            time.sleep(args.delay)


if __name__ == "__main__":
    main()