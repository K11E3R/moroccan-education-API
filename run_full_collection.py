"""
Run full collection - Get ALL the data!
"""

import asyncio
from pathlib import Path
from collectors.simple_collector import SimpleCollector


async def main():
    print("="*70)
    print("FULL COLLECTION - GETTING ALL DATA")
    print("="*70)
    print()
    
    collector = SimpleCollector("https://www.alloschool.com")
    
    # Collect up to 10,000 URLs
    await collector.collect(max_urls=10000)
    
    # Save
    filename = collector.save(Path("data/raw"))
    
    print()
    print("="*70)
    print("COLLECTION COMPLETE!")
    print("="*70)
    print(f"File: {filename}")
    print()
    print("Next steps:")
    print("  1. Validate data quality")
    print("  2. Clean and deduplicate")
    print("  3. Update API")
    print("  4. Deploy to Railway")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())

