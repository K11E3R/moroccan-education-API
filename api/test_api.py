#!/usr/bin/env python3
"""
API Tests for Moroccan Education API
Run with: python test_api.py
"""

import json
import sys
from pathlib import Path

def test_data_file():
    """Test that data.json exists and is valid"""
    data_path = Path(__file__).parent / "data.json"
    
    assert data_path.exists(), f"Data file not found: {data_path}"
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check required top-level fields
    required_fields = ['source', 'levels', 'subjects', 'content', 'statistics', 'metadata']
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
    
    # Check source
    assert data['source'] == 'public_website', f"Invalid source: {data['source']}"
    
    # Check counts
    assert len(data['levels']) > 0, "No levels found"
    assert len(data['subjects']) > 0, "No subjects found"
    assert len(data['content']) > 0, "No content found"
    
    print(f"[OK] Data file valid")
    print(f"     Levels: {len(data['levels'])}")
    print(f"     Subjects: {len(data['subjects'])}")
    print(f"     Content: {len(data['content'])}")
    
    return data


def test_levels(data):
    """Test levels data structure"""
    required_fields = ['id', 'name', 'name_ar', 'order', 'category']
    
    for level in data['levels']:
        for field in required_fields:
            assert field in level, f"Level missing field: {field}"
        assert level['category'] in ['primaire', 'college', 'lycee'], f"Invalid category: {level['category']}"
    
    print(f"[OK] Levels structure valid ({len(data['levels'])} levels)")


def test_subjects(data):
    """Test subjects data structure"""
    required_fields = ['id', 'name', 'name_ar', 'level_id']
    level_ids = {l['id'] for l in data['levels']}
    
    for subject in data['subjects']:
        for field in required_fields:
            assert field in subject, f"Subject missing field: {field}"
        assert subject['level_id'] in level_ids, f"Invalid level_id: {subject['level_id']}"
    
    print(f"[OK] Subjects structure valid ({len(data['subjects'])} subjects)")


def test_content(data):
    """Test content data structure"""
    required_fields = ['id', 'title', 'level_id', 'subject_id', 'content_type']
    valid_types = {'cours', 'exercice', 'resume', 'controle', 'examen', 'correction'}
    
    for item in data['content']:
        for field in required_fields:
            assert field in item, f"Content missing field: {field}"
        assert item['content_type'] in valid_types, f"Invalid content_type: {item['content_type']}"
    
    # Check content type distribution
    type_counts = {}
    for item in data['content']:
        t = item['content_type']
        type_counts[t] = type_counts.get(t, 0) + 1
    
    print(f"[OK] Content structure valid ({len(data['content'])} items)")
    print(f"     Types: {type_counts}")


def test_statistics(data):
    """Test statistics match actual data"""
    stats = data['statistics']
    
    assert stats['total_levels'] == len(data['levels']), "Levels count mismatch"
    assert stats['total_subjects'] == len(data['subjects']), "Subjects count mismatch"
    assert stats['total_content'] == len(data['content']), "Content count mismatch"
    
    print(f"[OK] Statistics verified")


def test_metadata(data):
    """Test metadata structure"""
    metadata = data['metadata']
    
    assert 'languages' in metadata, "Missing languages"
    assert 'quality_score' in metadata, "Missing quality_score"
    assert 0 <= metadata['quality_score'] <= 1, f"Invalid quality_score: {metadata['quality_score']}"
    
    print(f"[OK] Metadata valid (quality_score: {metadata['quality_score']:.4f})")


def test_arabic_coverage(data):
    """Test Arabic translation coverage"""
    content_with_ar = sum(1 for c in data['content'] if c.get('title_ar'))
    coverage = content_with_ar / len(data['content']) if data['content'] else 0
    
    assert coverage > 0.9, f"Arabic coverage too low: {coverage:.2%}"
    print(f"[OK] Arabic coverage: {coverage:.2%}")


def main():
    """Run all tests"""
    print("=" * 60)
    print("MOROCCAN EDUCATION API - TEST SUITE")
    print("=" * 60)
    print()
    
    try:
        # Run tests
        data = test_data_file()
        test_levels(data)
        test_subjects(data)
        test_content(data)
        test_statistics(data)
        test_metadata(data)
        test_arabic_coverage(data)
        
        print()
        print("=" * 60)
        print("[OK] ALL TESTS PASSED!")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

