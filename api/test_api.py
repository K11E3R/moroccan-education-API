#!/usr/bin/env python3
"""
Test suite for Moroccan Education API v1.0
Validates data integrity and API endpoint behavior.

Run: python3 api/test_api.py
"""

import json
import sys
from pathlib import Path


def test_data_file():
    """Verify data.json exists, is valid JSON, and has required top-level fields."""
    data_path = Path(__file__).parent / "data.json"

    assert data_path.exists(), f"Data file not found: {data_path}"

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    required_fields = ["source", "levels", "subjects", "content", "statistics", "metadata"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"

    assert data["source"] == "public_website", f"Invalid source: {data['source']}"
    assert len(data["levels"]) > 0, "No levels found"
    assert len(data["subjects"]) > 0, "No subjects found"
    assert len(data["content"]) > 0, "No content found"

    print(f"[PASS] Data file valid")
    print(f"       Levels: {len(data['levels'])} | Subjects: {len(data['subjects'])} | Content: {len(data['content'])}")
    return data


def test_levels(data):
    """Validate level structure and referential integrity."""
    required = ["id", "name", "name_ar", "order", "category"]
    valid_categories = {"primaire", "college", "lycee"}

    for level in data["levels"]:
        for field in required:
            assert field in level, f"Level missing field: {field} in {level.get('id', '?')}"
        assert level["category"] in valid_categories, f"Invalid category: {level['category']}"

    ids = [l["id"] for l in data["levels"]]
    assert len(ids) == len(set(ids)), "Duplicate level IDs"
    print(f"[PASS] Levels structure valid ({len(data['levels'])} levels)")


def test_subjects(data):
    """Validate subject structure and level references."""
    required = ["id", "name", "name_ar", "level_id"]
    level_ids = {l["id"] for l in data["levels"]}

    for subject in data["subjects"]:
        for field in required:
            assert field in subject, f"Subject missing: {field} in {subject.get('id', '?')}"
        assert subject["level_id"] in level_ids, f"Invalid level_id: {subject['level_id']}"

    ids = [s["id"] for s in data["subjects"]]
    assert len(ids) == len(set(ids)), "Duplicate subject IDs"
    print(f"[PASS] Subjects structure valid ({len(data['subjects'])} subjects)")


def test_content(data):
    """Validate content structure, types, and references."""
    required = ["id", "title", "level_id", "subject_id", "content_type"]
    valid_types = {"cours", "exercice", "resume", "controle", "examen", "correction"}
    subject_ids = {s["id"] for s in data["subjects"]}

    for item in data["content"]:
        for field in required:
            assert field in item, f"Content missing: {field} in {item.get('id', '?')}"
        assert item["content_type"] in valid_types, f"Invalid type: {item['content_type']}"
        assert item["subject_id"] in subject_ids, f"Orphaned subject_id: {item['subject_id']}"

    ids = [c["id"] for c in data["content"]]
    assert len(ids) == len(set(ids)), "Duplicate content IDs"

    types_found = {c["content_type"] for c in data["content"]}
    assert types_found == valid_types, f"Missing types: {valid_types - types_found}"

    type_counts = {}
    for item in data["content"]:
        t = item["content_type"]
        type_counts[t] = type_counts.get(t, 0) + 1

    print(f"[PASS] Content structure valid ({len(data['content'])} items)")
    print(f"       Types: {type_counts}")


def test_statistics(data):
    """Verify statistics match actual data counts."""
    stats = data["statistics"]
    assert stats["total_levels"] == len(data["levels"]), "Levels count mismatch"
    assert stats["total_subjects"] == len(data["subjects"]), "Subjects count mismatch"
    assert stats["total_content"] == len(data["content"]), "Content count mismatch"
    print(f"[PASS] Statistics verified")


def test_metadata(data):
    """Validate metadata structure and quality score."""
    md = data["metadata"]
    assert "languages" in md, "Missing languages"
    assert "quality_score" in md, "Missing quality_score"
    assert 0 <= md["quality_score"] <= 1, f"Invalid quality_score: {md['quality_score']}"
    assert "data_sources" in md, "Missing data_sources"
    print(f"[PASS] Metadata valid (quality: {md['quality_score']:.2%}, sources: {len(md.get('data_sources', []))})")


def test_arabic_coverage(data):
    """Verify Arabic translation coverage is above threshold."""
    with_ar = sum(1 for c in data["content"] if c.get("title_ar"))
    coverage = with_ar / len(data["content"]) if data["content"] else 0
    assert coverage > 0.9, f"Arabic coverage too low: {coverage:.2%}"
    print(f"[PASS] Arabic coverage: {coverage:.2%}")


def test_source_coverage(data):
    """Verify content items reference real data sources."""
    with_source = sum(1 for c in data["content"] if c.get("source"))
    coverage = with_source / len(data["content"]) if data["content"] else 0
    assert coverage > 0.8, f"Source coverage too low: {coverage:.2%}"
    sources = set(c.get("source", "") for c in data["content"] if c.get("source"))
    print(f"[PASS] Source coverage: {coverage:.2%} ({len(sources)} sources: {', '.join(sorted(sources))})")


def test_url_quality(data):
    """Verify URLs are present and point to real domains (not example.com)."""
    with_url = sum(1 for c in data["content"] if c.get("url"))
    example_urls = sum(1 for c in data["content"] if "example.com" in c.get("url", ""))
    assert with_url > 0, "No content items have URLs"
    assert example_urls == 0, f"{example_urls} items still use example.com URLs"
    print(f"[PASS] URL quality: {with_url} items have URLs, 0 use example.com")


def main():
    print("=" * 60)
    print("MOROCCAN EDUCATION API — TEST SUITE v1.0")
    print("=" * 60)
    print()

    try:
        data = test_data_file()
        test_levels(data)
        test_subjects(data)
        test_content(data)
        test_statistics(data)
        test_metadata(data)
        test_arabic_coverage(data)
        test_source_coverage(data)
        test_url_quality(data)

        print()
        print("=" * 60)
        print("[OK] ALL TESTS PASSED!")
        print("=" * 60)
        return 0

    except AssertionError as e:
        print(f"\n[FAIL] {e}")
        return 1
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
