#!/usr/bin/env python3
"""
Website Structure Analyzer for Moroccan Education Platform

This script analyzes the structure of the public Moroccan education website
to understand how educational content is organized and accessed.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin, urlparse
from collections import defaultdict
import logging
from typing import Dict, List, Set, Any
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class WebsiteStructure:
    """Data class to store website structure analysis"""
    base_url: str
    sitemaps: List[str]
    navigation_patterns: Dict[str, List[str]]
    content_patterns: Dict[str, List[str]]
    url_structure: Dict[str, str]
    data_sources: List[str]
    languages: List[str]
    content_types: List[str]
    analysis_timestamp: str

class WebsiteAnalyzer:
    """Generic website structure analyzer for educational platforms"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.visited_urls: Set[str] = set()
        self.structure_data: Dict[str, Any] = defaultdict(list)
        
    def analyze_website(self) -> WebsiteStructure:
        """Main method to analyze website structure"""
        logger.info(f"Starting analysis of {self.base_url}")
        
        # Step 1: Check robots.txt and sitemaps
        sitemaps = self._find_sitemaps()
        
        # Step 2: Analyze homepage structure
        homepage_analysis = self._analyze_homepage()
        
        # Step 3: Discover navigation patterns
        navigation_patterns = self._discover_navigation_patterns()
        
        # Step 4: Identify content patterns
        content_patterns = self._identify_content_patterns()
        
        # Step 5: Map URL structure
        url_structure = self._map_url_structure()
        
        # Step 6: Identify data sources
        data_sources = self._identify_data_sources()
        
        # Step 7: Detect languages
        languages = self._detect_languages()
        
        # Step 8: Identify content types
        content_types = self._identify_content_types()
        
        return WebsiteStructure(
            base_url=self.base_url,
            sitemaps=sitemaps,
            navigation_patterns=navigation_patterns,
            content_patterns=content_patterns,
            url_structure=url_structure,
            data_sources=data_sources,
            languages=languages,
            content_types=content_types,
            analysis_timestamp=time.strftime('%Y-%m-%dT%H:%M:%SZ')
        )
    
    def _find_sitemaps(self) -> List[str]:
        """Find sitemap URLs"""
        logger.info("Looking for sitemaps...")
        sitemaps = []
        
        # Check robots.txt
        try:
            robots_url = urljoin(self.base_url, '/robots.txt')
            response = self.session.get(robots_url, timeout=10)
            if response.status_code == 200:
                for line in response.text.split('\n'):
                    if line.strip().lower().startswith('sitemap:'):
                        sitemap_url = line.split(':', 1)[1].strip()
                        sitemaps.append(sitemap_url)
                        logger.info(f"Found sitemap: {sitemap_url}")
        except Exception as e:
            logger.warning(f"Could not fetch robots.txt: {e}")
        
        # Check common sitemap locations
        common_sitemaps = [
            '/sitemap.xml',
            '/sitemap_index.xml',
            '/sitemaps/sitemap.xml',
            '/sitemap/sitemap.xml'
        ]
        
        for sitemap_path in common_sitemaps:
            sitemap_url = urljoin(self.base_url, sitemap_path)
            try:
                response = self.session.head(sitemap_url, timeout=5)
                if response.status_code == 200:
                    sitemaps.append(sitemap_url)
                    logger.info(f"Found sitemap: {sitemap_url}")
            except Exception:
                continue
        
        return sitemaps
    
    def _analyze_homepage(self) -> Dict[str, Any]:
        """Analyze homepage structure"""
        logger.info("Analyzing homepage structure...")
        
        try:
            response = self.session.get(self.base_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find navigation menus
            nav_elements = soup.find_all(['nav', 'ul', 'div'], class_=re.compile(r'nav|menu|header'))
            
            # Find main content areas
            content_areas = soup.find_all(['main', 'section', 'div'], class_=re.compile(r'content|main|body'))
            
            # Find links to educational content
            education_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                text = link.get_text(strip=True)
                
                # Look for education-related keywords
                education_keywords = ['cours', 'lesson', 'matière', 'subject', 'niveau', 'level', 'primaire', 'collège', 'lycée']
                if any(keyword.lower() in text.lower() or keyword.lower() in href.lower() for keyword in education_keywords):
                    education_links.append({
                        'text': text,
                        'href': urljoin(self.base_url, href),
                        'element': str(link)
                    })
            
            return {
                'navigation_elements': len(nav_elements),
                'content_areas': len(content_areas),
                'education_links': education_links,
                'page_title': soup.title.string if soup.title else None,
                'meta_description': soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else None
            }
            
        except Exception as e:
            logger.error(f"Error analyzing homepage: {e}")
            return {}
    
    def _discover_navigation_patterns(self) -> Dict[str, List[str]]:
        """Discover navigation patterns"""
        logger.info("Discovering navigation patterns...")
        
        patterns = {
            'level_navigation': [],
            'subject_navigation': [],
            'content_navigation': [],
            'breadcrumb_patterns': []
        }
        
        try:
            response = self.session.get(self.base_url, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for level-based navigation
            for link in soup.find_all('a', href=True):
                href = link['href']
                text = link.get_text(strip=True)
                
                # Check for level indicators
                level_patterns = [
                    r'primaire|primary',
                    r'collège|college|middle',
                    r'lycée|lycee|high',
                    r'bac|baccalauréat',
                    r'supérieur|superior|university'
                ]
                
                for pattern in level_patterns:
                    if re.search(pattern, text.lower()) or re.search(pattern, href.lower()):
                        patterns['level_navigation'].append({
                            'text': text,
                            'href': urljoin(self.base_url, href),
                            'pattern': pattern
                        })
                        break
            
            # Look for subject-based navigation
            subject_keywords = ['math', 'français', 'arabe', 'sciences', 'histoire', 'géographie', 'anglais']
            for link in soup.find_all('a', href=True):
                text = link.get_text(strip=True)
                if any(keyword.lower() in text.lower() for keyword in subject_keywords):
                    patterns['subject_navigation'].append({
                        'text': text,
                        'href': urljoin(self.base_url, link['href'])
                    })
            
            # Look for content type navigation
            content_keywords = ['cours', 'exercice', 'controle', 'examen', 'correction']
            for link in soup.find_all('a', href=True):
                text = link.get_text(strip=True)
                href = link['href']
                if any(keyword.lower() in text.lower() or keyword.lower() in href.lower() for keyword in content_keywords):
                    patterns['content_navigation'].append({
                        'text': text,
                        'href': urljoin(self.base_url, href),
                        'type': next(keyword for keyword in content_keywords if keyword.lower() in text.lower() or keyword.lower() in href.lower())
                    })
            
        except Exception as e:
            logger.error(f"Error discovering navigation patterns: {e}")
        
        return patterns
    
    def _identify_content_patterns(self) -> Dict[str, List[str]]:
        """Identify content patterns and structures"""
        logger.info("Identifying content patterns...")
        
        patterns = {
            'url_patterns': [],
            'content_selectors': [],
            'data_attributes': [],
            'api_endpoints': []
        }
        
        try:
            response = self.session.get(self.base_url, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Analyze URL patterns
            urls = set()
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('/') or self.base_url in href:
                    urls.add(href)
            
            # Group URLs by pattern
            url_groups = defaultdict(list)
            for url in urls:
                # Extract path segments
                parsed = urlparse(url)
                path_segments = [seg for seg in parsed.path.split('/') if seg]
                
                if len(path_segments) >= 2:
                    pattern = '/'.join(path_segments[:2])  # First two segments
                    url_groups[pattern].append(url)
            
            patterns['url_patterns'] = [
                {'pattern': pattern, 'examples': examples[:5], 'count': len(examples)}
                for pattern, examples in url_groups.items()
            ]
            
            # Look for data attributes
            for element in soup.find_all(attrs=lambda x: x and any(attr.startswith('data-') for attr in x.keys())):
                for attr in element.attrs:
                    if attr.startswith('data-'):
                        patterns['data_attributes'].append(attr)
            
            # Look for API endpoints in JavaScript
            script_tags = soup.find_all('script')
            for script in script_tags:
                if script.string:
                    # Look for API calls
                    api_patterns = re.findall(r'["\']([^"\']*api[^"\']*)["\']', script.string)
                    patterns['api_endpoints'].extend(api_patterns)
            
        except Exception as e:
            logger.error(f"Error identifying content patterns: {e}")
        
        return patterns
    
    def _map_url_structure(self) -> Dict[str, str]:
        """Map URL structure patterns"""
        logger.info("Mapping URL structure...")
        
        structure = {
            'base_pattern': self.base_url,
            'level_pattern': None,
            'subject_pattern': None,
            'content_pattern': None,
            'language_pattern': None
        }
        
        try:
            response = self.session.get(self.base_url, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Analyze URL patterns from links
            url_patterns = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('/') or self.base_url in href:
                    url_patterns.append(href)
            
            # Identify common patterns
            if url_patterns:
                # Look for level patterns
                level_urls = [url for url in url_patterns if any(level in url.lower() for level in ['primaire', 'college', 'lycee', 'bac'])]
                if level_urls:
                    structure['level_pattern'] = self._extract_pattern(level_urls[0])
                
                # Look for subject patterns
                subject_urls = [url for url in url_patterns if any(subject in url.lower() for subject in ['math', 'francais', 'arabe', 'sciences'])]
                if subject_urls:
                    structure['subject_pattern'] = self._extract_pattern(subject_urls[0])
                
                # Look for content patterns
                content_urls = [url for url in url_patterns if any(content in url.lower() for content in ['cours', 'exercice', 'controle'])]
                if content_urls:
                    structure['content_pattern'] = self._extract_pattern(content_urls[0])
        
        except Exception as e:
            logger.error(f"Error mapping URL structure: {e}")
        
        return structure
    
    def _extract_pattern(self, url: str) -> str:
        """Extract pattern from URL"""
        parsed = urlparse(url)
        path_segments = [seg for seg in parsed.path.split('/') if seg]
        
        # Replace specific values with placeholders
        pattern_parts = []
        for segment in path_segments:
            if segment.isdigit():
                pattern_parts.append('{id}')
            elif len(segment) > 3:
                pattern_parts.append('{slug}')
            else:
                pattern_parts.append(segment)
        
        return '/'.join(pattern_parts)
    
    def _identify_data_sources(self) -> List[str]:
        """Identify potential data sources"""
        logger.info("Identifying data sources...")
        
        sources = []
        
        try:
            response = self.session.get(self.base_url, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for JSON-LD structured data
            json_ld_scripts = soup.find_all('script', type='application/ld+json')
            if json_ld_scripts:
                sources.append('json_ld')
            
            # Look for microdata
            microdata_elements = soup.find_all(attrs={'itemscope': True})
            if microdata_elements:
                sources.append('microdata')
            
            # Look for Open Graph data
            og_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))
            if og_tags:
                sources.append('open_graph')
            
            # Look for API endpoints
            script_tags = soup.find_all('script')
            for script in script_tags:
                if script.string and 'fetch(' in script.string:
                    sources.append('javascript_api')
            
        except Exception as e:
            logger.error(f"Error identifying data sources: {e}")
        
        return sources
    
    def _detect_languages(self) -> List[str]:
        """Detect supported languages"""
        logger.info("Detecting languages...")
        
        languages = []
        
        try:
            response = self.session.get(self.base_url, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check HTML lang attribute
            html_tag = soup.find('html')
            if html_tag and html_tag.get('lang'):
                languages.append(html_tag['lang'])
            
            # Look for language switchers
            lang_links = soup.find_all('a', href=True)
            for link in lang_links:
                href = link['href']
                text = link.get_text(strip=True)
                
                # Check for language indicators
                if any(lang in href.lower() for lang in ['fr', 'ar', 'en', 'lang']):
                    languages.append(href.split('/')[-1] if '/' in href else text.lower())
            
            # Look for Arabic content
            arabic_text = soup.find_all(text=re.compile(r'[\u0600-\u06FF]'))
            if arabic_text:
                languages.append('ar')
            
            # Look for French content
            french_keywords = ['cours', 'matière', 'niveau', 'exercice']
            page_text = soup.get_text().lower()
            if any(keyword in page_text for keyword in french_keywords):
                languages.append('fr')
            
        except Exception as e:
            logger.error(f"Error detecting languages: {e}")
        
        return list(set(languages))
    
    def _identify_content_types(self) -> List[str]:
        """Identify content types available"""
        logger.info("Identifying content types...")
        
        content_types = []
        
        try:
            response = self.session.get(self.base_url, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for content type indicators in URLs and text
            type_keywords = {
                'course': ['cours', 'lesson', 'leçon'],
                'exercise': ['exercice', 'exercise', 'pratique'],
                'control': ['controle', 'control', 'test'],
                'exam': ['examen', 'exam', 'évaluation'],
                'correction': ['correction', 'solution', 'réponse']
            }
            
            page_text = soup.get_text().lower()
            page_urls = [link['href'] for link in soup.find_all('a', href=True)]
            
            for content_type, keywords in type_keywords.items():
                if any(keyword in page_text or any(keyword in url.lower() for url in page_urls) for keyword in keywords):
                    content_types.append(content_type)
            
        except Exception as e:
            logger.error(f"Error identifying content types: {e}")
        
        return content_types
    
    def save_analysis(self, structure: WebsiteStructure, filename: str = None):
        """Save analysis results to file"""
        if not filename:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f"analysis/website_structure_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(asdict(structure), f, indent=2, ensure_ascii=False)
        
        logger.info(f"Analysis saved to {filename}")

def main():
    """Main function to run website analysis"""
    
    # Target Moroccan education website
    target_url = "https://www.alloschool.com"
    
    logger.info(f"Starting analysis of Moroccan education website: {target_url}")
    
    # Create analyzer
    analyzer = WebsiteAnalyzer(target_url)
    
    # Run analysis
    structure = analyzer.analyze_website()
    
    # Save results
    analyzer.save_analysis(structure)
    
    # Print summary
    print("\n" + "="*60)
    print("WEBSITE STRUCTURE ANALYSIS SUMMARY")
    print("="*60)
    print(f"Base URL: {structure.base_url}")
    print(f"Sitemaps found: {len(structure.sitemaps)}")
    print(f"Languages detected: {structure.languages}")
    print(f"Content types: {structure.content_types}")
    print(f"Data sources: {structure.data_sources}")
    print(f"Navigation patterns: {len(structure.navigation_patterns)}")
    print(f"Content patterns: {len(structure.content_patterns)}")
    print("="*60)
    
    # Print detailed findings
    print("\nSITEMAPS:")
    for sitemap in structure.sitemaps:
        print(f"  - {sitemap}")
    
    print("\nNAVIGATION PATTERNS:")
    for pattern_type, patterns in structure.navigation_patterns.items():
        print(f"  {pattern_type}: {len(patterns)} items")
        for pattern in patterns[:3]:  # Show first 3 examples
            print(f"    - {pattern}")
    
    print("\nURL STRUCTURE:")
    for structure_type, pattern in structure.url_structure.items():
        if pattern:
            print(f"  {structure_type}: {pattern}")
    
    logger.info("Analysis completed successfully!")

if __name__ == "__main__":
    main()

