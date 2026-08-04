import json
import glob
import os
import re
import sys
from datetime import datetime
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

EXPORT_DIR = r'D:\wiki\raw\notes\Chatgpt_2026-08-02-23-14-23'
WIKI_DIR = r'D:\wiki\wiki'
INDEX_PATH = r'D:\wiki\index.md'
LOG_PATH = r'D:\wiki\log.md'

def sanitize_filename(title):
    # 특수문자 제거 및 파일명 안전하게 변경
    s = re.sub(r'[\\/:*?"<>|]', '', title).strip()
    s = re.sub(r'\s+', '_', s)
    if not s:
        s = "chat_note"
    return s[:60]

def parse_conversations():
    files = sorted(glob.glob(os.path.join(EXPORT_DIR, 'conversations-*.json')))
    all_convs = []

    for fpath in files:
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for c in data:
                title = c.get('title') or 'Untitled'
                create_time = c.get('create_time')
                date_str = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d') if create_time else '2026-08-02'
                mapping = c.get('mapping', {})
                
                # 메시지 노드 순서 정렬
                ordered_messages = []
                for node_id, node in mapping.items():
                    msg = node.get('message')
                    if not msg:
                        continue
                    role = msg.get('author', {}).get('role')
                    if role not in ['user', 'assistant']:
                        continue
                    content = msg.get('content', {})
                    parts = content.get('parts', [])
                    text_parts = [p for p in parts if isinstance(p, str) and p.strip()]
                    text = '\n'.join(text_parts).strip()
                    if not text:
                        continue
                    msg_time = msg.get('create_time') or create_time or 0
                    ordered_messages.append((msg_time, role, text))
                
                ordered_messages.sort(key=lambda x: x[0])
                
                # 필터링: 실질적인 대화 내용이 있는 건만 (총 글자 수 150자 이상)
                total_len = sum(len(m[2]) for m in ordered_messages)
                if len(ordered_messages) >= 2 and total_len >= 150:
                    all_convs.append({
                        'id': c.get('id'),
                        'title': title,
                        'date': date_str,
                        'messages': ordered_messages,
                        'total_len': total_len
                    })

    return all_convs

def categorize_conv(conv):
    title = conv['title'].lower()
    full_text = ' '.join(m[2] for m in conv['messages'][:4]).lower()
    combined = title + ' ' + full_text

    if any(k in combined for k in ['error', 'exception', 'issue', 'bug', '오류', '에러', '실패', '안됨', '해결', 'permission', 'oom', 'fail']):
        return 'errors', 'Error Note'
    elif any(k in combined for k in ['cuda', 'gpu', 'nvidia', 'b200', 'vllm', 'sglang', 'ollama', 'glm', 'deepseek', 'llm', 'model', 'inference', 'serving', 'transformer', 'lora', 'fine-tune', 'moe']):
        return 'ml', 'Concept'
    elif any(k in combined for k in ['linux', 'ssh', 'conda', 'pip', 'ubuntu', 'bash', 'terminal', 'git', 'github', 'modal', 'docker', 'env', '환경', '설치']):
        return 'infra', 'Setup Guide'
    elif any(k in combined for k in ['python', 'java', 'algorithm', 'cs', '정보처리기사', '알고리즘', '자료구조', 'soa', '클래스', '객체', '함수']):
        return 'cs', 'Concept'
    elif any(k in combined for k in ['채용', '공채', '자기소개서', '이력서', '인턴', '지원', '포트폴리오', '면접']):
        return 'projects', 'Project'
    else:
        return 'reading', 'Study Note'

def run_ingest():
    convs = parse_conversations()
    print(f"Total filtered conversations for Wiki ingest: {len(convs)}")

    cat_counts = defaultdict(int)
    created_notes = []

    for conv in convs:
        cat_dir, note_type = categorize_conv(conv)
        target_dir = os.path.join(WIKI_DIR, cat_dir, 'chatgpt-archive')
        os.makedirs(target_dir, exist_ok=True)
        
        safe_title = sanitize_filename(conv['title'])
        filename = f"{safe_title}.md"
        filepath = os.path.join(target_dir, filename)
        
        # 동명 파일 처리
        dup = 1
        while os.path.exists(filepath):
            filename = f"{safe_title}_{dup}.md"
            filepath = os.path.join(target_dir, filename)
            dup += 1

        # YAML Frontmatter 및 OKF 문서 본문 생성
        rel_path = os.path.relpath(filepath, WIKI_DIR).replace('\\', '/')
        tags_str = f"[{cat_dir}, chatgpt-export]"
        
        lines = [
            "---",
            f"type: {note_type}",
            f"title: \"{conv['title']}\"",
            f"description: \"ChatGPT 대화 내역 기반 추출 지식 노트 ({conv['date']})\"",
            f"tags: {tags_str}",
            f"timestamp: {conv['date']}",
            "status: active",
            "---",
            "",
            f"# {conv['title']}",
            "",
            f"> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  ",
            f"> **작성일**: {conv['date']}",
            "",
            "## 💬 대화 핵심 요약 및 Q&A",
            ""
        ]

        # 대화 내용 정리 (User Question / Assistant Response)
        for msg_time, role, text in conv['messages']:
            if role == 'user':
                lines.append(f"### ❓ 질문 (User)")
                lines.append(text)
                lines.append("")
            elif role == 'assistant':
                lines.append(f"### 💡 답변 (Assistant)")
                lines.append(text)
                lines.append("")
                lines.append("---")
                lines.append("")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        cat_counts[cat_dir] += 1
        created_notes.append((conv['title'], rel_path, cat_dir))

    print("\nIngest Summary by Category:")
    for cat, count in cat_counts.items():
        print(f"- wiki/{cat}/chatgpt-archive/: {count} notes created")

    # index.md에 추가 카테고리 기입
    update_index(cat_counts)
    
    # log.md에 기록
    update_log(len(created_notes))

def update_index(cat_counts):
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    if "### ChatGPT Archive" not in content:
        archive_section = "\n### ChatGPT Archive\n"
        for cat in sorted(cat_counts.keys()):
            archive_section += f"- [{cat.upper()} ChatGPT Archive](wiki/{cat}/chatgpt-archive/) - ChatGPT 대화 내역 기반 {cat_counts[cat]}개 지식 노트\n"
        
        content = content.replace("### References", archive_section + "\n### References")
        with open(INDEX_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
        print("\n[OK] Updated index.md with ChatGPT Archive section.")

def update_log(total_notes):
    today_str = datetime.now().strftime('%Y-%m-%d')
    log_entry = f"""
## {today_str}

- **Ingest**: `raw/notes/Chatgpt_2026-08-02-23-14-23` 대화 내역 중 유의미한 {total_notes}개 대화를 분석하여 OKF 형식 지식 노트(`wiki/*/chatgpt-archive/`)로 추출 및 인덱스 갱신을 완료함.
"""
    with open(LOG_PATH, 'r', encoding='utf-8') as f:
        log_content = f.read()

    # Change Log 바로 아래에 삽입
    log_content = log_content.replace("# Change Log\n", "# Change Log\n" + log_entry)
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        f.write(log_content)
    print("[OK] Updated log.md with Ingest log entry.")

if __name__ == '__main__':
    run_ingest()
