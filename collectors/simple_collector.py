"""
Simple but effective collector - Just get the data!
"""

import asyncio
import aiohttp
import json
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from typing import List, Dict
import re


class SimpleCollector:
    """Simple collector that actually works"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = None
        self.data = {
            'levels': [],
            'subjects': [],
            'content': []
        }
    
    async def _fetch(self, url: str) -> str:
        """Fetch URL"""
        try:
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as response:
                if response.status == 200:
                    return await response.text()
        except:
            pass
        return None
    
    async def discover_urls(self) -> List[str]:
        """Get all URLs from sitemap"""
        print("Discovering URLs from sitemap...")
        
        sitemap_url = f"{self.base_url}/sitemap.xml"
        content = await self._fetch(sitemap_url)
        
        if not content:
            return []
        
        soup = BeautifulSoup(content, 'xml')
        sitemap_locs = soup.find_all('loc')
        
        all_urls = []
        for loc in sitemap_locs:
            url = loc.text.strip()
            if 'sitemap' in url:
                # Fetch sub-sitemap
                sub_content = await self._fetch(url)
                if sub_content:
                    sub_soup = BeautifulSoup(sub_content, 'xml')
                    sub_locs = sub_soup.find_all('loc')
                    all_urls.extend([l.text.strip() for l in sub_locs])
            else:
                all_urls.append(url)
        
        print(f"Found {len(all_urls)} URLs")
        return all_urls
    
    def detect_level(self, url: str) -> Dict:
        """Detect level from URL"""
        url_lower = url.lower()
        
        # Primaire
        if '1ere-annee-primaire' in url_lower or 'primaire-1' in url_lower:
            return {'id': 'primaire-1', 'name': '1ère Année Primaire', 'name_ar': 'السنة الأولى ابتدائي', 'order': 1}
        elif '2eme-annee-primaire' in url_lower or 'primaire-2' in url_lower:
            return {'id': 'primaire-2', 'name': '2ème Année Primaire', 'name_ar': 'السنة الثانية ابتدائي', 'order': 2}
        elif '3eme-annee-primaire' in url_lower or 'primaire-3' in url_lower:
            return {'id': 'primaire-3', 'name': '3ème Année Primaire', 'name_ar': 'السنة الثالثة ابتدائي', 'order': 3}
        elif '4eme-annee-primaire' in url_lower or 'primaire-4' in url_lower:
            return {'id': 'primaire-4', 'name': '4ème Année Primaire', 'name_ar': 'السنة الرابعة ابتدائي', 'order': 4}
        elif '5eme-annee-primaire' in url_lower or 'primaire-5' in url_lower:
            return {'id': 'primaire-5', 'name': '5ème Année Primaire', 'name_ar': 'السنة الخامسة ابتدائي', 'order': 5}
        elif '6eme-annee-primaire' in url_lower or 'primaire-6' in url_lower:
            return {'id': 'primaire-6', 'name': '6ème Année Primaire', 'name_ar': 'السنة السادسة ابتدائي', 'order': 6}
        
        # Collège
        elif '1ere-annee-college' in url_lower or 'college-1' in url_lower:
            return {'id': 'college-1', 'name': '1ère Année Collège', 'name_ar': 'السنة الأولى إعدادي', 'order': 7}
        elif '2eme-annee-college' in url_lower or 'college-2' in url_lower:
            return {'id': 'college-2', 'name': '2ème Année Collège', 'name_ar': 'السنة الثانية إعدادي', 'order': 8}
        elif '3eme-annee-college' in url_lower or 'college-3' in url_lower:
            return {'id': 'college-3', 'name': '3ème Année Collège', 'name_ar': 'السنة الثالثة إعدادي', 'order': 9}
        
        # Lycée
        elif 'tronc-commun' in url_lower:
            return {'id': 'lycee-tc', 'name': 'Tronc Commun', 'name_ar': 'الجذع المشترك', 'order': 10}
        elif '1ere-bac' in url_lower or 'premiere-bac' in url_lower:
            return {'id': 'lycee-1bac', 'name': '1ère Bac', 'name_ar': 'الأولى باكالوريا', 'order': 11}
        elif '2eme-bac' in url_lower or 'deuxieme-bac' in url_lower:
            return {'id': 'lycee-2bac', 'name': '2ème Bac', 'name_ar': 'الثانية باكالوريا', 'order': 12}
        
        return None
    
    async def process_url(self, url: str):
        """Process single URL"""
        # Detect level
        level_info = self.detect_level(url)
        if not level_info:
            return
        
        # Fetch page
        html = await self._fetch(url)
        if not html:
            return
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Get title
        title_tag = soup.find('h1')
        if not title_tag:
            return
        
        title = title_tag.get_text(strip=True)
        
        # Determine if it's a subject or content
        if '/category/' in url:
            # It's a level or subject
            self.data['subjects'].append({
                'id': f"{title.lower().replace(' ', '-')}-{level_info['id']}",
                'name': title,
                'name_ar': '',
                'level_id': level_info['id'],
                'level_name': level_info['name'],
                'url': url
            })
        elif '/course/' in url:
            # It's content
            content_type = 'cours'  # Default
            if 'exercice' in url.lower():
                content_type = 'exercice'
            elif 'examen' in url.lower():
                content_type = 'examen'
            elif 'controle' in url.lower():
                content_type = 'controle'
            
            self.data['content'].append({
                'id': f"{content_type}-{url.split('/')[-1]}",
                'title': title,
                'title_ar': '',
                'level_id': level_info['id'],
                'content_type': content_type,
                'url': url
            })
    
    async def collect(self, max_urls: int = 1000):
        """Collect data"""
        print("="*70)
        print("SIMPLE COLLECTOR - GETTING REAL DATA")
        print("="*70)
        print()
        
        # Create session
        connector = aiohttp.TCPConnector(limit=30)
        self.session = aiohttp.ClientSession(connector=connector)
        
        try:
            # Get URLs
            all_urls = await self.discover_urls()
            
            # Filter to relevant URLs
            relevant_urls = [
                url for url in all_urls
                if '/course/' in url or '/category/' in url
            ][:max_urls]
            
            print(f"Processing {len(relevant_urls)} URLs...")
            print()
            
            # Process in batches
            batch_size = 50
            for i in range(0, len(relevant_urls), batch_size):
                batch = relevant_urls[i:i+batch_size]
                tasks = [self.process_url(url) for url in batch]
                await asyncio.gather(*tasks)
                print(f"Processed {min(i+batch_size, len(relevant_urls))}/{len(relevant_urls)} URLs")
            
            # Extract unique levels
            level_ids = set()
            for subject in self.data['subjects']:
                level_ids.add(subject['level_id'])
            for content in self.data['content']:
                level_ids.add(content['level_id'])
            
            # Create level entries
            level_map = {
                'primaire-1': {'id': 'primaire-1', 'name': '1ère Année Primaire', 'name_ar': 'السنة الأولى ابتدائي', 'order': 1, 'category': 'primaire'},
                'primaire-2': {'id': 'primaire-2', 'name': '2ème Année Primaire', 'name_ar': 'السنة الثانية ابتدائي', 'order': 2, 'category': 'primaire'},
                'primaire-3': {'id': 'primaire-3', 'name': '3ème Année Primaire', 'name_ar': 'السنة الثالثة ابتدائي', 'order': 3, 'category': 'primaire'},
                'primaire-4': {'id': 'primaire-4', 'name': '4ème Année Primaire', 'name_ar': 'السنة الرابعة ابتدائي', 'order': 4, 'category': 'primaire'},
                'primaire-5': {'id': 'primaire-5', 'name': '5ème Année Primaire', 'name_ar': 'السنة الخامسة ابتدائي', 'order': 5, 'category': 'primaire'},
                'primaire-6': {'id': 'primaire-6', 'name': '6ème Année Primaire', 'name_ar': 'السنة السادسة ابتدائي', 'order': 6, 'category': 'primaire'},
                'college-1': {'id': 'college-1', 'name': '1ère Année Collège', 'name_ar': 'السنة الأولى إعدادي', 'order': 7, 'category': 'college'},
                'college-2': {'id': 'college-2', 'name': '2ème Année Collège', 'name_ar': 'السنة الثانية إعدادي', 'order': 8, 'category': 'college'},
                'college-3': {'id': 'college-3', 'name': '3ème Année Collège', 'name_ar': 'السنة الثالثة إعدادي', 'order': 9, 'category': 'college'},
                'lycee-tc': {'id': 'lycee-tc', 'name': 'Tronc Commun', 'name_ar': 'الجذع المشترك', 'order': 10, 'category': 'lycee'},
                'lycee-1bac': {'id': 'lycee-1bac', 'name': '1ère Bac', 'name_ar': 'الأولى باكالوريا', 'order': 11, 'category': 'lycee'},
                'lycee-2bac': {'id': 'lycee-2bac', 'name': '2ème Bac', 'name_ar': 'الثانية باكالوريا', 'order': 12, 'category': 'lycee'},
            }
            
            self.data['levels'] = [level_map[lid] for lid in level_ids if lid in level_map]
            self.data['levels'].sort(key=lambda x: x['order'])
            
            print()
            print("="*70)
            print("COLLECTION COMPLETE")
            print("="*70)
            print(f"Levels: {len(self.data['levels'])}")
            print(f"Subjects: {len(self.data['subjects'])}")
            print(f"Content: {len(self.data['content'])}")
            print("="*70)
            
        finally:
            await self.session.close()
    
    def save(self, output_dir: Path):
        """Save data"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = output_dir / f"simple_collected_{timestamp}.json"
        
        output = {
            'collection_date': datetime.now().isoformat(),
            'base_url': self.base_url,
            'statistics': {
                'total_levels': len(self.data['levels']),
                'total_subjects': len(self.data['subjects']),
                'total_content': len(self.data['content'])
            },
            'levels': self.data['levels'],
            'subjects': self.data['subjects'],
            'content': self.data['content']
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"\nSaved to: {filename}")
        return filename


async def main():
    collector = SimpleCollector("https://www.alloschool.com")
    await collector.collect(max_urls=2000)  # Collect 2000 URLs
    collector.save(Path("data/raw"))


if __name__ == "__main__":
    asyncio.run(main())

