#!/usr/bin/env python3
"""Check generated data quality"""
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

d = json.load(open('api/data.json', 'r', encoding='utf-8'))

print('=== DATA OVERVIEW ===')
print(f'Levels: {len(d["levels"])}')
print(f'Subjects: {len(d["subjects"])}')
print(f'Content: {len(d["content"])}')

print('\n=== SAMPLE CONTENT ITEMS ===')
for i, c in enumerate(d['content'][:8]):
    print(f'\n{i+1}. {c["title"]}')
    print(f'   Arabic: {c["title_ar"]}')
    print(f'   Type: {c["content_type"]}')
    print(f'   Level: {c["level_id"]}')
    print(f'   Subject: {c["subject_id"]}')
    if c.get('chapter'): 
        print(f'   Chapter: {c["chapter"]}')

print('\n=== SAMPLE SUBJECTS ===')
for s in d['subjects'][:8]:
    print(f'{s["name"]} ({s["name_ar"]}) - {s["level_name"]} - Content: {s["content_count"]}')

print('\n=== CONTENT PER LEVEL ===')
level_counts = {}
for c in d['content']:
    lid = c['level_id']
    level_counts[lid] = level_counts.get(lid, 0) + 1

level_order = {l['id']: l['order'] for l in d['levels']}
for lid in sorted(level_counts.keys(), key=lambda x: level_order.get(x, 99)):
    lname = next((l['name'] for l in d['levels'] if l['id'] == lid), lid)
    print(f'  {lname}: {level_counts[lid]} items')

print('\n=== CONTENT TYPES DISTRIBUTION ===')
ct = {}
for c in d['content']:
    t = c['content_type']
    ct[t] = ct.get(t, 0) + 1
for t, count in sorted(ct.items(), key=lambda x: -x[1]):
    print(f'  {t}: {count}')

print('\n=== SUBJECTS PER LEVEL CATEGORY ===')
cat_subj = {'primaire': 0, 'college': 0, 'lycee': 0}
for s in d['subjects']:
    cat = s.get('category', 'unknown')
    if cat in cat_subj:
        cat_subj[cat] += 1
for cat, count in cat_subj.items():
    print(f'  {cat}: {count} subjects')

print('\n=== ISSUES CHECK ===')
issues = []

# Check for empty titles
empty_titles = [c for c in d['content'] if not c.get('title')]
if empty_titles:
    issues.append(f'Empty titles: {len(empty_titles)}')

# Check for empty Arabic
empty_ar = [c for c in d['content'] if not c.get('title_ar')]
if empty_ar:
    issues.append(f'Missing Arabic titles: {len(empty_ar)}')

# Check for missing subject_id
missing_subj = [c for c in d['content'] if not c.get('subject_id')]
if missing_subj:
    issues.append(f'Missing subject_id: {len(missing_subj)}')

# Check subject content counts
zero_content = [s for s in d['subjects'] if s.get('content_count', 0) == 0]
if zero_content:
    issues.append(f'Subjects with 0 content: {len(zero_content)}')

if issues:
    print('ISSUES FOUND:')
    for issue in issues:
        print(f'  - {issue}')
else:
    print('No issues found! Data quality is good.')

