import json
import glob
import os
import re
import shutil
import sys
from datetime import datetime
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

EXPORT_DIR = r'D:\wiki\raw\notes\Chatgpt_2026-08-02-23-14-23'
WIKI_DIR = r'D:\wiki\wiki'
INDEX_PATH = r'D:\wiki\index.md'
LOG_PATH = r'D:\wiki\log.md'

def clean_old_coarse_archives():
    # 이전 개략적 chatgpt-archive 폴더 삭제
    coarse_cats = ['cs', 'errors', 'infra', 'ml', 'projects', 'reading']
    for cat in coarse_cats:
        p = os.path.join(WIKI_DIR, cat, 'chatgpt-archive')
        if os.path.exists(p):
            shutil.rmtree(p)
            print(f"[CLEAN] Removed old coarse archive: {p}")

def sanitize_filename(title):
    s = re.sub(r'[\\/:*?"<>|]', '', title).strip()
    s = re.sub(r'\s+', '_', s)
    if not s:
        s = "chat_note"
    return s[:60]

def categorize_granular(title, full_text):
    combined = (title + ' ' + full_text).lower()

    # 1. Algorithms & Data Structures
    if any(k in combined for k in ['알고리즘', '자료구조', '최단거리', '격자', '트리', '그래프', 'dp', '동적계획법', '정렬', '탐색', '코딩테스트', '백준', '프로그래머스', 'leetcode']):
        return 'algorithms/chatgpt', 'Algorithms (알고리즘 & 자료구조)', 'Concept'

    # 2. CS - Java
    if any(k in combined for k in ['java', '자바', 'jvm', 'spring', '스프링']):
        return 'cs/java/chatgpt', 'CS - Java 프로그래밍', 'Concept'

    # 3. CS - 정보처리기사
    if any(k in combined for k in ['정보처리기사', '정처기', '실기 벼락치기']):
        return 'cs/engineer_info_processing/chatgpt', 'CS - 정보처리기사', 'Study Note'

    # 4. CS - Architecture & Engineering
    if any(k in combined for k in ['soa', '아키텍처', '디자인 패턴', '소프트웨어 공학', '객체지향', '클린코드', '식별자', '도메인']):
        return 'cs/architecture/chatgpt', 'CS - Software Architecture', 'Concept'

    # 5. CS - Python
    if any(k in combined for k in ['python', '파이썬', '바다코끼리', 'pytest', 'decorator', 'generator', 'pyproject', 'dataclass', 'type hint']):
        if any(k in combined for k in ['error', 'exception', '오류', '에러', '실패', 'traceback']):
            return 'errors/python_conda/chatgpt', 'Errors - Python & Conda', 'Error Note'
        return 'cs/python/chatgpt', 'CS - Python 프로그래밍', 'Concept'

    # 6. ML - LLM Serving & Inference
    if any(k in combined for k in ['vllm', 'sglang', 'glm', '서빙', 'serving', '추측 디코딩', 'speculative', 'quantization', 'radix', 'kv cache', 'tpot', 'ttft']):
        return 'ml/llm_serving/chatgpt', 'ML - LLM Serving & Inference', 'Concept'

    # 7. ML - GPU & CUDA 가속
    if any(k in combined for k in ['cuda', 'gpu', 'nvidia', 'b200', 'gb300', 'nvlink', 'kernel', 'oom', 'triton', 'torch.cuda']):
        if any(k in combined for k in ['error', 'exception', '오류', '에러', '실패', 'out of memory']):
            return 'errors/cuda_gpu/chatgpt', 'Errors - CUDA & GPU', 'Error Note'
        return 'ml/gpu_cuda/chatgpt', 'ML - GPU & CUDA 가속', 'Concept'

    # 8. ML - Models & Theory
    if any(k in combined for k in ['deepseek', 'mamba', 'transformer', 'moe', 'lora', 'fine-tune', '파인튜닝', '학습', 'prompt', '프롬프트', 'embedding', 'rag', 'vector']):
        return 'ml/models_theory/chatgpt', 'ML - Models & Theory', 'Concept'

    # 9. Infra - Linux & Remote
    if any(k in combined for k in ['linux', '리눅스', 'ssh', 'bash', 'terminal', '권한', 'permission', 'tmux', 'ubuntu', 'chmod', 'sudo']):
        if any(k in combined for k in ['error', 'exception', '오류', '에러', '실패', 'denied']):
            return 'errors/linux_sys/chatgpt', 'Errors - Linux & System', 'Error Note'
        return 'infra/linux_ssh/chatgpt', 'Infra - Linux & Remote', 'Setup Guide'

    # 10. Infra - Cloud & DevOps
    if any(k in combined for k in ['modal', 'docker', 'git', 'github', 'conda', 'miniconda', 'pip', 'pip install']):
        return 'infra/cloud_devops/chatgpt', 'Infra - Cloud & DevOps', 'Setup Guide'

    # 11. Career & Job
    if any(k in combined for k in ['채용', '공채', '자기소개서', '이력서', '인턴', '지원', '포트폴리오', '면접', '지원서', '업스테이지', 'upstage']):
        return 'projects/career_job/chatgpt', 'Projects - Career & Job', 'Project'

    # 12. Errors - General Troubleshooting
    if any(k in combined for k in ['error', 'exception', '오류', '에러', '실패', '안됨', '해결', '트러블슈팅', 'bug', 'fix']):
        return 'errors/general/chatgpt', 'Errors - General Troubleshooting', 'Error Note'

    # 13. Reading - Tech Articles & Guides
    if any(k in combined for k in ['브리핑', '에이전트', 'agent', 'okf', 'llm wiki', '학습', '가이드', '코드 분석', '코드베이스']):
        return 'reading/tech_articles/chatgpt', 'Reading - Tech Articles & Guides', 'Study Note'

    # 14. Reading - Personal & Misc
    return 'reading/personal_misc/chatgpt', 'Reading - Personal & Misc', 'Study Note'

