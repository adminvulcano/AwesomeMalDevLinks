"""
Find and validate GitHub repository links in Markdown files.

This script recursively searches a directory for GitHub repository URLs in Markdown files,
checks each unique URL for validity (by verifying if it's a valid Git repository),
and stores the validation results in a CSV database for caching and future reference.
"""
import argparse
import csv
import os
import re
import sys
import time
import requests

# Regex to match GitHub repo URLs (captures the base repo: github.com/owner/repo)
GITHUB_REPO_REGEX = re.compile(
    r"https?://(?:www\.)?github\.com/([a-zA-Z0-9-_.]+)/([a-zA-Z0-9-_.]+)"
)
DEFAULT_DB_PATH = "scripts/githublinks.csv"
VALID_STATUSES = {"valid", "invalid", "unchecked"}


def load_repo_db(csv_path=DEFAULT_DB_PATH):
    """Loads repository status information from a CSV database."""
    repo_status = {}
    if not os.path.exists(csv_path):
        print(f"⚠️ CSV database not found at {os.path.abspath(csv_path)}")
        print(f"   Creating new database...")
        return repo_status

    try:
        with open(csv_path, "r", encoding="utf-8", newline="") as csv_file:
            reader = csv.reader(csv_file, delimiter=";")
            for row in reader:
                if len(row) < 2:
                    continue
                url = row[0].strip()
                status = row[1].strip().lower()
                if status not in VALID_STATUSES:
                    status = "unchecked"
                
                mirrored = row[2].strip().lower() if len(row) > 2 else ""
                
                if url:
                    repo_status[url] = {"status": status, "mirrored": mirrored}
    except Exception as e:
        print(f"⚠️ Error reading CSV database {csv_path}: {e}", file=sys.stderr)

    return repo_status


def save_repo_db(repo_status, csv_path=DEFAULT_DB_PATH):
    """Saves repository status information to a CSV database."""
    try:
        with open(csv_path, "w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerow(["url", "status", "mirrored"])
            for url in sorted(repo_status):
                data = repo_status[url]
                status = data["status"]
                if status not in VALID_STATUSES:
                    status = "unchecked"
                mirrored = data.get("mirrored", "")
                writer.writerow([url, status, mirrored])
    except Exception as e:
        print(f"⚠️ Error writing CSV database {csv_path}: {e}", file=sys.stderr)



def extract_github_repos(directory, max=0):
    """Recursively travels a directory and its subdirectories to extract unique GitHub repo URLs from markdown files."""
    found_repos = {}  # Format: {repo_url: [list_of_files_where_found]}

    print(f"🔍 Recursively scanning: {os.path.abspath(directory)}...")

    # os.walk inherently travels recursively into all subdirectories
    repos_found_count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".md", ".markdown")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        matches = GITHUB_REPO_REGEX.findall(content)

                        for owner, repo in matches:
                            # Clean up repo name from trailing markdown artifacts or extensions
                            repo = repo.split(".git")[0].rstrip(").,:`\"'")
                            repo_url = f"https://github.com/{owner}/{repo}"

                            if repo_url not in found_repos:
                                found_repos[repo_url] = []
                                #print(f"  🔗 Found: {repo_url}")
                            found_repos[repo_url].append(file_path)
                            repos_found_count += 1
                            if max > 0 and repos_found_count >= max:
                                break
                except Exception as e:
                    print(
                        f"⚠️ Error reading file {file_path}: {e}",
                        file=sys.stderr,
                    )

    return found_repos


