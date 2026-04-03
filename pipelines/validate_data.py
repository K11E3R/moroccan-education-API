#!/usr/bin/env python3
"""
Data Quality Validation Pipeline
Runs comprehensive checks on the education dataset and produces a quality report.
Designed to run standalone (CLI) or as part of CI/CD.

Exit codes:
  0 = all checks passed
  1 = critical failures found
  2 = warnings only (non-critical)
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple


REQUIRED_TOP_LEVEL = ["source", "levels", "subjects", "content", "statistics", "metadata"]
REQUIRED_LEVEL_FIELDS = ["id", "name", "name_ar", "order", "category"]
REQUIRED_SUBJECT_FIELDS = ["id", "name", "name_ar", "level_id"]
REQUIRED_CONTENT_FIELDS = ["id", "title", "level_id", "subject_id", "content_type"]
VALID_CATEGORIES = {"primaire", "college", "lycee"}
VALID_CONTENT_TYPES = {"cours", "exercice", "examen", "controle", "correction", "resume"}


class ValidationResult:
    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.warnings = 0
        self.issues: List[Dict[str, Any]] = []
        self.metrics: Dict[str, Any] = {}

    def pass_check(self, name: str):
        self.checks_passed += 1
        print(f"  [PASS] {name}")

    def fail_check(self, name: str, detail: str):
        self.checks_failed += 1
        self.issues.append({"severity": "error", "check": name, "detail": detail})
        print(f"  [FAIL] {name}: {detail}")

    def warn(self, name: str, detail: str):
        self.warnings += 1
        self.issues.append({"severity": "warning", "check": name, "detail": detail})
        print(f"  [WARN] {name}: {detail}")

    @property
    def total_checks(self) -> int:
        return self.checks_passed + self.checks_failed

    @property
    def score(self) -> float:
        if self.total_checks == 0:
            return 0.0
        return self.checks_passed / self.total_checks

    def to_report(self) -> Dict[str, Any]:
        return {
            "overall_score": round(self.score, 4),
            "checks_passed": self.checks_passed,
            "checks_failed": self.checks_failed,
            "warnings": self.warnings,
            "total_checks": self.total_checks,
            "issues": self.issues,
            "timestamp": datetime.now().isoformat(),
            "metrics": self.metrics,
        }


def validate_structure(data: Dict, result: ValidationResult):
    """Check top-level JSON structure"""
    print("\n--- Structure Checks ---")
    for field in REQUIRED_TOP_LEVEL:
        if field in data:
            result.pass_check(f"Top-level field '{field}' exists")
        else:
            result.fail_check(f"Top-level field '{field}'", "Missing required field")

    if data.get("source") == "public_website":
        result.pass_check("Source field value")
    else:
        result.warn("Source field", f"Expected 'public_website', got '{data.get('source')}'")


def validate_levels(data: Dict, result: ValidationResult):
    """Validate levels data"""
    print("\n--- Level Checks ---")
    levels = data.get("levels", [])

    if len(levels) >= 12:
        result.pass_check(f"Level count ({len(levels)} >= 12)")
    else:
        result.fail_check("Level count", f"Expected >= 12, got {len(levels)}")

    ids = set()
    for level in levels:
        for field in REQUIRED_LEVEL_FIELDS:
            if field not in level:
                result.fail_check(f"Level field '{field}'", f"Missing in level {level.get('id', '?')}")
                return

        cat = level.get("category")
        if cat not in VALID_CATEGORIES:
            result.fail_check("Level category", f"Invalid category '{cat}' in {level['id']}")
        else:
            result.pass_check(f"Level '{level['id']}' structure")

        if level["id"] in ids:
            result.fail_check("Level ID uniqueness", f"Duplicate: {level['id']}")
        ids.add(level["id"])

    categories_found = {l.get("category") for l in levels}
    if categories_found == VALID_CATEGORIES:
        result.pass_check("All categories present (primaire/college/lycee)")
    else:
        result.fail_check("Category coverage", f"Missing: {VALID_CATEGORIES - categories_found}")


def validate_subjects(data: Dict, result: ValidationResult):
    """Validate subjects data"""
    print("\n--- Subject Checks ---")
    subjects = data.get("subjects", [])
    level_ids = {l["id"] for l in data.get("levels", [])}

    if len(subjects) >= 50:
        result.pass_check(f"Subject count ({len(subjects)} >= 50)")
    else:
        result.warn("Subject count", f"Expected >= 50, got {len(subjects)}")

    orphaned = 0
    for subject in subjects:
        for field in REQUIRED_SUBJECT_FIELDS:
            if field not in subject:
                result.fail_check("Subject field", f"Missing '{field}' in {subject.get('id', '?')}")
                return

        if subject["level_id"] not in level_ids:
            orphaned += 1

    if orphaned == 0:
        result.pass_check("All subjects reference valid levels")
    else:
        result.fail_check("Subject-level integrity", f"{orphaned} subjects reference invalid levels")

    ids = [s["id"] for s in subjects]
    dupes = len(ids) - len(set(ids))
    if dupes == 0:
        result.pass_check("Subject ID uniqueness")
    else:
        result.fail_check("Subject ID uniqueness", f"{dupes} duplicate IDs")


def validate_content(data: Dict, result: ValidationResult):
    """Validate content data"""
    print("\n--- Content Checks ---")
    content = data.get("content", [])
    subject_ids = {s["id"] for s in data.get("subjects", [])}
    level_ids = {l["id"] for l in data.get("levels", [])}

    if len(content) >= 500:
        result.pass_check(f"Content count ({len(content)} >= 500)")
    else:
        result.warn("Content count", f"Expected >= 500, got {len(content)}")

    invalid_types = 0
    missing_fields = 0
    orphaned_subjects = 0
    orphaned_levels = 0

    for item in content:
        for field in REQUIRED_CONTENT_FIELDS:
            if field not in item:
                missing_fields += 1
                break

        if item.get("content_type") not in VALID_CONTENT_TYPES:
            invalid_types += 1
        if item.get("subject_id") not in subject_ids:
            orphaned_subjects += 1
        if item.get("level_id") not in level_ids:
            orphaned_levels += 1

    if missing_fields == 0:
        result.pass_check("Content required fields")
    else:
        result.fail_check("Content required fields", f"{missing_fields} items missing required fields")

    if invalid_types == 0:
        result.pass_check("Content type validity")
    else:
        result.fail_check("Content type validity", f"{invalid_types} items have invalid content_type")

    if orphaned_subjects == 0:
        result.pass_check("Content-subject integrity")
    else:
        result.fail_check("Content-subject integrity", f"{orphaned_subjects} items reference invalid subjects")

    if orphaned_levels == 0:
        result.pass_check("Content-level integrity")
    else:
        result.fail_check("Content-level integrity", f"{orphaned_levels} items reference invalid levels")

    ids = [c["id"] for c in content]
    dupes = len(ids) - len(set(ids))
    if dupes == 0:
        result.pass_check("Content ID uniqueness")
    else:
        result.fail_check("Content ID uniqueness", f"{dupes} duplicate IDs")

    types_found = {c.get("content_type") for c in content}
    if types_found == VALID_CONTENT_TYPES:
        result.pass_check("All content types present")
    else:
        missing = VALID_CONTENT_TYPES - types_found
        result.warn("Content type coverage", f"Missing types: {missing}")


def validate_bilingual(data: Dict, result: ValidationResult):
    """Check Arabic translation coverage"""
    print("\n--- Bilingual Checks ---")
    content = data.get("content", [])

    ar_titles = sum(1 for c in content if c.get("title_ar"))
    ar_coverage = ar_titles / len(content) if content else 0
    result.metrics["arabic_coverage"] = round(ar_coverage, 4)

    if ar_coverage >= 0.9:
        result.pass_check(f"Arabic title coverage ({ar_coverage:.1%})")
    elif ar_coverage >= 0.7:
        result.warn("Arabic title coverage", f"Only {ar_coverage:.1%} (target: 90%+)")
    else:
        result.fail_check("Arabic title coverage", f"Only {ar_coverage:.1%} (target: 90%+)")

    subjects = data.get("subjects", [])
    ar_subjects = sum(1 for s in subjects if s.get("name_ar"))
    s_coverage = ar_subjects / len(subjects) if subjects else 0
    if s_coverage >= 0.95:
        result.pass_check(f"Subject Arabic coverage ({s_coverage:.1%})")
    else:
        result.warn("Subject Arabic coverage", f"Only {s_coverage:.1%}")


def validate_statistics(data: Dict, result: ValidationResult):
    """Verify statistics match actual data"""
    print("\n--- Statistics Checks ---")
    stats = data.get("statistics", {})

    if stats.get("total_levels") == len(data.get("levels", [])):
        result.pass_check("Levels count in statistics")
    else:
        result.fail_check("Levels count", "statistics.total_levels doesn't match actual count")

    if stats.get("total_subjects") == len(data.get("subjects", [])):
        result.pass_check("Subjects count in statistics")
    else:
        result.fail_check("Subjects count", "statistics.total_subjects doesn't match actual count")

    if stats.get("total_content") == len(data.get("content", [])):
        result.pass_check("Content count in statistics")
    else:
        result.fail_check("Content count", "statistics.total_content doesn't match actual count")


def validate_quality_score(data: Dict, result: ValidationResult):
    """Check quality score in metadata"""
    print("\n--- Quality Metadata ---")
    metadata = data.get("metadata", {})

    if "quality_score" in metadata:
        score = metadata["quality_score"]
        if 0 <= score <= 1:
            result.pass_check(f"Quality score valid ({score:.4f})")
        else:
            result.fail_check("Quality score range", f"Score {score} out of [0, 1] range")
    else:
        result.warn("Quality score", "Missing metadata.quality_score")

    if "languages" in metadata:
        result.pass_check("Languages metadata present")
    else:
        result.warn("Languages metadata", "Missing")


def run_validation(data_path: str) -> Tuple[ValidationResult, Dict]:
    """Run all validation checks and return results"""
    path = Path(data_path)
    if not path.exists():
        print(f"[ERROR] Data file not found: {path}")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("=" * 60)
    print("DATA QUALITY VALIDATION PIPELINE")
    print(f"File: {path}")
    print(f"Size: {path.stat().st_size / 1024:.1f} KB")
    print("=" * 60)

    result = ValidationResult()

    validate_structure(data, result)
    validate_levels(data, result)
    validate_subjects(data, result)
    validate_content(data, result)
    validate_bilingual(data, result)
    validate_statistics(data, result)
    validate_quality_score(data, result)

    result.metrics.update({
        "total_levels": len(data.get("levels", [])),
        "total_subjects": len(data.get("subjects", [])),
        "total_content": len(data.get("content", [])),
        "file_size_kb": round(path.stat().st_size / 1024, 1),
    })

    print("\n" + "=" * 60)
    print(f"RESULTS: {result.checks_passed}/{result.total_checks} checks passed")
    print(f"  Passed: {result.checks_passed} | Failed: {result.checks_failed} | Warnings: {result.warnings}")
    print(f"  Quality Score: {result.score:.1%}")
    print("=" * 60)

    return result, result.to_report()


def main():
    data_path = sys.argv[1] if len(sys.argv) > 1 else "api/data.json"
    result, report = run_validation(data_path)

    report_path = Path("pipelines/quality_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\nReport saved: {report_path}")

    if result.checks_failed > 0:
        sys.exit(1)
    elif result.warnings > 0:
        sys.exit(0)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