def parse_and_reorganize():
    clean_old_coarse_archives()
    
    files = sorted(glob.glob(os.path.join(EXPORT_DIR, 'conversations-*.json')))
    cat_counts = defaultdict(int)
    cat_names = {}
    total_notes = 0

    for fpath in files:
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for c in data:
                title = c.get('title') or 'Untitled'
                create_time = c.get('create_time')
                date_str = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d') if create_time else '2026-08-02'
                mapping = c.get('mapping', {})
                
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
                total_len = sum(len(m[2]) for m in ordered_messages)
                
                if len(ordered_messages) >= 2 and total_len >= 150:
                    full_text = ' '.join(m[2] for m in ordered_messages)
                    subpath, cat_display_name, default_type = categorize_granular(title, full_text)
                    
                    target_dir = os.path.join(WIKI_DIR, subpath.replace('/', os.sep))
                    os.makedirs(target_dir, exist_ok=True)
                    
                    safe_title = sanitize_filename(title)
                    filename = f"{safe_title}.md"
                    filepath = os.path.join(target_dir, filename)
                    
                    dup = 1
                    while os.path.exists(filepath):
                        filename = f"{safe_title}_{dup}.md"
                        filepath = os.path.join(target_dir, filename)
                        dup += 1

                    tags = [subpath.split('/')[0], 'chatgpt-export']
                    tags_str = f"[{', '.join(tags)}]"
                    
                    lines = [
                        "---",
                        f"type: {default_type}",
                        f"title: \"{title}\"",
                        f"description: \"{cat_display_name} - ChatGPT 대화 추출 노트 ({date_str})\"",
                        f"tags: {tags_str}",
                        f"timestamp: {date_str}",
                        "status: active",
                        "---",
                        "",
                        f"# {title}",
                        "",
                        f"> **카테고리**: `{cat_display_name}`  ",
                        f"> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  ",
                        f"> **작성일**: {date_str}",
                        "",
                        "## 💬 대화 내용 및 Q&A",
                        ""
                    ]

                    for msg_time, role, text in ordered_messages:
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

                    with open(filepath, 'w', encoding='utf-8') as out_f:
                        out_f.write('\n'.join(lines))
                    
                    cat_counts[subpath] += 1
                    cat_names[subpath] = cat_display_name
                    total_notes += 1

    print(f"\n[OK] Successfully reorganized {total_notes} notes into granular subcategories:")
    for subpath, count in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  - wiki/{subpath}/: {count} notes ({cat_names[subpath]})")

    update_index_granular(cat_counts, cat_names)
    update_log_granular(total_notes, len(cat_counts))

def update_index_granular(cat_counts, cat_names):
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 기존 ChatGPT Archive 섹션 제거 및 세분화 섹션으로 재작성
    if "### ChatGPT Archive" in content:
        content = content.split("### ChatGPT Archive")[0].strip() + "\n\n"

    archive_section = "### ChatGPT Archive (세분화 지식 아카이브)\n"
    for subpath in sorted(cat_counts.keys()):
        disp_name = cat_names[subpath]
        count = cat_counts[subpath]
        archive_section += f"- [{disp_name}](wiki/{subpath}/) - {count}개 지식 노트\n"

    archive_section += "\n### References\n"
    if "### References" in content:
        content = content.split("### References")[0].strip() + "\n\n" + archive_section + content.split("### References")[1]
    else:
        content = content + "\n\n" + archive_section

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print("\n[OK] Updated index.md with granular ChatGPT Archive subcategories.")

def update_log_granular(total_notes, cat_num):
    today_str = datetime.now().strftime('%Y-%m-%d')
    log_entry = f"""
## {today_str}

- **Refactor**: ChatGPT 674개 대화 내역을 단순 6개 분류에서 **{cat_num}개 세부 기술 카테고리**(알고리즘, Python, Java, 정처기, 아키텍처, LLM 서빙, GPU/CUDA, 모델이론, 리눅스, DevOps, 채용, 에러 트러블슈팅 등)로 세분화 재구성하여 {total_notes}개 지식 노트를 배치함.
"""
    with open(LOG_PATH, 'r', encoding='utf-8') as f:
        log_content = f.read()

    # Change Log 최상단 갱신
    if f"## {today_str}" in log_content:
        # 오늘 날짜 로그 항목에 이어붙이기
        log_content = log_content.replace(f"## {today_str}\n", f"## {today_str}\n" + f"- **Refactor**: ChatGPT 대화 내역을 {cat_num}개 세부 기술 카테고리로 재구성하여 {total_notes}개 지식 노트 배치 완료.\n")
    else:
        log_content = log_content.replace("# Change Log\n", "# Change Log\n" + log_entry)

    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        f.write(log_content)
    print("[OK] Updated log.md with granular Refactor log entry.")

if __name__ == '__main__':
    parse_and_reorganize()
