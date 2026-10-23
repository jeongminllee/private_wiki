"""Audit daily routine files without changing them; optionally rebuild their index."""

import argparse
from collections import Counter, defaultdict
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


REPO_DIR = Path(__file__).resolve().parents[1]
ROUTINE_DIR = REPO_DIR / "wiki" / "routine"
SUBJECTS = {
    "ai_paper": "AI Paper & Tech",
    "economy": "경제 브리핑",
    "Eng": "영어 학습",
    "Job_LLM_ML": "LLM/ML 채용",
    "checklist": "체크리스트",
}
DAY_NAME = re.compile(r"\d{4}-\d{2}-\d{2}\.md$")


def split_frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return "missing", {}, text
    for end in range(1, len(lines)):
        if lines[end].strip() == "---":
            indented = lines[0] != "---" or lines[end] != "---"
            fields = {}
            for line in lines[1:end]:
                key, sep, value = line.strip().partition(":")
                if sep:
                    fields[key] = value.strip().strip("\"'")
            return "indented" if indented else "present", fields, "\n".join(lines[end + 1:])
    return "unclosed", {}, text


def body_has_content(body, fields):
    # Generated planned notes contain only section headings and a navigation link.
    ignored = {"<!-- 작성 예정 -->"}
    lines = [line.strip() for line in body.splitlines()]
    if fields.get("status") == "planned":
        lines = [line for line in lines if "해당 날짜 체크리스트" not in line]
    return any(
        line and line not in ignored and not line.startswith("#")
        and not re.fullmatch(r"[-*_]{3,}", line)
        for line in lines
    )


def local_links(path, text):
    # Check inline Markdown file links outside fenced code; do not fetch web URLs.
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            if fence is None:
                fence = marker.group(1)[0]
            elif marker.group(1)[0] == fence:
                fence = None
            continue
        if fence:
            continue
        for match in re.finditer(r"\[[^\]]*\]\((<[^>]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\)", line):
            target = match.group(1).strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            link_path = unquote(parsed.path)
            resolved = (REPO_DIR / link_path.lstrip("/")) if link_path.startswith("/") else path.parent / link_path
            yield target, resolved.resolve()


def audit():
    entries = []
    broken = []
    duplicates = defaultdict(list)
    by_subject = {}
    session_artifacts = []
    for subject in SUBJECTS:
        paths = sorted(path for path in (ROUTINE_DIR / subject).rglob("*.md") if DAY_NAME.fullmatch(path.name))
        rows = []
        for path in paths:
            text = path.read_text(encoding="utf-8-sig")
            state, fields, body = split_frontmatter(text)
            item = {
                "subject": subject,
                "date": path.stem,
                "path": path.relative_to(ROUTINE_DIR).as_posix(),
                "frontmatter": state,
                "type_missing": not fields.get("type"),
                "description_missing": not fields.get("description"),
                "has_content": body_has_content(body, fields),
                "checked": len(re.findall(r"^\s*- \[[xX]\]", body, re.M)),
                "checkboxes": len(re.findall(r"^\s*- \[[ xX]\]", body, re.M)),
            }
            if subject == "Eng" and "이 날은 주말이므로" in body:
                item["note_kind"] = "휴식 안내"
            elif subject == "Job_LLM_ML" and "신규 알림 기준 충족 공고 없음" in body:
                item["note_kind"] = "공고 없음"
            else:
                item["note_kind"] = "본문" if item["has_content"] else "빈 틀"
            rows.append(item)
            entries.append(item)
            residuals = {
                "content_reference": text.count(":chatgpt-content-reference{"),
                "internal_cite": text.count("\ue200cite"),
                "internal_url": text.count("\ue200url"),
                "sandbox_links": len(re.findall(r"\]\(sandbox:[^)]+\)", text)),
            }
            if any(residuals.values()):
                session_artifacts.append({"path": item["path"], **residuals})
            if subject != "checklist" and item["has_content"]:
                duplicates[hashlib.sha256(text.encode("utf-8")).hexdigest()].append(item["path"])
            for target, resolved in local_links(path, text):
                if not resolved.exists():
                    broken.append({"path": item["path"], "target": target})
        by_subject[subject] = rows
    days = sorted({row["date"] for row in entries})
    expected = []
    if days:
        current, last = date.fromisoformat(days[0]), date.fromisoformat(days[-1])
        while current <= last:
            expected.append(current.isoformat())
            current += timedelta(days=1)
    summary = {}
    for subject, rows in by_subject.items():
        summary[subject] = {
            "files": len(rows),
            "with_body": sum(row["has_content"] for row in rows),
            "empty_templates": sum(not row["has_content"] for row in rows),
            "frontmatter": dict(Counter(row["frontmatter"] for row in rows)),
            "type_missing": sum(row["type_missing"] for row in rows),
            "description_missing": sum(row["description_missing"] for row in rows),
            "missing_dates": sorted(set(expected) - {row["date"] for row in rows}),
        }
    indexed = set()
    index_path = ROUTINE_DIR / "index.md"
    if index_path.exists():
        indexed = {resolved for _, resolved in local_links(index_path, index_path.read_text(encoding="utf-8-sig"))}
    unindexed = [row["path"] for row in entries if (ROUTINE_DIR / row["path"]).resolve() not in indexed]
    content_rows = {(row["date"], row["subject"]): row for row in entries}
    unchecked_with_body = defaultdict(list)
    for checklist in by_subject["checklist"]:
        text = (ROUTINE_DIR / checklist["path"]).read_text(encoding="utf-8-sig")
        for subject in SUBJECTS:
            if subject == "checklist":
                continue
            row = content_rows.get((checklist["date"], subject))
            unchecked = re.search(r"^\s*- \[ \].*\]\(\.\./" + re.escape(subject) + r"/", text, re.M)
            if row and row["has_content"] and unchecked:
                unchecked_with_body[subject].append(checklist["date"])
    return {
        "period": [days[0], days[-1]] if days else [],
        "days": len(days),
        "files": len(entries),
        "subjects": summary,
        "broken_local_links": broken,
        "exact_duplicates_with_body": [paths for paths in duplicates.values() if len(paths) > 1],
        "session_artifacts": session_artifacts,
        "not_in_routine_index": unindexed,
        "unchecked_with_body": dict(unchecked_with_body),
        "checked_items": sum(row["checked"] for row in by_subject["checklist"]),
        "checkbox_items": sum(row["checkboxes"] for row in by_subject["checklist"]),
        "entries": entries,
    }


