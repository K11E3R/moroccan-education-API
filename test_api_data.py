"""Test API data"""
import json

# Load data
with open('api/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("="*60)
print("API DATA CHECK")
print("="*60)
print(f"Levels: {len(data.get('levels', []))}")
print(f"Subjects: {len(data.get('subjects', []))}")
print(f"Content: {len(data.get('content', []))}")
print()

# Show sample
if data.get('levels'):
    print("Sample Level:")
    print(f"  {data['levels'][0]['name']} ({data['levels'][0]['name_ar']})")
print()

if data.get('content'):
    print("Sample Content:")
    print(f"  {data['content'][0]['title']}")
print()

print("="*60)
print("Data is ready for API!" if data.get('levels') else "ERROR: No data!")
print("="*60)

