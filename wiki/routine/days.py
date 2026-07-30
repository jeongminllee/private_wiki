import os
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROUTINE_DIR = SCRIPT_DIR

def create_daily_routine():
    today = date.today().strftime('%Y-%m-%d')
    subjects = ['economy', 'ai_paper', 'Eng', 'Job_LLM_ML']
    
    # 1. 4개 과목별 날짜 폴더 및 md 생성
    for sub in subjects:
        folder_path = os.path.join(ROUTINE_DIR, sub, today)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{today}.md")
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {sub} - {today}\n\n")

    # 2. wiki/routine/checklist/YYYY-MM-DD.md 체크리스트 생성
    checklist_dir = os.path.join(ROUTINE_DIR, 'checklist')
    os.makedirs(checklist_dir, exist_ok=True)
    checklist_path = os.path.join(checklist_dir, f"{today}.md")
    
    if not os.path.exists(checklist_path):
        template = f"""---
type: Study Note
title: Daily Routine Checklist {today}
description: Checklist for daily study routine items
tags: [routine, checklist]
timestamp: {today}
status: active
---

# {today} Daily Routine Checklist

- [ ] 🤖 [AI Paper & Tech 브리핑](../ai_paper/{today}/{today}.md)
- [ ] 📈 [미국 경제 아침 브리핑](../economy/{today}/{today}.md)
- [ ] 🔤 [영어 학습](../Eng/{today}/{today}.md)
- [ ] 💼 [LLM/ML 채용 공고 점검](../Job_LLM_ML/{today}/{today}.md)
"""
        with open(checklist_path, 'w', encoding='utf-8') as f:
            f.write(template)

    print(f"[OK] {today} 루틴 폴더 4개와 체크리스트 작성이 완료되었습니다!")
    print(f"    - 체크리스트: {checklist_path}")

if __name__ == '__main__':
    create_daily_routine()
    print("\nPress Enter to exit...")
    try:
        input()
    except EOFError:
        pass