def check_repo_status(repo_urls, csv_path=DEFAULT_DB_PATH, delay=0.5):
    """Validates the URLs using a CSV-backed status cache and a built-in rate-limiting delay."""
    repo_db = load_repo_db(csv_path)
    results = {"valid": [], "invalid": []}

    # Count how many repos need to be checked
    urls_to_check = 0
    for url in repo_urls:
        existing_data = repo_db.get(url, {"status": "unchecked", "mirrored": ""})
        if existing_data["status"] == "unchecked":
            urls_to_check += 1

    cached_count = len(repo_urls) - urls_to_check
    print(f"\n📡 Found {len(repo_urls)} unique repositories:")
    print(f"   ✓ {cached_count} already checked (cached)")
    print(f"   🔄 {urls_to_check} need to be validated")
    if urls_to_check > 0:
        print(f"   ⏱️  Estimated time: ~{urls_to_check * delay / 60:.1f} minutes (with {delay}s delay between requests)\n")

    with requests.Session() as session:
        session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

        for url in sorted(repo_urls):
            existing_data = repo_db.get(url, {"status": "unchecked", "mirrored": ""})
            existing_status = existing_data["status"]
            
            if existing_status == "valid":
                #print(f"  Skipping already checked URL: {url} [valid]")
                results["valid"].append((url, "Cached"))
                continue
            elif existing_status == "invalid":
                #print(f"  Skipping already checked URL: {url} [invalid]")
                results["invalid"].append((url, "Cached", "Previously marked invalid"))
                continue

            if url.startswith("https://github.com/topics/") or url.startswith("https://github.com/users/") or url.startswith("https://github.com/orgs/"):
                print(f"  Skipping non-repo URL: {url}")
                repo_db[url] = {"status": "invalid", "mirrored": existing_data.get("mirrored", "")}
                results["invalid"].append((url, "Non-repo URL", "Not a repository"))
                continue

            print(f"  Checking: {url}", end=" ", flush=True)
            try:
                git_refs_url = f"{url}/info/refs?service=git-upload-pack"
                response = session.get(git_refs_url, allow_redirects=True, timeout=5)

                content_type = response.headers.get("Content-Type", "")
                if response.status_code == 200 and "git-upload-pack" in content_type:
                    repo_db[url] = {"status": "valid", "mirrored": existing_data.get("mirrored", "")}
                    results["valid"].append((url, response.status_code))
                    print(f"✅ Git repo confirmed")
                else:
                    repo_db[url] = {"status": "invalid", "mirrored": existing_data.get("mirrored", "")}
                    reason = f"Not a git repo ({response.status_code})"
                    results["invalid"].append((url, response.status_code, reason))
                    print(f"❌ {reason}")
            except requests.RequestException as e:
                repo_db[url] = {"status": "invalid", "mirrored": existing_data.get("mirrored", "")}
                results["invalid"].append((url, "Connection Error", str(e)))
                print(f"❌ Connection Error")

            time.sleep(delay)

    save_repo_db(repo_db, csv_path)
    return results


def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Find and validate GitHub repositories inside Markdown files recursively."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="The target directory to scan (defaults to current directory '.')",
    )
    parser.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help="Path to the CSV database file storing repo status (default: githublinks.csv)",
    )
    args = parser.parse_args()

    # Validate directory existence
    if not os.path.isdir(args.directory):
        print(
            f"❌ Error: '{args.directory}' is not a valid directory.",
            file=sys.stderr,
        )
        sys.exit(1)

    # 1. Extract Repos recursively
    repo_map = extract_github_repos(args.directory)

    if not repo_map:
        print("No GitHub repositories found in any Markdown files.")
        return

    print(f"Found {len(repo_map)} unique repository URLs.")
    print(f"Using CSV database: {os.path.abspath(args.db)}")

    # 2. Validate Repos with rate limiting and cached results
    results = check_repo_status(repo_map.keys(), csv_path=args.db, delay=1.0)

    # 3. Print Results Summary
    print("\n" + "=" * 50)
    print(" RESULTS SUMMARY ")
    print("=" * 50)

    print(f"\n✅ VALID REPOSITORIES ({len(results['valid'])}):")
    for url, code in results["valid"]:
        print(f"  [Status {code}] {url}")

    print(f"\n❌ BROKEN REPOSITORIES ({len(results['invalid'])}):")
    for entry in results["invalid"]:
        if len(entry) == 3:
            url, code, reason = entry
        else:
            url, code = entry
            reason = "Previously marked invalid"
        print(f"  [Status {code}] {url} -> ({reason})")
        print("     Found in:")
        for file in repo_map[url]:
            print(f"       - {file}")


if __name__ == "__main__":
    main()