def render_index(result):
    entries = {(row["date"], row["subject"]): row for row in result["entries"]}
    days = sorted({row["date"] for row in result["entries"]}, reverse=True)
    lines = [
        "# 데일리 루틴", "",
        "<!-- Generated by scripts/audit_routine.py --write-index. Edit the generator for persistent changes. -->", "",
        "날짜별 AI·경제·영어·채용 기록과 체크리스트의 진입점입니다. 기존 기록의 위치와 본문은 유지합니다.", "",
        "- [루틴 운영 및 생성 방법](../../README.md) - 당일 생성과 점검 명령",
        "- [2026-10-13 점검 기록](../_maintenance/routine-audit-2026-10-13.md) - 형식 문제, 미체크 후보와 후속 정리 범위",
        "- [전체 지식베이스](../../index.md) - 관련 개념과 프로젝트 찾기", "",
        "## 최근 기록", "",
    ]
    for day in days[:7]:
        row = entries.get((day, "checklist"))
        if row:
            lines.append(f"- [{day} 체크리스트]({row['path']}) - 표시된 완료 {row['checked']}/{row['checkboxes']}")
    lines += ["", "## 분류별 현황", "", "| 분류 | 기록 수 | 본문 있음 | 빈 틀 |", "| --- | ---: | ---: | ---: |"]
    for subject, title in SUBJECTS.items():
        stats = result["subjects"][subject]
        lines.append(f"| [{title}]({subject}/) | {stats['files']} | {stats['with_body']} | {stats['empty_templates']} |")
    lines += [
        "", "‘본문 있음’은 텍스트가 입력됐다는 뜻입니다. 학습 완료나 원문 검증을 뜻하지 않으며, 휴식·신규 공고 없음 안내도 포함됩니다.",
        "체크리스트의 완료 표시는 기존 값을 그대로 읽습니다. `빈 틀`은 제목만 있거나 생성 템플릿만 남은 파일입니다.", "",
        "## 날짜별 기록", "",
        f"{result['period'][0]} ~ {result['period'][-1]} · {result['days']}일 · {result['files']}개 날짜별 문서" if days else "아직 날짜별 기록이 없습니다.", "",
    ]
    months = sorted({day[:7] for day in days}, reverse=True)
    for month in months:
        lines += [f"### {month}", "", "| 날짜 / 체크리스트 | AI | 경제 | 영어 | 채용 | 완료 표시 |", "| --- | --- | --- | --- | --- | ---: |"]
        for day in (day for day in days if day.startswith(month)):
            checklist = entries.get((day, "checklist"))
            cells = [f"[{day}]({checklist['path']})" if checklist else day]
            for subject in ("ai_paper", "economy", "Eng", "Job_LLM_ML"):
                row = entries.get((day, subject))
                cells.append(f"[{row['note_kind']}]({row['path']})" if row else "누락")
            cells.append(f"{checklist['checked']}/{checklist['checkboxes']}" if checklist else "—")
            lines.append("| " + " | ".join(cells) + " |")
        lines.append("")
    lines += [
        "## 관련 지식", "",
        "- [논문 노트](../papers/index.md) - 검증 후 재사용할 연구 내용 정리",
        "- [LLM 생명주기 환경 설계](../infra/llm-lifecycle-environment-design.md) - 학습·서빙·평가 인프라 연결",
        "- [Fine-Tuned 프로젝트](../projects/Fine_Tuned/index.md) - AI 브리핑의 적용 아이디어 검토",
        "- [학습과 커리어 자료](../reading/learning-career.md) - 영어·채용 기록과 함께 볼 자료", "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="날짜별 루틴의 파일·형식·내부 링크 점검 (본문 수정 없음)")
    parser.add_argument("--write-index", action="store_true", help="wiki/routine/index.md만 재생성")
    parser.add_argument("--details", action="store_true", help="파일별 점검 결과도 JSON 출력")
    args = parser.parse_args()
    result = audit()
    if args.write_index:
        (ROUTINE_DIR / "index.md").write_text(render_index(result), encoding="utf-8")
        result["not_in_routine_index"] = []
    if not args.details:
        result.pop("entries")
        result["session_artifacts"] = {
            "files": len(result["session_artifacts"]),
            "counts": dict(Counter({key: sum(row[key] for row in result["session_artifacts"]) for key in ("content_reference", "internal_cite", "internal_url", "sandbox_links")})),
        }
        result["not_in_routine_index"] = len(result["not_in_routine_index"])
        result["unchecked_with_body"] = {subject: len(days) for subject, days in result["unchecked_with_body"].items()}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
