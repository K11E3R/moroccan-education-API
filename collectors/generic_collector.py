#!/usr/bin/env python3
"""
Generic Educational Data Collector

A flexible, configurable data collection system for educational websites.
This collector can be adapted to work with any educational platform by
modifying the configuration file.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
import asyncio
import aiohttp
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Set, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
from fake_useragent import UserAgent
import xml.etree.ElementTree as ET
from slugify import slugify
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class CollectionConfig:
    """Configuration for data collection"""
    base_url: str
    source_name: str
    country: str
    respect_robots: bool = True
    delay_between_requests: float = 1.0
    max_concurrent_requests: int = 5
    timeout: int = 30
    user_agent: str = None
    sitemap_urls: List[str] = None
    content_selectors: Dict[str, str] = None
    url_patterns: Dict[str, str] = None
    data_extraction_rules: Dict[str, Dict[str, str]] = None

@dataclass
class CollectedData:
    """Container for collected educational data"""
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

class GenericEducationalCollector:
    """Generic educational data collector"""
    
    def __init__(self, config: CollectionConfig):
        self.config = config
        self.session = requests.Session()
        self.ua = UserAgent()
        
        # Set up session
        self.session.headers.update({
            'User-Agent': config.user_agent or self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,ar;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
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
        
    def collect_all_data(self) -> CollectedData:
        """Main method to collect all educational data"""
        logger.info(f"Starting data collection from {self.config.base_url}")
        
        try:
            # Step 1: Check robots.txt compliance
            if self.config.respect_robots:
                self._check_robots_txt()
            
            # Step 2: Discover sitemaps
            sitemaps = self._discover_sitemaps()
            
            # Step 3: Extract URLs from sitemaps
            all_urls = self._extract_urls_from_sitemaps(sitemaps)
            
            # Step 4: Categorize URLs
            categorized_urls = self._categorize_urls(all_urls)
            
            # Step 5: Collect data by category
            self._collect_levels(categorized_urls.get('levels', []))
            self._collect_subjects(categorized_urls.get('subjects', []))
            self._collect_content(categorized_urls.get('courses', []), 'courses')
            self._collect_content(categorized_urls.get('exercises', []), 'exercises')
            self._collect_content(categorized_urls.get('controls', []), 'controls')
            self._collect_content(categorized_urls.get('exams', []), 'exams')
            self._collect_content(categorized_urls.get('corrections', []), 'corrections')
            
            # Step 6: Generate metadata
            self._generate_metadata()
            
            logger.info("Data collection completed successfully!")
            return self.collected_data
            
        except Exception as e:
            logger.error(f"Error during data collection: {e}")
            raise
    
    def _check_robots_txt(self):
        """Check robots.txt compliance"""
        try:
            robots_url = urljoin(self.config.base_url, '/robots.txt')
            response = self.session.get(robots_url, timeout=10)
            
            if response.status_code == 200:
                robots_content = response.text
                logger.info("Robots.txt found and respected")
                
                # Check for crawl delay
                crawl_delay_match = re.search(r'crawl-delay:\s*(\d+)', robots_content, re.IGNORECASE)
                if crawl_delay_match:
                    delay = int(crawl_delay_match.group(1))
                    self.config.delay_between_requests = max(delay, self.config.delay_between_requests)
                    logger.info(f"Adjusted delay to {delay} seconds based on robots.txt")
        
        except Exception as e:
            logger.warning(f"Could not check robots.txt: {e}")
    
    def _discover_sitemaps(self) -> List[str]:
        """Discover sitemap URLs"""
        sitemaps = []
        
        # Use provided sitemap URLs
        if self.config.sitemap_urls:
            sitemaps.extend(self.config.sitemap_urls)
        
        # Check robots.txt for sitemaps
        try:
            robots_url = urljoin(self.config.base_url, '/robots.txt')
            response = self.session.get(robots_url, timeout=10)
            
            if response.status_code == 200:
                for line in response.text.split('\n'):
                    if line.strip().lower().startswith('sitemap:'):
                        sitemap_url = line.split(':', 1)[1].strip()
                        sitemaps.append(sitemap_url)
        
        except Exception as e:
            logger.warning(f"Could not fetch robots.txt: {e}")
        
        # Check common sitemap locations
        common_sitemaps = [
            '/sitemap.xml',
            '/sitemap_index.xml',
            '/sitemaps/sitemap.xml'
        ]
        
        for sitemap_path in common_sitemaps:
            sitemap_url = urljoin(self.config.base_url, sitemap_path)
            try:
                response = self.session.head(sitemap_url, timeout=5)
                if response.status_code == 200:
                    sitemaps.append(sitemap_url)
            except Exception:
                continue
        
        logger.info(f"Found {len(sitemaps)} sitemaps")
        return sitemaps
    
    def _extract_urls_from_sitemaps(self, sitemaps: List[str]) -> List[str]:
        """Extract URLs from sitemap files"""
        all_urls = []
        
        for sitemap_url in sitemaps:
            try:
                logger.info(f"Processing sitemap: {sitemap_url}")
                response = self.session.get(sitemap_url, timeout=15)
                response.raise_for_status()
                
                # Parse XML sitemap
                root = ET.fromstring(response.content)
                
                # Handle sitemap index
                if root.tag.endswith('sitemapindex'):
                    for sitemap_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap'):
                        loc_elem = sitemap_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                        if loc_elem is not None:
                            nested_urls = self._extract_urls_from_sitemaps([loc_elem.text])
                            all_urls.extend(nested_urls)
                
                # Handle regular sitemap
                elif root.tag.endswith('urlset'):
                    for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                        loc_elem = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                        if loc_elem is not None:
                            all_urls.append(loc_elem.text)
                
                time.sleep(self.config.delay_between_requests)
                
            except Exception as e:
                logger.error(f"Error processing sitemap {sitemap_url}: {e}")
                continue
        
        logger.info(f"Extracted {len(all_urls)} URLs from sitemaps")
        return all_urls
    
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
        
        # Define URL patterns for categorization
        patterns = {
            'levels': [r'level', r'niveau', r'primaire', r'college', r'lycee', r'bac', r'superieur'],
            'subjects': [r'subject', r'matiere', r'math', r'francais', r'arabe', r'sciences'],
            'courses': [r'cours', r'lesson', r'lecon'],
            'exercises': [r'exercice', r'exercise', r'pratique'],
            'controls': [r'controle', r'control', r'test'],
            'exams': [r'examen', r'exam', r'evaluation'],
            'corrections': [r'correction', r'solution', r'reponse']
        }
        
        for url in urls:
            url_lower = url.lower()
            
            for category, category_patterns in patterns.items():
                if any(re.search(pattern, url_lower) for pattern in category_patterns):
                    categorized[category].append(url)
                    break
        
        # Log categorization results
        for category, urls_list in categorized.items():
            logger.info(f"Categorized {len(urls_list)} URLs as {category}")
        
        return categorized
    
    def _collect_levels(self, level_urls: List[str]):
        """Collect education level data"""
        logger.info(f"Collecting data from {len(level_urls)} level URLs")
        
        for url in level_urls[:50]:  # Limit to first 50 URLs
            try:
                if url in self.visited_urls:
                    continue
                
                response = self.session.get(url, timeout=self.config.timeout)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract level information
                level_data = self._extract_level_data(soup, url)
                if level_data:
                    self.collected_data.levels.append(level_data)
                
                self.visited_urls.add(url)
                time.sleep(self.config.delay_between_requests)
                
            except Exception as e:
                logger.error(f"Error collecting level data from {url}: {e}")
                self.failed_urls.add(url)
                continue
    
    def _extract_level_data(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """Extract level data from page"""
        try:
            # Extract title
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else ""
            
            # Extract level name from title or URL
            level_name = self._extract_level_name(title_text, url)
            
            if not level_name:
                return None
            
            # Extract description
            description = ""
            desc_elem = soup.find('meta', attrs={'name': 'description'})
            if desc_elem:
                description = desc_elem.get('content', '')
            
            # Count subjects and courses
            subjects_count = len(soup.find_all('a', href=re.compile(r'subject|matiere')))
            courses_count = len(soup.find_all('a', href=re.compile(r'cours|lesson')))
            
            return {
                'id': slugify(level_name),
                'slug': slugify(level_name),
                'name': level_name,
                'name_ar': self._get_arabic_name(level_name),
                'description': description,
                'description_ar': self._get_arabic_description(level_name),
                'subjects_count': subjects_count,
                'courses_count': courses_count,
                'url': url,
                'source': self.config.source_name,
                'collected_at': time.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            
        except Exception as e:
            logger.error(f"Error extracting level data: {e}")
            return None
    
    def _extract_level_name(self, title: str, url: str) -> Optional[str]:
        """Extract level name from title or URL"""
        # Level mapping
        level_mapping = {
            'primaire': 'Primaire',
            'primary': 'Primaire',
            'college': 'Collège',
            'middle': 'Collège',
            'lycee': 'Lycée',
            'lycée': 'Lycée',
            'high': 'Lycée',
            'bac': 'Baccalauréat',
            'baccalaureat': 'Baccalauréat',
            'superieur': 'Supérieur',
            'superior': 'Supérieur',
            'university': 'Supérieur'
        }
        
        text_to_check = f"{title} {url}".lower()
        
        for keyword, level_name in level_mapping.items():
            if keyword in text_to_check:
                return level_name
        
        return None
    
    def _get_arabic_name(self, level_name: str) -> str:
        """Get Arabic name for level"""
        arabic_mapping = {
            'Primaire': 'الابتدائي',
            'Collège': 'الإعدادي',
            'Lycée': 'الثانوي',
            'Baccalauréat': 'البكالوريا',
            'Supérieur': 'العالي'
        }
        return arabic_mapping.get(level_name, level_name)
    
    def _get_arabic_description(self, level_name: str) -> str:
        """Get Arabic description for level"""
        arabic_descriptions = {
            'Primaire': 'التعليم الابتدائي المغربي',
            'Collège': 'التعليم الإعدادي المغربي',
            'Lycée': 'التعليم الثانوي المغربي',
            'Baccalauréat': 'التحضير للبكالوريا المغربية',
            'Supérieur': 'التعليم العالي المغربي'
        }
        return arabic_descriptions.get(level_name, f'التعليم {self._get_arabic_name(level_name)} المغربي')
    
    def _collect_subjects(self, subject_urls: List[str]):
        """Collect subject data"""
        logger.info(f"Collecting data from {len(subject_urls)} subject URLs")
        
        for url in subject_urls[:100]:  # Limit to first 100 URLs
            try:
                if url in self.visited_urls:
                    continue
                
                response = self.session.get(url, timeout=self.config.timeout)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract subject information
                subject_data = self._extract_subject_data(soup, url)
                if subject_data:
                    self.collected_data.subjects.append(subject_data)
                
                self.visited_urls.add(url)
                time.sleep(self.config.delay_between_requests)
                
            except Exception as e:
                logger.error(f"Error collecting subject data from {url}: {e}")
                self.failed_urls.add(url)
                continue
    
    def _extract_subject_data(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """Extract subject data from page"""
        try:
            # Extract title
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else ""
            
            # Extract subject name
            subject_name = self._extract_subject_name(title_text, url)
            
            if not subject_name:
                return None
            
            # Extract level from URL or content
            level_id = self._extract_level_from_url(url)
            
            # Count courses
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
            
        except Exception as e:
            logger.error(f"Error extracting subject data: {e}")
            return None
    
    def _extract_subject_name(self, title: str, url: str) -> Optional[str]:
        """Extract subject name from title or URL"""
        subject_mapping = {
            'math': 'Mathématiques',
            'mathematiques': 'Mathématiques',
            'francais': 'Français',
            'français': 'Français',
            'arabe': 'Arabe',
            'sciences': 'Sciences',
            'histoire': 'Histoire',
            'geographie': 'Géographie',
            'anglais': 'Anglais',
            'physique': 'Physique',
            'chimie': 'Chimie',
            'svt': 'SVT',
            'islamique': 'Éducation Islamique',
            'informatique': 'Informatique'
        }
        
        text_to_check = f"{title} {url}".lower()
        
        for keyword, subject_name in subject_mapping.items():
            if keyword in text_to_check:
                return subject_name
        
        return None
    
    def _extract_level_from_url(self, url: str) -> str:
        """Extract level ID from URL"""
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
    
    def _get_level_name_from_id(self, level_id: str) -> str:
        """Get level name from ID"""
        level_mapping = {
            'primaire': 'Primaire',
            'college': 'Collège',
            'lycee': 'Lycée',
            'bac': 'Baccalauréat',
            'superieur': 'Supérieur'
        }
        return level_mapping.get(level_id, 'Unknown')
    
    def _get_arabic_subject_name(self, subject_name: str) -> str:
        """Get Arabic name for subject"""
        arabic_mapping = {
            'Mathématiques': 'الرياضيات',
            'Français': 'الفرنسية',
            'Arabe': 'العربية',
            'Sciences': 'العلوم',
            'Histoire': 'التاريخ',
            'Géographie': 'الجغرافيا',
            'Anglais': 'الإنجليزية',
            'Physique': 'الفيزياء',
            'Chimie': 'الكيمياء',
            'SVT': 'علوم الحياة والأرض',
            'Éducation Islamique': 'التربية الإسلامية',
            'Informatique': 'المعلوماتية'
        }
        return arabic_mapping.get(subject_name, subject_name)
    
    def _get_subject_color(self, subject_name: str) -> str:
        """Get color for subject"""
        color_mapping = {
            'Mathématiques': '#3b82f6',
            'Français': '#ef4444',
            'Arabe': '#10b981',
            'Sciences': '#f59e0b',
            'Histoire': '#8b5cf6',
            'Géographie': '#06b6d4',
            'Anglais': '#8b5cf6',
            'Physique': '#f59e0b',
            'Chimie': '#10b981',
            'SVT': '#059669',
            'Éducation Islamique': '#059669',
            'Informatique': '#6366f1'
        }
        return color_mapping.get(subject_name, '#6b7280')
    
    def _get_subject_icon(self, subject_name: str) -> str:
        """Get icon for subject"""
        icon_mapping = {
            'Mathématiques': 'Calculator',
            'Français': 'BookOpen',
            'Arabe': 'Book',
            'Sciences': 'Microscope',
            'Histoire': 'Clock',
            'Géographie': 'Globe',
            'Anglais': 'Globe',
            'Physique': 'Atom',
            'Chimie': 'FlaskConical',
            'SVT': 'Leaf',
            'Éducation Islamique': 'BookOpen',
            'Informatique': 'Monitor'
        }
        return icon_mapping.get(subject_name, 'Book')
    
    def _collect_content(self, content_urls: List[str], content_type: str):
        """Collect content data (courses, exercises, etc.)"""
        logger.info(f"Collecting {content_type} from {len(content_urls)} URLs")
        
        for url in content_urls[:200]:  # Limit to first 200 URLs
            try:
                if url in self.visited_urls:
                    continue
                
                response = self.session.get(url, timeout=self.config.timeout)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract content information
                content_data = self._extract_content_data(soup, url, content_type)
                if content_data:
                    getattr(self.collected_data, content_type).append(content_data)
                
                self.visited_urls.add(url)
                time.sleep(self.config.delay_between_requests)
                
            except Exception as e:
                logger.error(f"Error collecting {content_type} data from {url}: {e}")
                self.failed_urls.add(url)
                continue
    
    def _extract_content_data(self, soup: BeautifulSoup, url: str, content_type: str) -> Optional[Dict[str, Any]]:
        """Extract content data from page"""
        try:
            # Extract title
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else ""
            
            # Extract description
            description = ""
            desc_elem = soup.find('meta', attrs={'name': 'description'})
            if desc_elem:
                description = desc_elem.get('content', '')
            
            # Extract subject and level
            subject_id = self._extract_subject_from_url(url)
            level_id = self._extract_level_from_url(url)
            
            return {
                'id': slugify(f"{content_type}-{title_text}"),
                'slug': slugify(title_text),
                'title': title_text,
                'title_ar': self._get_arabic_title(title_text),
                'description': description,
                'description_ar': self._get_arabic_description_text(description),
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
            
        except Exception as e:
            logger.error(f"Error extracting {content_type} data: {e}")
            return None
    
    def _extract_subject_from_url(self, url: str) -> str:
        """Extract subject ID from URL"""
        url_lower = url.lower()
        
        subject_keywords = {
            'math': 'math',
            'mathematiques': 'math',
            'francais': 'francais',
            'français': 'francais',
            'arabe': 'arabe',
            'sciences': 'sciences',
            'histoire': 'histoire',
            'geographie': 'geographie',
            'anglais': 'anglais',
            'physique': 'physique',
            'chimie': 'chimie',
            'svt': 'svt',
            'islamique': 'islamique',
            'informatique': 'informatique'
        }
        
        for keyword, subject_id in subject_keywords.items():
            if keyword in url_lower:
                return subject_id
        
        return 'unknown'
    
    def _get_subject_name_from_id(self, subject_id: str) -> str:
        """Get subject name from ID"""
        subject_mapping = {
            'math': 'Mathématiques',
            'francais': 'Français',
            'arabe': 'Arabe',
            'sciences': 'Sciences',
            'histoire': 'Histoire',
            'geographie': 'Géographie',
            'anglais': 'Anglais',
            'physique': 'Physique',
            'chimie': 'Chimie',
            'svt': 'SVT',
            'islamique': 'Éducation Islamique',
            'informatique': 'Informatique'
        }
        return subject_mapping.get(subject_id, 'Unknown')
    
    def _get_arabic_title(self, title: str) -> str:
        """Get Arabic version of title"""
        # Simple mapping for common terms
        arabic_mapping = {
            'addition': 'الجمع',
            'soustraction': 'الطرح',
            'multiplication': 'الضرب',
            'division': 'القسمة',
            'alphabet': 'الأبجدية',
            'corps humain': 'الجسم البشري',
            'histoire du maroc': 'تاريخ المغرب',
            'géographie du maroc': 'جغرافية المغرب'
        }
        
        title_lower = title.lower()
        for french, arabic in arabic_mapping.items():
            if french in title_lower:
                return arabic
        
        return title  # Return original if no mapping found
    
    def _get_arabic_description_text(self, description: str) -> str:
        """Get Arabic version of description"""
        # Simple mapping for common descriptions
        arabic_mapping = {
            'apprendre': 'تعلم',
            'cours': 'دروس',
            'exercice': 'تمرين',
            'controle': 'مراقبة',
            'examen': 'امتحان',
            'correction': 'تصحيح'
        }
        
        description_lower = description.lower()
        for french, arabic in arabic_mapping.items():
            if french in description_lower:
                description = description.replace(french, arabic)
        
        return description
    
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
        """Save collected data to file"""
        if not filename:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f"data/collected_data_{timestamp}.json"
        
        # Ensure directory exists
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.collected_data), f, indent=2, ensure_ascii=False)
        
        logger.info(f"Data saved to {filename}")
        
        # Also save as CSV for analysis
        self._save_as_csv(filename.replace('.json', '.csv'))
    
    def _save_as_csv(self, filename: str):
        """Save data as CSV files for analysis"""
        try:
            # Save levels
            if self.collected_data.levels:
                df_levels = pd.DataFrame(self.collected_data.levels)
                df_levels.to_csv(filename.replace('.csv', '_levels.csv'), index=False, encoding='utf-8')
            
            # Save subjects
            if self.collected_data.subjects:
                df_subjects = pd.DataFrame(self.collected_data.subjects)
                df_subjects.to_csv(filename.replace('.csv', '_subjects.csv'), index=False, encoding='utf-8')
            
            # Save courses
            if self.collected_data.courses:
                df_courses = pd.DataFrame(self.collected_data.courses)
                df_courses.to_csv(filename.replace('.csv', '_courses.csv'), index=False, encoding='utf-8')
            
            logger.info(f"CSV files saved with prefix: {filename}")
            
        except Exception as e:
            logger.error(f"Error saving CSV files: {e}")

def create_moroccan_config() -> CollectionConfig:
    """Create configuration for Moroccan education website"""
    return CollectionConfig(
        base_url="https://www.alloschool.com",
        source_name="public_website",
        country="morocco",
        respect_robots=True,
        delay_between_requests=2.0,
        max_concurrent_requests=3,
        timeout=30,
        sitemap_urls=[
            "https://www.alloschool.com/sitemap.xml",
            "https://www.alloschool.com/sitemap_index.xml"
        ],
        content_selectors={
            'title': 'h1, .title, .page-title',
            'description': '.description, .content, .summary',
            'level': '.level, .niveau, .grade',
            'subject': '.subject, .matiere, .discipline'
        },
        url_patterns={
            'levels': r'/category/(primaire|college|lycee|bac|superieur)',
            'subjects': r'/category/[^/]+/(primaire|college|lycee|bac|superieur)',
            'courses': r'/cours/',
            'exercises': r'/exercice/',
            'controls': r'/controle/',
            'exams': r'/examen/',
            'corrections': r'/correction/'
        }
    )

def main():
    """Main function to run data collection"""
    logger.info("Starting Moroccan Education Data Collection")
    
    # Create configuration
    config = create_moroccan_config()
    
    # Create collector
    collector = GenericEducationalCollector(config)
    
    # Collect data
    collected_data = collector.collect_all_data()
    
    # Save data
    collector.save_data()
    
    # Print summary
    print("\n" + "="*60)
    print("DATA COLLECTION SUMMARY")
    print("="*60)
    print(f"Source: {collected_data.source}")
    print(f"Country: {collected_data.country}")
    print(f"Collection Date: {collected_data.collection_date}")
    print(f"Total Items: {collected_data.metadata['total_items']}")
    print(f"Levels: {collected_data.metadata['levels_count']}")
    print(f"Subjects: {collected_data.metadata['subjects_count']}")
    print(f"Courses: {collected_data.metadata['courses_count']}")
    print(f"Exercises: {collected_data.metadata['exercises_count']}")
    print(f"Controls: {collected_data.metadata['controls_count']}")
    print(f"Exams: {collected_data.metadata['exams_count']}")
    print(f"Corrections: {collected_data.metadata['corrections_count']}")
    print(f"Visited URLs: {collected_data.metadata['visited_urls']}")
    print(f"Failed URLs: {collected_data.metadata['failed_urls']}")
    print("="*60)
    
    logger.info("Data collection completed successfully!")

if __name__ == "__main__":
    main()
