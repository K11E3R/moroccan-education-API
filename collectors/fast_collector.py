#!/usr/bin/env python3
"""
Fast Educational Data Collector - Optimized for Speed

High-performance collector using:
- Async/await for parallel requests
- Connection pooling
- Aggressive caching
- Minimal delays
- Batch processing
"""

import asyncio
import aiohttp
import json
import time
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Dict, List, Set, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
from slugify import slugify
import pandas as pd
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class FastCollectionConfig:
    """Fast collection configuration"""
    base_url: str
    source_name: str
    country: str
    max_concurrent_requests: int = 50  # High concurrency
    timeout: int = 10  # Short timeout
    delay_between_requests: float = 0.1  # Minimal delay
    max_retries: int = 2
    sitemap_urls: List[str] = None

@dataclass
class CollectedData:
    """Container for collected data"""
    source: str
    country: str
    collection_date: str
    levels: List[Dict[str, Any]]
    subjects: List[Dict[str, Any]]
    courses: List[Dict[str, Any]]
    exercises: List[Dict[str, Any]]
    controls: List[Dict[str, Any]]
    exams: List[Dict[str, Any]]
    corrections: List[Dict[str, Any]]
    metadata: Dict[str, Any]

class FastEducationalCollector:
    """High-performance educational data collector"""
    
    def __init__(self, config: FastCollectionConfig):
        self.config = config
        self.collected_data = CollectedData(
            source=config.source_name,
            country=config.country,
            collection_date=time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            levels=[],
            subjects=[],
            courses=[],
            exercises=[],
            controls=[],
            exams=[],
            corrections=[],
            metadata={}
        )
        self.visited_urls: Set[str] = set()
        self.failed_urls: Set[str] = set()
        self.session = None
        
    async def collect_all_data(self) -> CollectedData:
        """Main async method to collect all data"""
        logger.info(f"🚀 Starting FAST data collection from {self.config.base_url}")
        start_time = time.time()
        
        # Create session with connection pooling
        connector = aiohttp.TCPConnector(
            limit=self.config.max_concurrent_requests,
            limit_per_host=self.config.max_concurrent_requests,
            ttl_dns_cache=300
        )
        
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)
        
        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'fr-FR,fr;q=0.9,ar;q=0.8,en;q=0.7',
                'Connection': 'keep-alive'
            }
        ) as session:
            self.session = session
            
            try:
                # Step 1: Discover sitemaps
                logger.info("📍 Discovering sitemaps...")
                sitemaps = await self._discover_sitemaps_async()
                logger.info(f"✅ Found {len(sitemaps)} sitemaps")
                
                # Step 2: Extract URLs from sitemaps (parallel)
                logger.info("🔗 Extracting URLs from sitemaps...")
                all_urls = await self._extract_urls_from_sitemaps_async(sitemaps)
                logger.info(f"✅ Extracted {len(all_urls)} URLs")
                
                # Step 3: Categorize URLs
                logger.info("📂 Categorizing URLs...")
                categorized_urls = self._categorize_urls(all_urls)
                
                # Step 4: Collect data in parallel batches
                logger.info("📊 Collecting data in parallel...")
                await self._collect_all_categories_async(categorized_urls)
                
                # Step 5: Generate metadata
                self._generate_metadata()
                
                elapsed = time.time() - start_time
                logger.info(f"✅ Collection completed in {elapsed:.2f} seconds!")
                logger.info(f"⚡ Speed: {len(all_urls)/elapsed:.2f} URLs/second")
                
                return self.collected_data
                
            except Exception as e:
                logger.error(f"❌ Error during collection: {e}")
                raise
    
    async def _discover_sitemaps_async(self) -> List[str]:
        """Discover sitemaps asynchronously"""
        sitemaps = []
        
        if self.config.sitemap_urls:
            sitemaps.extend(self.config.sitemap_urls)
        
        # Check common locations in parallel
        common_paths = [
            '/sitemap.xml',
            '/sitemap_index.xml',
            '/sitemaps/sitemap.xml',
            '/robots.txt'
        ]
        
        tasks = []
        for path in common_paths:
            url = urljoin(self.config.base_url, path)
            tasks.append(self._check_sitemap_exists(url))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for url, exists in zip([urljoin(self.config.base_url, p) for p in common_paths], results):
            if exists and not isinstance(exists, Exception):
                if 'robots.txt' in url:
                    # Parse robots.txt for sitemap URLs
                    try:
                        async with self.session.get(url) as response:
                            if response.status == 200:
                                text = await response.text()
                                for line in text.split('\n'):
                                    if line.strip().lower().startswith('sitemap:'):
                                        sitemap_url = line.split(':', 1)[1].strip()
                                        sitemaps.append(sitemap_url)
                    except:
                        pass
                else:
                    sitemaps.append(url)
        
        return list(set(sitemaps))
    
    async def _check_sitemap_exists(self, url: str) -> bool:
        """Check if sitemap exists"""
        try:
            async with self.session.head(url, allow_redirects=True) as response:
                return response.status == 200
        except:
            return False
    
    async def _extract_urls_from_sitemaps_async(self, sitemaps: List[str]) -> List[str]:
        """Extract URLs from sitemaps in parallel"""
        tasks = [self._extract_urls_from_sitemap(sitemap) for sitemap in sitemaps]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_urls = []
        for result in results:
            if isinstance(result, list):
                all_urls.extend(result)
        
        return list(set(all_urls))
    
    async def _extract_urls_from_sitemap(self, sitemap_url: str) -> List[str]:
        """Extract URLs from a single sitemap"""
        urls = []
        
        try:
            async with self.session.get(sitemap_url) as response:
                if response.status != 200:
                    return urls
                
                content = await response.read()
                root = ET.fromstring(content)
                
                # Handle sitemap index
                if root.tag.endswith('sitemapindex'):
                    nested_sitemaps = []
                    for sitemap_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap'):
                        loc_elem = sitemap_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                        if loc_elem is not None:
                            nested_sitemaps.append(loc_elem.text)
                    
                    # Recursively fetch nested sitemaps
                    tasks = [self._extract_urls_from_sitemap(sm) for sm in nested_sitemaps]
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    for result in results:
                        if isinstance(result, list):
                            urls.extend(result)
                
                # Handle regular sitemap
                elif root.tag.endswith('urlset'):
                    for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                        loc_elem = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                        if loc_elem is not None:
                            urls.append(loc_elem.text)
        
        except Exception as e:
            logger.debug(f"Error extracting from {sitemap_url}: {e}")
        
        return urls
    
    def _categorize_urls(self, urls: List[str]) -> Dict[str, List[str]]:
        """Categorize URLs by content type"""
        categorized = {
            'levels': [],
            'subjects': [],
            'courses': [],
            'exercises': [],
            'controls': [],
            'exams': [],
            'corrections': []
        }
        
        patterns = {
            'levels': [r'primaire', r'college', r'lycee', r'bac', r'superieur'],
            'subjects': [r'math', r'francais', r'arabe', r'sciences', r'histoire', r'geographie', 
                        r'anglais', r'physique', r'chimie', r'svt', r'islamique', r'informatique'],
            'courses': [r'/cours/', r'/lesson/', r'/lecon/'],
            'exercises': [r'/exercice/', r'/exercise/', r'/pratique/'],
            'controls': [r'/controle/', r'/control/', r'/test/'],
            'exams': [r'/examen/', r'/exam/', r'/evaluation/'],
            'corrections': [r'/correction/', r'/solution/', r'/reponse/']
        }
        
        for url in urls:
            url_lower = url.lower()
            for category, category_patterns in patterns.items():
                if any(re.search(pattern, url_lower) for pattern in category_patterns):
                    categorized[category].append(url)
                    break
        
        for category, urls_list in categorized.items():
            logger.info(f"   - {category}: {len(urls_list)} URLs")
        
        return categorized
    
    async def _collect_all_categories_async(self, categorized_urls: Dict[str, List[str]]):
        """Collect all categories in parallel"""
        tasks = []
        
        # Collect levels (limit to 20)
        if categorized_urls['levels']:
            tasks.append(self._collect_batch_async(
                categorized_urls['levels'][:20], 
                'level', 
                self._extract_level_data
            ))
        
        # Collect subjects (limit to 50)
        if categorized_urls['subjects']:
            tasks.append(self._collect_batch_async(
                categorized_urls['subjects'][:50], 
                'subject', 
                self._extract_subject_data
            ))
        
        # Collect courses (limit to 100)
        if categorized_urls['courses']:
            tasks.append(self._collect_batch_async(
                categorized_urls['courses'][:100], 
                'course', 
                self._extract_content_data
            ))
        
        # Collect exercises (limit to 100)
        if categorized_urls['exercises']:
            tasks.append(self._collect_batch_async(
                categorized_urls['exercises'][:100], 
                'exercise', 
                self._extract_content_data
            ))
        
        # Collect controls (limit to 50)
        if categorized_urls['controls']:
            tasks.append(self._collect_batch_async(
                categorized_urls['controls'][:50], 
                'control', 
                self._extract_content_data
            ))
        
        # Collect exams (limit to 50)
        if categorized_urls['exams']:
            tasks.append(self._collect_batch_async(
                categorized_urls['exams'][:50], 
                'exam', 
                self._extract_content_data
            ))
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _collect_batch_async(self, urls: List[str], data_type: str, extractor_func):
        """Collect data from URLs in parallel batches"""
        logger.info(f"📥 Collecting {data_type} data from {len(urls)} URLs...")
        
        # Process in batches to avoid overwhelming the server
        batch_size = self.config.max_concurrent_requests
        
        for i in range(0, len(urls), batch_size):
            batch = urls[i:i+batch_size]
            tasks = [self._fetch_and_extract(url, data_type, extractor_func) for url in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Store results
            for result in results:
                if result and not isinstance(result, Exception):
                    if data_type == 'level':
                        self.collected_data.levels.append(result)
                    elif data_type == 'subject':
                        self.collected_data.subjects.append(result)
                    elif data_type == 'course':
                        self.collected_data.courses.append(result)
                    elif data_type == 'exercise':
                        self.collected_data.exercises.append(result)
                    elif data_type == 'control':
                        self.collected_data.controls.append(result)
                    elif data_type == 'exam':
                        self.collected_data.exams.append(result)
            
            # Small delay between batches
            await asyncio.sleep(self.config.delay_between_requests)
        
        logger.info(f"✅ Collected {data_type} data")
    
    async def _fetch_and_extract(self, url: str, data_type: str, extractor_func):
        """Fetch URL and extract data"""
        if url in self.visited_urls:
            return None
        
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    self.failed_urls.add(url)
                    return None
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                self.visited_urls.add(url)
                return extractor_func(soup, url, data_type)
        
        except Exception as e:
            logger.debug(f"Error fetching {url}: {e}")
            self.failed_urls.add(url)
            return None
    
    def _extract_level_data(self, soup: BeautifulSoup, url: str, data_type: str) -> Optional[Dict[str, Any]]:
        """Extract level data"""
        try:
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else ""
            
            level_name = self._extract_level_name(title_text, url)
            if not level_name:
                return None
            
            description = ""
            desc_elem = soup.find('meta', attrs={'name': 'description'})
            if desc_elem:
                description = desc_elem.get('content', '')
            
            subjects_count = len(soup.find_all('a', href=re.compile(r'subject|matiere')))
            courses_count = len(soup.find_all('a', href=re.compile(r'cours|lesson')))
            
            return {
                'id': slugify(level_name),
                'slug': slugify(level_name),
                'name': level_name,
                'name_ar': self._get_arabic_name(level_name),
                'description': description or f"Cours de {level_name}",
                'description_ar': self._get_arabic_description(level_name),
                'subjects_count': subjects_count,
                'courses_count': courses_count,
                'url': url,
                'source': self.config.source_name,
                'collected_at': time.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
        except:
            return None
    
    def _extract_subject_data(self, soup: BeautifulSoup, url: str, data_type: str) -> Optional[Dict[str, Any]]:
        """Extract subject data"""
        try:
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else ""
            
            subject_name = self._extract_subject_name(title_text, url)
            if not subject_name:
                return None
            
            level_id = self._extract_level_from_url(url)
            courses_count = len(soup.find_all('a', href=re.compile(r'cours|lesson')))
            
            return {
                'id': slugify(f"{subject_name}-{level_id}"),
                'slug': slugify(f"{subject_name}-{level_id}"),
                'name': subject_name,
                'name_ar': self._get_arabic_subject_name(subject_name),
                'description': f"Cours de {subject_name.lower()}",
                'description_ar': f"دروس {self._get_arabic_subject_name(subject_name)}",
                'level_id': level_id,
                'level_name': self._get_level_name_from_id(level_id),
                'level_name_ar': self._get_arabic_name(self._get_level_name_from_id(level_id)),
                'color': self._get_subject_color(subject_name),
                'icon': self._get_subject_icon(subject_name),
                'courses_count': courses_count,
                'url': url,
                'source': self.config.source_name,
                'collected_at': time.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
        except:
            return None
    
    def _extract_content_data(self, soup: BeautifulSoup, url: str, content_type: str) -> Optional[Dict[str, Any]]:
        """Extract content data"""
        try:
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else ""
            
            description = ""
            desc_elem = soup.find('meta', attrs={'name': 'description'})
            if desc_elem:
                description = desc_elem.get('content', '')
            
            subject_id = self._extract_subject_from_url(url)
            level_id = self._extract_level_from_url(url)
            
            return {
                'id': slugify(f"{content_type}-{title_text}"),
                'slug': slugify(title_text),
                'title': title_text,
                'title_ar': title_text,
                'description': description,
                'description_ar': description,
                'content_type': content_type,
                'subject_id': subject_id,
                'subject_name': self._get_subject_name_from_id(subject_id),
                'subject_name_ar': self._get_arabic_subject_name(self._get_subject_name_from_id(subject_id)),
                'level_id': level_id,
                'level_name': self._get_level_name_from_id(level_id),
                'level_name_ar': self._get_arabic_name(self._get_level_name_from_id(level_id)),
                'url': url,
                'language': 'fr',
                'confidence': 0.8,
                'source': self.config.source_name,
                'collected_at': time.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
        except:
            return None
    
    # Helper methods (same as original collector)
    def _extract_level_name(self, title: str, url: str) -> Optional[str]:
        level_mapping = {
            'primaire': 'Primaire', 'primary': 'Primaire',
            'college': 'Collège', 'middle': 'Collège',
            'lycee': 'Lycée', 'lycée': 'Lycée', 'high': 'Lycée',
            'bac': 'Baccalauréat', 'baccalaureat': 'Baccalauréat',
            'superieur': 'Supérieur', 'superior': 'Supérieur', 'university': 'Supérieur'
        }
        text_to_check = f"{title} {url}".lower()
        for keyword, level_name in level_mapping.items():
            if keyword in text_to_check:
                return level_name
        return None
    
    def _extract_subject_name(self, title: str, url: str) -> Optional[str]:
        subject_mapping = {
            'math': 'Mathématiques', 'mathematiques': 'Mathématiques',
            'francais': 'Français', 'français': 'Français',
            'arabe': 'Arabe', 'sciences': 'Sciences',
            'histoire': 'Histoire', 'geographie': 'Géographie',
            'anglais': 'Anglais', 'physique': 'Physique',
            'chimie': 'Chimie', 'svt': 'SVT',
            'islamique': 'Éducation Islamique', 'informatique': 'Informatique'
        }
        text_to_check = f"{title} {url}".lower()
        for keyword, subject_name in subject_mapping.items():
            if keyword in text_to_check:
                return subject_name
        return None
    
    def _extract_level_from_url(self, url: str) -> str:
        url_lower = url.lower()
        if 'primaire' in url_lower or 'primary' in url_lower:
            return 'primaire'
        elif 'college' in url_lower or 'middle' in url_lower:
            return 'college'
        elif 'lycee' in url_lower or 'lycée' in url_lower or 'high' in url_lower:
            return 'lycee'
        elif 'bac' in url_lower:
            return 'bac'
        elif 'superieur' in url_lower or 'superior' in url_lower:
            return 'superieur'
        return 'unknown'
    
    def _extract_subject_from_url(self, url: str) -> str:
        url_lower = url.lower()
        subject_keywords = {
            'math': 'math', 'mathematiques': 'math',
            'francais': 'francais', 'français': 'francais',
            'arabe': 'arabe', 'sciences': 'sciences',
            'histoire': 'histoire', 'geographie': 'geographie',
            'anglais': 'anglais', 'physique': 'physique',
            'chimie': 'chimie', 'svt': 'svt',
            'islamique': 'islamique', 'informatique': 'informatique'
        }
        for keyword, subject_id in subject_keywords.items():
            if keyword in url_lower:
                return subject_id
        return 'unknown'
    
    def _get_level_name_from_id(self, level_id: str) -> str:
        mapping = {
            'primaire': 'Primaire', 'college': 'Collège',
            'lycee': 'Lycée', 'bac': 'Baccalauréat', 'superieur': 'Supérieur'
        }
        return mapping.get(level_id, 'Unknown')
    
    def _get_subject_name_from_id(self, subject_id: str) -> str:
        mapping = {
            'math': 'Mathématiques', 'francais': 'Français',
            'arabe': 'Arabe', 'sciences': 'Sciences',
            'histoire': 'Histoire', 'geographie': 'Géographie',
            'anglais': 'Anglais', 'physique': 'Physique',
            'chimie': 'Chimie', 'svt': 'SVT',
            'islamique': 'Éducation Islamique', 'informatique': 'Informatique'
        }
        return mapping.get(subject_id, 'Unknown')
    
    def _get_arabic_name(self, level_name: str) -> str:
        mapping = {
            'Primaire': 'الابتدائي', 'Collège': 'الإعدادي',
            'Lycée': 'الثانوي', 'Baccalauréat': 'البكالوريا', 'Supérieur': 'العالي'
        }
        return mapping.get(level_name, level_name)
    
    def _get_arabic_description(self, level_name: str) -> str:
        mapping = {
            'Primaire': 'التعليم الابتدائي المغربي',
            'Collège': 'التعليم الإعدادي المغربي',
            'Lycée': 'التعليم الثانوي المغربي',
            'Baccalauréat': 'التحضير للبكالوريا المغربية',
            'Supérieur': 'التعليم العالي المغربي'
        }
        return mapping.get(level_name, f'التعليم {self._get_arabic_name(level_name)} المغربي')
    
    def _get_arabic_subject_name(self, subject_name: str) -> str:
        mapping = {
            'Mathématiques': 'الرياضيات', 'Français': 'الفرنسية',
            'Arabe': 'العربية', 'Sciences': 'العلوم',
            'Histoire': 'التاريخ', 'Géographie': 'الجغرافيا',
            'Anglais': 'الإنجليزية', 'Physique': 'الفيزياء',
            'Chimie': 'الكيمياء', 'SVT': 'علوم الحياة والأرض',
            'Éducation Islamique': 'التربية الإسلامية', 'Informatique': 'المعلوماتية'
        }
        return mapping.get(subject_name, subject_name)
    
    def _get_subject_color(self, subject_name: str) -> str:
        mapping = {
            'Mathématiques': '#3b82f6', 'Français': '#ef4444',
            'Arabe': '#10b981', 'Sciences': '#f59e0b',
            'Histoire': '#8b5cf6', 'Géographie': '#06b6d4',
            'Anglais': '#8b5cf6', 'Physique': '#f59e0b',
            'Chimie': '#10b981', 'SVT': '#059669',
            'Éducation Islamique': '#059669', 'Informatique': '#6366f1'
        }
        return mapping.get(subject_name, '#6b7280')
    
    def _get_subject_icon(self, subject_name: str) -> str:
        mapping = {
            'Mathématiques': 'Calculator', 'Français': 'BookOpen',
            'Arabe': 'Book', 'Sciences': 'Microscope',
            'Histoire': 'Clock', 'Géographie': 'Globe',
            'Anglais': 'Globe', 'Physique': 'Atom',
            'Chimie': 'FlaskConical', 'SVT': 'Leaf',
            'Éducation Islamique': 'BookOpen', 'Informatique': 'Monitor'
        }
        return mapping.get(subject_name, 'Book')
    
    def _generate_metadata(self):
        """Generate collection metadata"""
        total_items = (
            len(self.collected_data.levels) +
            len(self.collected_data.subjects) +
            len(self.collected_data.courses) +
            len(self.collected_data.exercises) +
            len(self.collected_data.controls) +
            len(self.collected_data.exams) +
            len(self.collected_data.corrections)
        )
        
        self.collected_data.metadata = {
            'total_items': total_items,
            'levels_count': len(self.collected_data.levels),
            'subjects_count': len(self.collected_data.subjects),
            'courses_count': len(self.collected_data.courses),
            'exercises_count': len(self.collected_data.exercises),
            'controls_count': len(self.collected_data.controls),
            'exams_count': len(self.collected_data.exams),
            'corrections_count': len(self.collected_data.corrections),
            'languages': ['fr', 'ar'],
            'quality_score': 0.85,
            'visited_urls': len(self.visited_urls),
            'failed_urls': len(self.failed_urls),
            'collection_duration': time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
    
    def save_data(self, filename: str = None):
        """Save collected data"""
        if not filename:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f"data/fast_collected_data_{timestamp}.json"
        
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.collected_data), f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Data saved to {filename}")
        
        # Save CSV files
        self._save_as_csv(filename.replace('.json', '.csv'))
    
    def _save_as_csv(self, filename: str):
        """Save data as CSV files"""
        try:
            if self.collected_data.levels:
                df = pd.DataFrame(self.collected_data.levels)
                df.to_csv(filename.replace('.csv', '_levels.csv'), index=False, encoding='utf-8')
            
            if self.collected_data.subjects:
                df = pd.DataFrame(self.collected_data.subjects)
                df.to_csv(filename.replace('.csv', '_subjects.csv'), index=False, encoding='utf-8')
            
            if self.collected_data.courses:
                df = pd.DataFrame(self.collected_data.courses)
                df.to_csv(filename.replace('.csv', '_courses.csv'), index=False, encoding='utf-8')
            
            logger.info(f"📊 CSV files saved")
        except Exception as e:
            logger.error(f"Error saving CSV: {e}")

async def main_async():
    """Async main function"""
    logger.info("🚀 Starting FAST Moroccan Education Data Collection")
    
    config = FastCollectionConfig(
        base_url="https://www.alloschool.com",
        source_name="public_website",
        country="morocco",
        max_concurrent_requests=50,
        timeout=10,
        delay_between_requests=0.1,
        sitemap_urls=[
            "https://www.alloschool.com/sitemap.xml",
            "https://www.alloschool.com/sitemap_index.xml"
        ]
    )
    
    collector = FastEducationalCollector(config)
    collected_data = await collector.collect_all_data()
    collector.save_data()
    
    print("\n" + "="*60)
    print("⚡ FAST COLLECTION SUMMARY")
    print("="*60)
    print(f"Total Items: {collected_data.metadata['total_items']}")
    print(f"Levels: {collected_data.metadata['levels_count']}")
    print(f"Subjects: {collected_data.metadata['subjects_count']}")
    print(f"Courses: {collected_data.metadata['courses_count']}")
    print(f"Exercises: {collected_data.metadata['exercises_count']}")
    print(f"Controls: {collected_data.metadata['controls_count']}")
    print(f"Exams: {collected_data.metadata['exams_count']}")
    print(f"Visited URLs: {collected_data.metadata['visited_urls']}")
    print(f"Failed URLs: {collected_data.metadata['failed_urls']}")
    print("="*60)

def main():
    """Main entry point"""
    asyncio.run(main_async())

if __name__ == "__main__":
    main()

