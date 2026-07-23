#!/usr/bin/env python3
"""Generate an Atom feed for the URLs in links.md."""

import argparse
import re
import subprocess
from datetime import datetime
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
    metadata = {}
    commit_time = None
    author = None
    for line in result.stdout.splitlines():
        if line.startswith("author "):
            author = line.removeprefix("author ")
        if line.startswith("committer-time "):
            commit_time = datetime.fromtimestamp(int(line.split()[1])).astimezone()
        elif line.startswith("\t") and commit_time:
            for url in URL_RE.findall(line[1:]):
                url = url.rstrip(".,;:!?)]}")
                metadata.setdefault(url, {"published": commit_time, "author": author or ""})
            commit_time = None
            author = None
    return metadata


def url_to_filename(url):
    """Return the Markdown filename used by the scraper for a URL."""
    filename = re.sub(r"^https?://", "", url.lower())
    filename = re.sub(r"^www\.", "", filename)
    filename = re.sub(r"[^\w\-.]", "_", filename)
    filename = re.sub(r"_+", "_", filename).strip("_")
    return filename[:144]


def llm_description(url, scraped_dir):
    """Return the complete LLM summary for a URL, if available."""
    matches = list(scraped_dir.rglob(f"{url_to_filename(url)}.llm"))
    if not matches:
        return ""
    summary = matches[0].read_text(encoding="utf-8", errors="ignore")
    return "<p>" + "<br>".join(line.rstrip() for line in summary.splitlines()).strip() + "</p>"


def title_for(url):
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")
    title = path.rsplit("/", 1)[-1] if path else parsed.netloc
    title = title.replace("-", " ").replace("_", " ")
    return title or url


def add_text(entry, namespace, name, *, text=None, attributes=None):
    """Add a namespaced Atom element containing text."""
    if attributes is None:
        attributes = {}
    element = ElementTree.SubElement(entry, f"{{{namespace}}}{name}", attributes)
    if text is not None:
        element.text = text


def render_item(feed, item, namespace):
    """Add one Atom entry to the feed."""
    entry = ElementTree.SubElement(feed, f"{{{namespace}}}entry")
    add_text(entry, namespace, "title", text = item["title"])
    add_text(entry, namespace, "link", attributes = {"href": item["url"]})
    add_text(entry, namespace, "id", text = item["url"])
    author = ElementTree.SubElement(entry, f"{{{namespace}}}author")
    add_text(author, namespace, "name", text = item["author"])
    published = item["published"].isoformat()
    add_text(entry, namespace, "published", text = published)
    add_text(entry, namespace, "updated", text = published)
    add_text(entry, namespace, "summary", text = item["description"], attributes = { "type": "html"})


def render_feed(items, title, link, description):
    latest = max((item["published"] for item in items), default=datetime.now().astimezone())
    namespace = "http://www.w3.org/2005/Atom"
    ElementTree.register_namespace("", namespace)
    feed = ElementTree.Element(f"{{{namespace}}}feed")
    add_text(feed, namespace, "title", text = title)
    add_text(feed, namespace, "link", attributes = {"href": link})
    add_text(feed, namespace, "id", text = link)
    add_text(feed, namespace, "updated", text = latest.isoformat())
    add_text(feed, namespace, "subtitle", text = description)

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
    metadata = git_url_timestamps(source)
    items = [
        {
            "url": url,
            "title": title_for(url),
            "published": metadata[url]["published"],
            "author": metadata[url]["author"],
            "description": llm_description(url, scraped_dir) or "Added to the link collection.",
        }
        for url in extract_urls(source)
    ]
    Path(args.output).write_text(
        render_feed(items, args.title, args.link, args.description), encoding="utf-8"
    )
    print(f"Generated {args.output} with {len(items)} links")


if __name__ == "__main__":
    main()
