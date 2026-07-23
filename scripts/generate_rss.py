#!/usr/bin/env python3
"""Generate an Atom feed for the URLs in links.md."""

import argparse
import html
import re
import subprocess
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree


URL_RE = re.compile(r"https?://[^\s<>`\"]+")
DEFAULT_SOURCE = "links.md"
DEFAULT_OUTPUT = "data/rss/rss.xml"
DEFAULT_TITLE = "Awesome Mega MalDev Links"
DEFAULT_LINK = "https://github.com/dobin/AwesomeMalDevLinks"
DEFAULT_DESCRIPTION = "Curated offensive security, malware development, and red-team links."
DEFAULT_SCRAPED_DIR = "data/out"
DESCRIPTION_LIMIT = 500


def extract_urls(source):
    """Return unique URLs in source, preserving their order in the file."""
    urls = []
    seen = set()
    for match in URL_RE.finditer(source.read_text(encoding="utf-8")):
        url = match.group(0).rstrip(".,;:!?)]}")
        if url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


def git_url_timestamps(source):
    """Return URL timestamps from a single porcelain blame invocation."""
    result = subprocess.run(
        [
            "git",
            "blame",
            "--line-porcelain",
            "--",
            str(source),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    timestamps = {}
    commit_time = None
    for line in result.stdout.splitlines():
        if line.startswith("committer-time "):
            commit_time = datetime.fromtimestamp(int(line.split()[1])).astimezone()
        elif line.startswith("\t") and commit_time:
            for url in URL_RE.findall(line[1:]):
                url = url.rstrip(".,;:!?)]}")
                timestamps.setdefault(url, commit_time)
            commit_time = None
    return timestamps


def url_to_filename(url):
    """Return the Markdown filename used by the scraper for a URL."""
    filename = re.sub(r"^https?://", "", url.lower())
    filename = re.sub(r"^www\.", "", filename)
    filename = re.sub(r"[^\w\-.]", "_", filename)
    filename = re.sub(r"_+", "_", filename).strip("_")
    return filename[:144]


class GithubAboutParser(HTMLParser):
    """Extract the repository About paragraph from GitHub HTML."""

    def __init__(self):
        super().__init__()
        self.heading = []
        self.in_about = False
        self.in_paragraph = False
        self.paragraph = []
        self.description = ""

    def handle_starttag(self, tag, attrs):
        if tag == "h2":
            self.heading = []
        elif tag == "p" and self.in_about and not self.description:
            self.in_paragraph = True
            self.paragraph = []

    def handle_endtag(self, tag):
        if tag == "h2":
            self.in_about = "".join(self.heading).strip().lower() == "about"
        elif tag == "p" and self.in_paragraph:
            self.description = " ".join("".join(self.paragraph).split())
            self.in_paragraph = False

    def handle_data(self, data):
        if self.heading is not None and not self.in_paragraph:
            self.heading.append(data)
        if self.in_paragraph:
            self.paragraph.append(data)


def clean_description(text):
    text = re.sub(r"\s+", " ", html.unescape(text)).strip()
    if len(text) > DESCRIPTION_LIMIT:
        text = text[:DESCRIPTION_LIMIT].rsplit(" ", 1)[0] + "..."
    return text


def github_html_description(url, scraped_dir):
    """Extract GitHub's repository About paragraph from scraped HTML."""
    matches = list(scraped_dir.rglob(f"{url_to_filename(url)}.html"))
    if not matches:
        return ""
    parser = GithubAboutParser()
    parser.feed(matches[0].read_text(encoding="utf-8", errors="ignore"))
    return clean_description(parser.description) if parser.description else ""


def markdown_description(url, scraped_dir):
    """Extract a paragraph after GitHub's repository-content marker."""
    matches = list(scraped_dir.rglob(f"{url_to_filename(url)}.md"))
    if not matches:
        return ""

    markdown = matches[0].read_text(encoding="utf-8", errors="ignore")
    marker = re.search(r"^## Repository files navigation\s*$", markdown, re.MULTILINE)
    if not marker:
        return ""

    paragraphs = re.split(r"\n\s*\n", markdown[marker.end() :])
    for paragraph in paragraphs:
        text = re.sub(r"^#+\s*", "", paragraph.strip())
        if "[Permalink:" in text:
            continue
        text = re.sub(r"!\[[^]]*\]\([^)]*\)", "", text)
        text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
        text = re.sub(r"[*_`~]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) >= 40 and not text.startswith("http"):
            return clean_description(text)

    return ""


def general_markdown_description(url, scraped_dir):
    """Extract a short description from a non-GitHub Markdown file."""
    matches = list(scraped_dir.rglob(f"{url_to_filename(url)}.md"))
    if not matches:
        return ""

    paragraphs = re.split(r"\n\s*\n", matches[0].read_text(encoding="utf-8", errors="ignore"))
    for paragraph in paragraphs:
        text = re.sub(r"^#+\s*", "", paragraph.strip())
        text = re.sub(r"!\[[^]]*\]\([^)]*\)", "", text)
        text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
        text = re.sub(r"[*_`~]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) >= 40 and not text.startswith("http"):
            return clean_description(text)
    return ""


def scraped_description(url, scraped_dir):
    """Use GitHub About, then marked repository Markdown, then a fallback."""
    if urlparse(url).netloc.lower() in {"github.com", "www.github.com"}:
        description = github_html_description(url, scraped_dir)
        if description:
            return description
        description = markdown_description(url, scraped_dir)
        if description:
            return description
    else:
        description = general_markdown_description(url, scraped_dir)
        if description:
            return description
    return "Added to the link collection."


def title_for(url):
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")
    title = path.rsplit("/", 1)[-1] if path else parsed.netloc
    title = title.replace("-", " ").replace("_", " ")
    return title or url


def add_text(entry, namespace, name, value):
    """Add a namespaced Atom element containing text."""
    ElementTree.SubElement(entry, f"{{{namespace}}}{name}").text = value


def render_item(feed, item, namespace):
    """Add one Atom entry to the feed."""
    entry = ElementTree.SubElement(feed, f"{{{namespace}}}entry")
    add_text(entry, namespace, "title", item["title"])
    ElementTree.SubElement(entry, f"{{{namespace}}}link", {"href": item["url"]})
    add_text(entry, namespace, "id", item["url"])
    published = item["published"].isoformat()
    add_text(entry, namespace, "published", published)
    add_text(entry, namespace, "updated", published)
    add_text(entry, namespace, "summary", item["description"])


def render_feed(items, title, link, description):
    latest = max((item["published"] for item in items), default=datetime.now().astimezone())
    namespace = "http://www.w3.org/2005/Atom"
    ElementTree.register_namespace("", namespace)
    feed = ElementTree.Element(f"{{{namespace}}}feed")
    add_text(feed, namespace, "title", title)
    ElementTree.SubElement(feed, f"{{{namespace}}}link", {"href": link})
    add_text(feed, namespace, "id", link)
    add_text(feed, namespace, "updated", latest.isoformat())
    add_text(feed, namespace, "subtitle", description)

    for item in sorted(items, key=lambda item: item["published"], reverse=True):
        render_item(feed, item, namespace)

    ElementTree.indent(feed)
    return ElementTree.tostring(feed, encoding="unicode", xml_declaration=True) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=DEFAULT_SOURCE, help="Markdown file containing URLs")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Atom output path")
    parser.add_argument(
        "--scraped-dir", default=DEFAULT_SCRAPED_DIR, help="Directory containing scraped Markdown"
    )
    parser.add_argument("--title", default=DEFAULT_TITLE, help="Atom feed title")
    parser.add_argument("--link", default=DEFAULT_LINK, help="Atom feed link")
    parser.add_argument("--description", default=DEFAULT_DESCRIPTION, help="Atom feed description")
    args = parser.parse_args()

    source = Path(args.source)
    scraped_dir = Path(args.scraped_dir)
    timestamps = git_url_timestamps(source)
    items = [
        {
            "url": url,
            "title": title_for(url),
            "published": timestamps[url],
            "description": scraped_description(url, scraped_dir),
        }
        for url in extract_urls(source)
    ]
    Path(args.output).write_text(
        render_feed(items, args.title, args.link, args.description), encoding="utf-8"
    )
    print(f"Generated {args.output} with {len(items)} links")


if __name__ == "__main__":
    main()
