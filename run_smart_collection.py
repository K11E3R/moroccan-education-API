"""
Run smart collection with validation and cleaning
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
from collectors.smart_collector import SmartCollector
from collectors.data_schema import DataValidator, DataCleaner, DataOrganizer


async def main():
    """Main collection pipeline"""
    
    print("="*70)
    print("🇲🇦 SMART MOROCCAN EDUCATION DATA COLLECTION")
    print("="*70)
    print()
    
    # Step 1: Collect data
    print("📥 Step 1: Collecting data...")
    collector = SmartCollector(
        base_url="https://www.alloschool.com",
        max_concurrent=50
    )
    
    await collector.collect_all()
    
    # Save raw data
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    collector.save_data(raw_dir)
    
    # Load collected data
    files = sorted(raw_dir.glob("smart_collected_*.json"))
    if not files:
        print("❌ No data collected!")
        return
    
    latest_file = files[-1]
    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ Data collected: {latest_file.name}")
    print()
    
    # Step 2: Validate data
    print("✅ Step 2: Validating data...")
    validation_results = DataValidator.validate_dataset(data)
    
    print(f"  Levels: {validation_results['levels']['valid']} valid, "
          f"{validation_results['levels']['invalid']} invalid, "
          f"{validation_results['levels']['warnings']} warnings")
    print(f"  Subjects: {validation_results['subjects']['valid']} valid, "
          f"{validation_results['subjects']['invalid']} invalid, "
          f"{validation_results['subjects']['warnings']} warnings")
    print(f"  Content: {validation_results['content']['valid']} valid, "
          f"{validation_results['content']['invalid']} invalid, "
          f"{validation_results['content']['warnings']} warnings")
    print(f"  Overall Quality Score: {validation_results['overall_score']:.2f}/1.0")
    
    if validation_results['errors']:
        print(f"  ⚠️  {len(validation_results['errors'])} errors found")
        for error in validation_results['errors'][:5]:  # Show first 5
            print(f"     - {error}")
    
    print()
    
    # Step 3: Clean data
    print("🧹 Step 3: Cleaning data...")
    cleaned_data = DataCleaner.clean_dataset(data)
    
    original_counts = {
        'levels': len(data.get('levels', [])),
        'subjects': len(data.get('subjects', [])),
        'content': len(data.get('content', []))
    }
    
    cleaned_counts = {
        'levels': len(cleaned_data.get('levels', [])),
        'subjects': len(cleaned_data.get('subjects', [])),
        'content': len(cleaned_data.get('content', []))
    }
    
    print(f"  Levels: {original_counts['levels']} → {cleaned_counts['levels']} "
          f"({original_counts['levels'] - cleaned_counts['levels']} duplicates removed)")
    print(f"  Subjects: {original_counts['subjects']} → {cleaned_counts['subjects']} "
          f"({original_counts['subjects'] - cleaned_counts['subjects']} duplicates removed)")
    print(f"  Content: {original_counts['content']} → {cleaned_counts['content']} "
          f"({original_counts['content'] - cleaned_counts['content']} duplicates removed)")
    print()
    
    # Step 4: Organize data
    print("📊 Step 4: Organizing data...")
    organized = DataOrganizer.organize_by_level(cleaned_data)
    stats = DataOrganizer.generate_statistics(cleaned_data)
    
    print(f"  Organized into {len(organized)} levels")
    print(f"  Total items: {stats['total_levels'] + stats['total_subjects'] + stats['total_content']}")
    print()
    
    # Step 5: Save cleaned data
    print("💾 Step 5: Saving cleaned data...")
    cleaned_dir = Path("data/cleaned")
    cleaned_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cleaned_file = cleaned_dir / f"cleaned_data_{timestamp}.json"
    
    cleaned_data['statistics'] = stats
    cleaned_data['validation'] = {
        'quality_score': validation_results['overall_score'],
        'errors_count': len(validation_results['errors']),
        'warnings_count': len(validation_results['warnings'])
    }
    
    with open(cleaned_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
    
    print(f"  Saved to: {cleaned_file}")
    print()
    
    # Step 6: Quality report
    print("="*70)
    print("📊 FINAL QUALITY REPORT")
    print("="*70)
    print()
    print(f"Quality Score: {validation_results['overall_score']:.2f}/1.0")
    print()
    print("Data Summary:")
    print(f"  ✅ {cleaned_counts['levels']} unique levels")
    print(f"  ✅ {cleaned_counts['subjects']} unique subjects")
    print(f"  ✅ {cleaned_counts['content']} unique content items")
    print()
    print("By Category:")
    for category, count in stats['by_category'].items():
        print(f"  - {category}: {count} levels")
    print()
    print("By Content Type:")
    for content_type, count in stats['by_content_type'].items():
        print(f"  - {content_type}: {count} items")
    print()
    
    # Decision
    if validation_results['overall_score'] >= 0.95:
        print("✅ Data quality is EXCELLENT! Ready for production.")
        print()
        print("Next steps:")
        print("  1. Copy to public API: api/data.json")
        print("  2. Push to GitHub")
        print("  3. Deploy to Railway")
    elif validation_results['overall_score'] >= 0.85:
        print("⚠️  Data quality is GOOD but needs improvement.")
        print()
        print("Issues to fix:")
        for error in validation_results['errors'][:10]:
            print(f"  - {error}")
    else:
        print("❌ Data quality is LOW. More work needed.")
        print()
        print("Major issues:")
        for error in validation_results['errors'][:10]:
            print(f"  - {error}")
    
    print()
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())

