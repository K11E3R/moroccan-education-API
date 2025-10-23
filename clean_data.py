#!/usr/bin/env python3
"""
Clean data - Remove all source references to make it 100% public
"""
import json
import re

# Load data
with open('data/fast_collected_data_20251022_233523.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Cleaning data - removing all source references...")
print("")

changes = 0

# Clean levels
for level in data.get('levels', []):
    # Remove URL
    if 'url' in level:
        del level['url']
        changes += 1
    
    # Clean description - remove website names
    if 'description' in level:
        original = level['description']
        # Remove "AlloSchool", "Votre école sur internet", URLs, etc.
        cleaned = re.sub(r'AlloSchool', '', level['description'], flags=re.IGNORECASE)
        cleaned = re.sub(r'Votre école sur internet', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'https?://[^\s]+', '', cleaned)
        cleaned = re.sub(r',\s*Cours,', ', Cours,', cleaned)
        cleaned = re.sub(r'\s+-\s+', ' - ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        cleaned = re.sub(r'\s*-\s*$', '', cleaned)
        cleaned = re.sub(r'^\s*-\s*', '', cleaned)
        cleaned = re.sub(r'\.\s*\.\s*$', '.', cleaned)
        if cleaned != original:
            level['description'] = cleaned if cleaned else "Cours et ressources pédagogiques"
            changes += 1

# Clean subjects
for subject in data.get('subjects', []):
    # Remove URL
    if 'url' in subject:
        del subject['url']
        changes += 1
    
    # Clean description
    if 'description' in subject:
        original = subject['description']
        cleaned = re.sub(r'AlloSchool', '', subject['description'], flags=re.IGNORECASE)
        cleaned = re.sub(r'Votre école sur internet', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'https?://[^\s]+', '', cleaned)
        cleaned = re.sub(r',\s*Cours,', ', Cours,', cleaned)
        cleaned = re.sub(r'\s+-\s+', ' - ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        cleaned = re.sub(r'\s*-\s*$', '', cleaned)
        cleaned = re.sub(r'^\s*-\s*', '', cleaned)
        cleaned = re.sub(r'\.\s*\.\s*$', '.', cleaned)
        if cleaned != original:
            subject['description'] = cleaned if cleaned else "Cours et ressources pédagogiques"
            changes += 1

# Save cleaned data
with open('data/fast_collected_data_20251022_233523.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Also save to api/data.json
with open('api/data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Cleaned {changes} references")
print("")
print("Removed:")
print("  - All URLs")
print("  - Website names (AlloSchool, etc.)")
print("  - Website slogans")
print("")
print("Data is now 100% source-free and public!")
print("")
print("Files updated:")
print("  - data/fast_collected_data_20251022_233523.json")
print("  - api/data.json")

