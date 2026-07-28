#!/usr/bin/env python3
"""Resolve saved URLs and fetch page titles for the Notion reading library."""

from __future__ import annotations

import argparse
import html
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "raw" / "notion" / "resource-library-2026-07-24.json"
OUTPUT = (
    ROOT / "raw" / "notion" / "resource-library-url-metadata-2026-07-24.json"
)
URL_PATTERN = re.compile(r"https?://[^\s<>\"]+")
GENERIC_TITLES = {
    "arxiv.org",
    "github.com",
    "medium.com",
    "x.com",
    "youtu.be",
    "youtube.com",
}
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 Chrome/126 Safari/537.36"
)
MAX_TITLE_BYTES = 768 * 1024


def clean_url(value: str) -> str:
    return value.strip().rstrip(".,);]}>")


def extract_source_url(record: dict[str, str]) -> str:
    explicit = clean_url(record.get("userDefined:URL", ""))
    if explicit:
        return explicit
    match = URL_PATTERN.search(record.get("Title", ""))
    return clean_url(match.group(0)) if match else ""


def is_weak_title(value: str, source_url: str) -> bool:
    title = " ".join(value.split()).strip()
    if not title or title.startswith(("http://", "https://")):
        return True
    lowered = title.casefold()
    normalized = lowered.removeprefix("www.")
    if lowered.startswith("source:") or normalized in GENERIC_TITLES:
        return True
    host = urlparse(source_url).netloc.casefold().removeprefix("www.")
    if normalized in {host, host.split(".", 1)[0]}:
        return True
    return len(title) <= 12


class TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.title_parts: list[str] = []
        self.meta_titles: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        if tag.casefold() == "title":
            self.in_title = True
            return
        if tag.casefold() != "meta":
            return
        values = {key.casefold(): value or "" for key, value in attrs}
        label = (values.get("property") or values.get("name", "")).casefold()
        if label in {"og:title", "twitter:title"} and values.get("content"):
            self.meta_titles.append(values["content"])

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)

    def result(self) -> str:
        values = self.meta_titles + [" ".join(self.title_parts)]
        for value in values:
            cleaned = " ".join(html.unescape(value).split()).strip()
            if cleaned:
                return cleaned
        return ""


def youtube_video_id(value: str) -> str:
    parsed = urlparse(value)
    host = parsed.netloc.casefold().removeprefix("www.")
    if host == "youtu.be":
        return parsed.path.strip("/").split("/", 1)[0]
    if host.endswith("youtube.com"):
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [""])[0]
        if parsed.path.startswith(("/shorts/", "/embed/")):
            return parsed.path.split("/")[2]
    return ""


def fetch_youtube_metadata(source_url: str) -> dict[str, object] | None:
    video_id = youtube_video_id(source_url)
    if not video_id:
        return None
    canonical = f"https://www.youtube.com/watch?v={video_id}"
    query = urlencode({"url": canonical, "format": "json"})
    request = Request(
        f"https://www.youtube.com/oembed?{query}",
        headers={"User-Agent": USER_AGENT},
    )
    try:
        with urlopen(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return {
            "final_url": canonical,
            "title": " ".join(str(payload.get("title", "")).split()),
            "status": response.status,
            "content_type": "application/json",
        }
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        return {
            "final_url": canonical,
            "title": "",
            "status": getattr(error, "code", 0),
            "content_type": "",
            "error": type(error).__name__,
        }


def fetch_metadata(source_url: str, weak_title: bool) -> dict[str, object]:
    youtube = fetch_youtube_metadata(source_url)
    if youtube:
        return youtube

    request = Request(source_url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=15) as response:
            final_url = response.geturl()
            content_type = response.headers.get_content_type()
            title = ""
            if weak_title and content_type in {"text/html", "application/xhtml+xml"}:
                body = response.read(MAX_TITLE_BYTES)
                charset = response.headers.get_content_charset() or "utf-8"
                document = body.decode(charset, errors="replace")
                parser = TitleParser()
                parser.feed(document)
                title = parser.result()
                if not title:
                    match = re.search(
                        r'"(?:headline|name)"\s*:\s*"([^"]+)"',
                        document,
                        re.IGNORECASE,
                    )
                    if match:
                        title = " ".join(
                            html.unescape(match.group(1)).split()
                        )
            return {
                "final_url": final_url,
                "title": title,
                "status": response.status,
                "content_type": content_type,
            }
    except HTTPError as error:
        return {
            "final_url": error.geturl() or source_url,
            "title": "",
            "status": error.code,
            "content_type": error.headers.get_content_type()
            if error.headers
            else "",
            "error": type(error).__name__,
        }
    except (URLError, TimeoutError, ValueError) as error:
        return {
            "final_url": source_url,
            "title": "",
            "status": 0,
            "content_type": "",
            "error": type(error).__name__,
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()

    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    records_by_url: dict[str, dict[str, str]] = {}
    for record in payload["records"]:
        source_url = extract_source_url(record)
        if source_url and source_url not in records_by_url:
            records_by_url[source_url] = record

    cached: dict[str, dict[str, object]] = {}
    if OUTPUT.exists() and not args.refresh:
        cached = json.loads(OUTPUT.read_text(encoding="utf-8")).get(
            "entries", {}
        )

    pending = {
        source_url: record
        for source_url, record in records_by_url.items()
        if source_url not in cached
    }
    print(
        f"URLs: {len(records_by_url)}, cached: {len(cached)}, "
        f"pending: {len(pending)}",
        flush=True,
    )

    completed = 0
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {
            executor.submit(
                fetch_metadata,
                source_url,
                is_weak_title(record.get("Title", ""), source_url),
            ): source_url
            for source_url, record in pending.items()
        }
        for future in as_completed(futures):
            source_url = futures[future]
            cached[source_url] = future.result()
            completed += 1
            if completed % 25 == 0 or completed == len(pending):
                print(
                    f"Resolved {completed}/{len(pending)}",
                    flush=True,
                )

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": SOURCE.name,
        "entry_count": len(cached),
        "entries": dict(sorted(cached.items())),
    }
    temporary = OUTPUT.with_suffix(OUTPUT.suffix + ".tmp")
    temporary.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(OUTPUT)

    resolved = sum(
        item.get("final_url") and item.get("final_url") != source_url
        for source_url, item in cached.items()
    )
    titled = sum(bool(item.get("title")) for item in cached.values())
    failed = sum(not item.get("status") for item in cached.values())
    print(
        json.dumps(
            {
                "entries": len(cached),
                "redirected": resolved,
                "titles_fetched": titled,
                "failed": failed,
            },
            ensure_ascii=False,
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
