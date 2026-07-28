#!/usr/bin/env python3
"""Build a local reading library from a Notion resource snapshot."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "raw" / "notion" / "resource-library-2026-07-24.json"
URL_METADATA_SOURCE = (
    ROOT / "raw" / "notion" / "resource-library-url-metadata-2026-07-24.json"
)
OUTPUT = ROOT / "wiki" / "reading"

URL_PATTERN = re.compile(r"https?://[^\s<>\"]+")
TRACKING_PARAMS = {
    "data",
    "eid",
    "lipi",
    "midSig",
    "midToken",
    "otpToken",
    "pp",
    "si",
    "shem",
    "source",
    "surface",
    "tc",
    "trk",
    "trkEmail",
}


@dataclass(frozen=True)
class Category:
    slug: str
    title: str
    description: str
    keywords: tuple[str, ...]


CATEGORIES = (
    Category(
        "ai-agents",
        "AI 에이전트와 코딩 도구",
        "에이전트, 코딩 에이전트, 하니스, MCP 및 자동화 도구",
        (
            "agentic",
            "agent",
            "claude code",
            "codex",
            "harness",
            "openclaw",
            "claw",
            "langgraph",
            "mcp",
            "multi-agent",
            "에이전트",
            "바이브 코딩",
            "코딩 도구",
            "코딩 에이전트",
        ),
    ),
    Category(
        "ml-research",
        "AI/ML 연구와 모델",
        "논문, 언어 모델, RAG, 강화학습, 모델 학습 및 평가",
        (
            "arxiv",
            "openreview",
            "huggingface",
            "pytorch",
            "machine learning",
            "deep learning",
            "language model",
            "transformer",
            "llm",
            "rag",
            "reinforcement learning",
            "fine-tun",
            "benchmark",
            "diffusion",
            "vlm",
            "모델",
            "논문",
            "머신러닝",
            "딥러닝",
            "강화학습",
        ),
    ),
    Category(
        "data-infra",
        "데이터와 인프라",
        "데이터 엔지니어링, 데이터베이스, GPU, 서빙 및 운영 인프라",
        (
            "data engineering",
            "database",
            "sql",
            "spark",
            "cuda",
            "gpu",
            "infra",
            "vllm",
            "triton",
            "serving",
            "recommendation",
            "visualization",
            "시계열",
            "데이터",
            "인프라",
            "로그",
        ),
    ),
    Category(
        "software-engineering",
        "소프트웨어 엔지니어링",
        "프로그래밍, 설계, 코드 리뷰, 프레임워크 및 개발 실무",
        (
            "github.com",
            "software",
            "python",
            "java",
            "fastapi",
            "django",
            "developer",
            "programming",
            "code review",
            "over-engineering",
            "프로그래밍",
            "개발자",
            "코드 리뷰",
            "소프트웨어",
        ),
    ),
    Category(
        "learning-career",
        "학습과 커리어",
        "강의, 교재, 학습 로드맵, 취업 및 성장 자료",
        (
            "course",
            "curriculum",
            "syllabus",
            "book",
            "learn",
            "career",
            "interview",
            "certification",
            "roadmap",
            "study",
            "training",
            "채용",
            "취업",
            "교재",
            "도서",
            "강의",
            "학습",
            "커리어",
            "로드맵",
        ),
    ),
    Category(
        "math-statistics",
        "수학과 통계",
        "수학, 통계, 최적화 및 이론 자료",
        (
            "mathemat",
            "statistics",
            "statistical",
            "measure",
            "optimization",
            "shortest path",
            "수학",
            "통계",
            "측도",
            "최적화",
            "알고리즘",
        ),
    ),
    Category(
        "business-productivity",
        "비즈니스와 생산성",
        "제품, 조직, 생산성, 마케팅, 재무 및 1인 비즈니스",
        (
            "business",
            "productivity",
            "marketing",
            "finance",
            "roi",
            "saas",
            "startup",
            "product",
            "생산성",
            "비즈니스",
            "마케팅",
            "재무",
            "기업",
            "서비스",
        ),
    ),
    Category(
        "personal-misc",
        "개인 관심사와 미분류",
        "다른 분류에 포함되지 않은 개인 자료와 확인이 필요한 링크",
        (),
    ),
)

CATEGORY_BY_SLUG = {category.slug: category for category in CATEGORIES}


@dataclass
class Resource:
    key: str
    title: str
    source_url: str
    canonical_url: str
    date_added: str
    notes: list[str] = field(default_factory=list)
    notion_urls: list[str] = field(default_factory=list)
    notion_categories: set[str] = field(default_factory=set)
    category: str = ""
    kind: str = ""


def clean_url(value: str) -> str:
    return value.strip().rstrip(".,);]}>")


def extract_source_url(record: dict[str, str]) -> str:
    explicit = clean_url(record.get("userDefined:URL", ""))
    if explicit:
        return explicit

    match = URL_PATTERN.search(record.get("Title", ""))
    return clean_url(match.group(0)) if match else ""


def load_url_metadata() -> dict[str, dict[str, object]]:
    if not URL_METADATA_SOURCE.exists():
        return {}
    payload = json.loads(URL_METADATA_SOURCE.read_text(encoding="utf-8"))
    return payload.get("entries", {})


URL_METADATA = load_url_metadata()


def metadata_for_url(value: str) -> dict[str, object]:
    return URL_METADATA.get(clean_url(value), {})


def resolve_url(value: str) -> str:
    metadata = metadata_for_url(value)
    final_url = str(metadata.get("final_url", "")).strip()
    if final_url:
        original_path = urlparse(value).path.casefold()
        final_path = urlparse(final_url).path.casefold()
        auth_markers = ("/login", "/signin", "/auth", "/uas/")
        redirected_to_auth = any(
            marker in final_path and marker not in original_path
            for marker in auth_markers
        )
        if redirected_to_auth:
            final_url = ""
    return clean_url(final_url or value)


def canonicalize_url(value: str) -> str:
    if not value:
        return ""

    value = resolve_url(value)
    parsed = urlparse(value)
    host = parsed.netloc.lower().removeprefix("m.").removeprefix("www.")
    path = parsed.path.rstrip("/") or "/"
    query = parse_qsl(parsed.query, keep_blank_values=True)

    if host == "youtu.be":
        video_id = path.strip("/").split("/")[0]
        return f"https://www.youtube.com/watch?v={video_id}"

    if host == "youtube.com":
        if path.startswith("/shorts/"):
            video_id = path.split("/")[2]
            return f"https://www.youtube.com/watch?v={video_id}"
        if path == "/watch":
            video_id = dict(query).get("v", "")
            if video_id:
                return f"https://www.youtube.com/watch?v={video_id}"

    filtered_query = [
        (key, item)
        for key, item in query
        if not key.lower().startswith("utm_") and key not in TRACKING_PARAMS
    ]
    return urlunparse(
        (
            parsed.scheme.lower() or "https",
            parsed.netloc.lower(),
            path,
            "",
            urlencode(filtered_query),
            "",
        )
    )


GENERIC_TITLES = {
    "arxiv.org",
    "github.com",
    "medium.com",
    "x.com",
    "youtu.be",
    "youtube.com",
}


def is_weak_title(value: str, source_url: str) -> bool:
    title = " ".join(value.split()).strip()
    if not title or title.startswith(("http://", "https://")):
        return True
    lowered = title.casefold()
    normalized = lowered.removeprefix("www.")
    if lowered.startswith("source:") or normalized in GENERIC_TITLES:
        return True
    if source_url:
        host = urlparse(source_url).netloc.casefold().removeprefix("www.")
        if normalized in {host, host.split(".", 1)[0]}:
            return True
    return False


def enrich_title(current: str, fetched: str, source_url: str) -> str:
    fetched = " ".join(fetched.split()).strip()
    if not fetched:
        return current
    if is_weak_title(current, source_url):
        return fetched
    if len(current) <= 12 and len(fetched) >= len(current) + 8:
        return fetched
    return current


def choose_title(current: str, candidate: str, source_url: str) -> str:
    candidate = " ".join(candidate.split())
    if not candidate or candidate.startswith(("http://", "https://")):
        return current
    if not current or current.startswith(("Source:", "GitHub -")):
        return candidate
    if current.startswith("Source:") and not candidate.startswith("Source:"):
        return candidate
    return current


def classify(resource: Resource) -> str:
    haystack = " ".join(
        [resource.title, resource.source_url, *resource.notes]
    ).casefold()
    for category in CATEGORIES[:-1]:
        if any(keyword.casefold() in haystack for keyword in category.keywords):
            return category.slug
    return CATEGORIES[-1].slug


def detect_kind(resource: Resource) -> str:
    value = resource.source_url.casefold()
    title = resource.title.casefold()
    if not value:
        return "note"
    if "youtube.com" in value or "youtu.be" in value:
        return "video"
    if "arxiv.org" in value or "openreview.net" in value or "/doi/" in value:
        return "paper"
    if "github.com" in value:
        return "repository"
    if "huggingface.co" in value:
        return "model-or-paper"
    if value.endswith((".pdf", ".png", ".jpg", ".jpeg")):
        return "document"
    if any(keyword in title for keyword in ("course", "syllabus", "강의", "교재")):
        return "course"
    return "article"


def load_resources() -> list[Resource]:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    resources: dict[str, Resource] = {}

    records = sorted(
        payload["records"],
        key=lambda record: record.get("Date Added", ""),
        reverse=True,
    )
    for record in records:
        original_url = extract_source_url(record)
        metadata = metadata_for_url(original_url)
        source_url = resolve_url(original_url)
        canonical_url = canonicalize_url(original_url)
        raw_title = record.get("Title", "").strip()
        fallback_title = (
            urlparse(source_url).netloc
            if source_url
            else f"제목 없는 Notion 항목 {record.get('url', '')[-8:]}"
        )
        title = choose_title("", raw_title, source_url) or fallback_title
        title = enrich_title(
            title,
            str(metadata.get("title", "")),
            source_url,
        )
        key = canonical_url.casefold() if canonical_url else hashlib.sha1(
            (title + record.get("url", "")).encode("utf-8")
        ).hexdigest()

        if key in resources:
            continue

        resources[key] = Resource(
            key=key,
            title=title,
            source_url=source_url,
            canonical_url=canonical_url,
            date_added=record.get("Date Added", "")[:10],
        )
        resource = resources[key]

        note = record.get("Notes", "").strip()
        if note and note not in resource.notes:
            resource.notes.append(note)

        notion_url = record.get("url", "").strip()
        if notion_url and notion_url not in resource.notion_urls:
            resource.notion_urls.append(notion_url)

        raw_categories = record.get("Category", "")
        if raw_categories:
            try:
                resource.notion_categories.update(json.loads(raw_categories))
            except json.JSONDecodeError:
                resource.notion_categories.add(raw_categories)

    result = list(resources.values())
    for resource in result:
        resource.category = classify(resource)
        resource.kind = detect_kind(resource)
    return sorted(result, key=lambda item: (item.date_added, item.title), reverse=True)


def frontmatter(
    *,
    title: str,
    description: str,
    tags: list[str],
) -> list[str]:
    return [
        "---",
        "type: Reference",
        f"title: {title}",
        f"description: {description}",
        f"tags: [{', '.join(tags)}]",
        "timestamp: 2026-07-24",
        "status: active",
        "---",
        "",
        "<!-- Generated by scripts/import_notion_resource_library.py. -->",
        "",
    ]


def display_title(resource: Resource) -> str:
    return resource.title.replace("[", r"\[").replace("]", r"\]")


def compact_note(value: str, limit: int = 320) -> str:
    compact = " ".join(value.split())
    return compact if len(compact) <= limit else compact[: limit - 1] + "…"


def render_resource(resource: Resource) -> list[str]:
    title = display_title(resource)
    if resource.source_url:
        lines = [f"## [{title}]({resource.source_url})"]
    else:
        lines = [f"## {title}"]

    lines.extend(
        [
            "",
            "- 상태: `unread`",
            f"- 형식: `{resource.kind}`",
            f"- 추가일: {resource.date_added or '확인 필요'}",
        ]
    )
    if resource.notion_urls:
        links = ", ".join(
            f"[항목 {index + 1}]({url})"
            for index, url in enumerate(resource.notion_urls)
        )
        lines.append(f"- Notion 원본: {links}")
    if resource.notion_categories:
        lines.append(
            "- Notion 분류: "
            + ", ".join(sorted(category.strip() for category in resource.notion_categories))
        )
    for note in resource.notes:
        lines.append(f"- 기존 메모: {compact_note(note)}")
    if not resource.source_url:
        lines.append("- 확인: 원문 URL이 없어 Notion 항목에서 링크를 보완해야 함")
    lines.append("")
    return lines


def write_category_files(resources: list[Resource]) -> dict[str, int]:
    counts = Counter(resource.category for resource in resources)
    for category in CATEGORIES:
        selected = [
            resource for resource in resources if resource.category == category.slug
        ]
        lines = frontmatter(
            title=category.title,
            description=category.description,
            tags=["reading", "resource-library", category.slug],
        )
        lines.extend(
            [
                "# Summary",
                "",
                f"Notion 읽기 목록에서 자동 분류한 자료 {len(selected)}개입니다.",
                "원문을 실제로 읽고 정리한 뒤 관련 concept 또는 paper note로 승격합니다.",
                "",
                "# Resources",
                "",
            ]
        )
        for resource in selected:
            lines.extend(render_resource(resource))
        (OUTPUT / f"{category.slug}.md").write_text(
            "\n".join(lines).rstrip() + "\n", encoding="utf-8"
        )
    return dict(counts)


def load_checked_resources() -> set[str]:
    inbox_path = OUTPUT / "inbox.md"
    if not inbox_path.exists():
        return set()

    checked: set[str] = set()
    for line in inbox_path.read_text(encoding="utf-8").splitlines():
        if not re.match(r"^- \[[xX]\] ", line):
            continue
        link_match = re.search(r"\]\((https?://[^)]+)\)", line)
        if link_match:
            checked.add(canonicalize_url(link_match.group(1)).casefold())
            continue
        title = line[6:].split(" — ", 1)[0].strip()
        checked.add(f"title:{title.casefold()}")
    return checked


def write_inbox(resources: list[Resource], checked: set[str]) -> None:
    lines = frontmatter(
        title="Notion 읽기 목록 전체 수집함",
        description="Notion Second Brain에서 가져온 자료를 최신순으로 확인하는 체크리스트",
        tags=["reading", "inbox", "notion"],
    )
    lines.extend(
        [
            "# Reading Inbox",
            "",
            "체크 표시는 이 파일에서 관리할 수 있습니다. 상세 정보는 각 분류 문서에 있습니다.",
            "",
        ]
    )
    for resource in resources:
        category = CATEGORY_BY_SLUG[resource.category]
        title = display_title(resource)
        checked_key = (
            resource.canonical_url.casefold()
            if resource.canonical_url
            else f"title:{title.casefold()}"
        )
        mark = "x" if checked_key in checked else " "
        if resource.source_url:
            label = f"[{title}]({resource.source_url})"
        else:
            label = title
        lines.append(
            f"- [{mark}] {label} — {category.title} · `{resource.kind}` · {resource.date_added}"
        )
    (OUTPUT / "inbox.md").write_text(
        "\n".join(lines).rstrip() + "\n", encoding="utf-8"
    )


def write_title_review(resources: list[Resource]) -> None:
    unresolved = [
        resource
        for resource in resources
        if is_weak_title(resource.title, resource.source_url)
    ]
    metadata_by_canonical: dict[str, dict[str, object]] = {}
    for original_url, metadata in URL_METADATA.items():
        canonical = canonicalize_url(original_url)
        if canonical:
            metadata_by_canonical.setdefault(canonical.casefold(), metadata)

    lines = frontmatter(
        title="제목 수동 확인 목록",
        description="원문 조회 후에도 제목을 충분히 식별하지 못한 읽기 자료",
        tags=["reading", "maintenance", "title-review"],
    )
    lines.extend(
        [
            "# Summary",
            "",
            f"원문 메타데이터 조회 후에도 제목 확인이 필요한 자료는 {len(unresolved)}개입니다.",
            "삭제·비공개 자료, 접근 차단, PDF·이미지, 로그인 전용 페이지가 주된 원인입니다.",
            "",
            "# Items",
            "",
        ]
    )
    for resource in unresolved:
        metadata = metadata_by_canonical.get(
            resource.canonical_url.casefold(), {}
        )
        status = metadata.get("status") or "연결 실패"
        content_type = metadata.get("content_type") or "확인 불가"
        error = metadata.get("error")
        reason = f"HTTP {status} · `{content_type}`"
        if error:
            reason += f" · `{error}`"
        title = display_title(resource)
        label = (
            f"[{title}]({resource.source_url})"
            if resource.source_url
            else title
        )
        lines.extend(
            [
                f"## {label}",
                "",
                f"- 추가일: {resource.date_added or '확인 필요'}",
                f"- 조회 결과: {reason}",
                "",
            ]
        )
    (OUTPUT / "title-review.md").write_text(
        "\n".join(lines).rstrip() + "\n", encoding="utf-8"
    )


def write_index(
    *,
    source_count: int,
    resources: list[Resource],
    counts: dict[str, int],
) -> None:
    duplicate_count = source_count - len(resources)
    no_url_count = sum(not resource.source_url for resource in resources)
    weak_title_count = sum(
        is_weak_title(resource.title, resource.source_url)
        for resource in resources
    )
    lines = frontmatter(
        title="읽기 자료실",
        description="Notion에 저장한 글, 논문, 영상과 도구 링크를 로컬에서 읽고 정리하는 수집함",
        tags=["reading", "resource-library", "notion"],
    )
    lines.extend(
        [
            "# Summary",
            "",
            f"Notion 원본 {source_count}개를 가져와 최종 URL 기준 {len(resources)}개로 정리했습니다.",
            f"중복 {duplicate_count}개를 합쳤고 원문 URL이 없는 항목은 {no_url_count}개입니다.",
            "",
            "- [전체 읽기 체크리스트](inbox.md)",
            "- [전체 처리 현황](progress.md)",
            "- [최근 20개 재작성 요약](notes/index.md)",
            f"- [제목 수동 확인 목록](title-review.md) - {weak_title_count}개",
            "- [Notion 원본 데이터베이스](https://app.notion.com/p/5f61a73cf20b82f2a3d501dbde31bf8f)",
            "- [가져오기 원본](../../raw/notion/resource-library-2026-07-24.json)",
            "",
            "# Categories",
            "",
            "| 분류 | 자료 수 | 설명 |",
            "| --- | ---: | --- |",
        ]
    )
    for category in CATEGORIES:
        lines.append(
            f"| [{category.title}]({category.slug}.md) | "
            f"{counts.get(category.slug, 0)} | {category.description} |"
        )
    lines.extend(
        [
            "",
            "# Workflow",
            "",
            "1. `inbox.md`에서 읽을 자료를 고릅니다.",
            "2. 원문을 읽고 핵심 주장, 근거, 적용 아이디어를 정리합니다.",
            "3. 재사용 가치가 있으면 기존 wiki 문서에 통합하거나 새 concept/paper note를 만듭니다.",
            "4. 관련 문서에 cross-link를 추가하고 이 목록의 상태를 갱신합니다.",
            "",
            "# Import Notes",
            "",
            "- 자동 분류는 보정된 원문 제목, 최종 URL, 기존 메모의 키워드를 기준으로 한 1차 분류입니다.",
            "- 단축 URL과 불명확한 제목은 `raw/notion/resource-library-url-metadata-2026-07-24.json`의 조회 결과로 보정합니다.",
            "- 접근이 차단되거나 삭제된 원문은 저장된 제목과 URL을 유지하므로 수동 확인이 필요합니다.",
            "- 생성된 분류 문서는 스크립트를 다시 실행하면 갱신됩니다. 재작성 요약은 `notes/`에 보존합니다.",
        ]
    )
    (OUTPUT / "index.md").write_text(
        "\n".join(lines).rstrip() + "\n", encoding="utf-8"
    )


def main() -> None:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    resources = load_resources()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    checked = load_checked_resources()
    counts = write_category_files(resources)
    write_inbox(resources, checked)
    write_title_review(resources)
    write_index(
        source_count=payload["record_count"],
        resources=resources,
        counts=counts,
    )
    print(
        json.dumps(
            {
                "source_records": payload["record_count"],
                "unique_resources": len(resources),
                "duplicates_merged": payload["record_count"] - len(resources),
                "without_source_url": sum(
                    not resource.source_url for resource in resources
                ),
                "categories": counts,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
