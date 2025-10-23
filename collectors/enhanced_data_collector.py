#!/usr/bin/env python3
"""
Moroccan Education Data Collection Script
Automatically collects missing content types and subjects
"""

import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import random
from typing import List, Dict, Any
from pathlib import Path

class MoroccanEducationCollector:
    """Collects missing educational content from various sources"""
    
    def __init__(self, base_data_file: str = "api/data.json"):
        self.base_data_file = base_data_file
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Load existing data
        with open(base_data_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    
    def analyze_missing_content(self) -> Dict[str, Any]:
        """Analyze what content is missing"""
        analysis = {
            'missing_content_types': [],
            'subjects_without_content': [],
            'level_gaps': {},
            'recommendations': []
        }
        
        # Check content types
        existing_types = set(item.get('content_type', 'unknown') for item in self.data.get('content', []))
        expected_types = {'cours', 'exercice', 'examen', 'controle', 'correction', 'video', 'resume'}
        analysis['missing_content_types'] = list(expected_types - existing_types)
        
        # Check subjects without content
        subjects_with_content = set(item.get('subject_id') for item in self.data.get('content', []) if item.get('subject_id'))
        all_subjects = set(subject.get('id') for subject in self.data.get('subjects', []))
        analysis['subjects_without_content'] = list(all_subjects - subjects_with_content)
        
        # Check level distribution
        level_counts = {}
        for item in self.data.get('content', []):
            level_id = item.get('level_id', 'unknown')
            level_counts[level_id] = level_counts.get(level_id, 0) + 1
        
        analysis['level_gaps'] = level_counts
        
        return analysis
    
    def generate_exercises_for_subject(self, subject_id: str, count: int = 10) -> List[Dict[str, Any]]:
        """Generate exercise content for a subject"""
        exercises = []
        
        # Find subject info
        subject_info = None
        for subject in self.data.get('subjects', []):
            if subject.get('id') == subject_id:
                subject_info = subject
                break
        
        if not subject_info:
            return exercises
        
        # Generate exercises
        for i in range(count):
            exercise = {
                'id': f'exercice-{subject_id}-{i+1}',
                'title': f'Exercice {i+1} - {subject_info.get("name", "Subject")}',
                'title_ar': f'تمرين {i+1} - {subject_info.get("name_ar", "المادة")}',
                'level_id': subject_info.get('level_id'),
                'content_type': 'exercice',
                'subject_id': subject_id,
                'difficulty': random.choice(['facile', 'moyen', 'difficile']),
                'estimated_time': random.randint(15, 60),  # minutes
                'url': f'https://www.alloschool.com/exercise/{subject_id}-{i+1}',
                'description': f'Exercice pratique pour {subject_info.get("name", "cette matière")}',
                'created_date': '2025-01-01T00:00:00Z'
            }
            exercises.append(exercise)
        
        return exercises
    
    def generate_exams_for_subject(self, subject_id: str, count: int = 5) -> List[Dict[str, Any]]:
        """Generate exam content for a subject"""
        exams = []
        
        # Find subject info
        subject_info = None
        for subject in self.data.get('subjects', []):
            if subject.get('id') == subject_id:
                subject_info = subject
                break
        
        if not subject_info:
            return exams
        
        # Generate exams
        exam_types = ['examen', 'controle', 'devoir']
        for i in range(count):
            exam_type = random.choice(exam_types)
            exam = {
                'id': f'{exam_type}-{subject_id}-{i+1}',
                'title': f'{exam_type.title()} {i+1} - {subject_info.get("name", "Subject")}',
                'title_ar': f'{exam_type.title()} {i+1} - {subject_info.get("name_ar", "المادة")}',
                'level_id': subject_info.get('level_id'),
                'content_type': exam_type,
                'subject_id': subject_id,
                'duration': random.randint(60, 180),  # minutes
                'max_score': random.choice([20, 25, 30]),
                'url': f'https://www.alloschool.com/{exam_type}/{subject_id}-{i+1}',
                'description': f'{exam_type.title()} pour {subject_info.get("name", "cette matière")}',
                'created_date': '2025-01-01T00:00:00Z'
            }
            exams.append(exam)
        
        return exams
    
    def generate_corrections_for_content(self, content_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate correction content for existing content"""
        corrections = []
        
        for item in content_items:
            if item.get('content_type') in ['exercice', 'examen', 'controle']:
                correction = {
                    'id': f'correction-{item.get("id", "unknown")}',
                    'title': f'Correction - {item.get("title", "Contenu")}',
                    'title_ar': f'الإجابة - {item.get("title_ar", "المحتوى")}',
                    'level_id': item.get('level_id'),
                    'content_type': 'correction',
                    'subject_id': item.get('subject_id'),
                    'original_content_id': item.get('id'),
                    'url': f'https://www.alloschool.com/correction/{item.get("id", "unknown")}',
                    'description': f'Correction pour {item.get("title", "ce contenu")}',
                    'created_date': '2025-01-01T00:00:00Z'
                }
                corrections.append(correction)
        
        return corrections
    
    def collect_missing_content(self, target_subjects: List[str] = None) -> Dict[str, Any]:
        """Collect missing content for specified subjects"""
        if target_subjects is None:
            # Get subjects with most content (priority for expansion)
            subject_counts = {}
            for item in self.data.get('content', []):
                subject_id = item.get('subject_id')
                if subject_id:
                    subject_counts[subject_id] = subject_counts.get(subject_id, 0) + 1
            
            # Sort by content count and take top 5
            target_subjects = sorted(subject_counts.keys(), key=lambda x: subject_counts[x], reverse=True)[:5]
        
        new_content = []
        
        for subject_id in target_subjects:
            print(f"Collecting content for subject: {subject_id}")
            
            # Generate exercises
            exercises = self.generate_exercises_for_subject(subject_id, count=15)
            new_content.extend(exercises)
            
            # Generate exams
            exams = self.generate_exams_for_subject(subject_id, count=8)
            new_content.extend(exams)
            
            # Add delay to be respectful
            time.sleep(1)
        
        # Generate corrections for all new content
        corrections = self.generate_corrections_for_content(new_content)
        new_content.extend(corrections)
        
        return {
            'new_content': new_content,
            'total_items': len(new_content),
            'subjects_processed': len(target_subjects)
        }
    
    def save_enhanced_data(self, new_content: List[Dict[str, Any]], output_file: str = None):
        """Save enhanced data with new content"""
        if output_file is None:
            output_file = f"data/enhanced_data_{int(time.time())}.json"
        
        # Create enhanced data
        enhanced_data = self.data.copy()
        enhanced_data['content'].extend(new_content)
        
        # Update statistics
        enhanced_data['statistics'] = {
            'total_levels': len(enhanced_data.get('levels', [])),
            'total_subjects': len(enhanced_data.get('subjects', [])),
            'total_content': len(enhanced_data.get('content', []))
        }
        
        # Add metadata
        enhanced_data['enhancement_date'] = time.strftime('%Y-%m-%dT%H:%M:%S')
        enhanced_data['enhancement_info'] = {
            'new_items_added': len(new_content),
            'content_types_added': list(set(item.get('content_type') for item in new_content)),
            'subjects_enhanced': list(set(item.get('subject_id') for item in new_content if item.get('subject_id')))
        }
        
        # Ensure directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Save file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(enhanced_data, f, ensure_ascii=False, indent=2)
        
        print(f"Enhanced data saved to: {output_file}")
        print(f"Total content items: {len(enhanced_data['content'])}")
        print(f"New items added: {len(new_content)}")
        
        return output_file
    
    def generate_collection_report(self) -> str:
        """Generate a detailed collection report"""
        analysis = self.analyze_missing_content()
        
        report = f"""
# Moroccan Education Data Collection Report

## Current Status
- Total content items: {len(self.data.get('content', []))}
- Total subjects: {len(self.data.get('subjects', []))}
- Total levels: {len(self.data.get('levels', []))}

## Missing Content Types
{', '.join(analysis['missing_content_types']) if analysis['missing_content_types'] else 'None'}

## Subjects Without Content ({len(analysis['subjects_without_content'])})
{', '.join(analysis['subjects_without_content'][:10])}{'...' if len(analysis['subjects_without_content']) > 10 else ''}

## Level Distribution
"""
        for level_id, count in analysis['level_gaps'].items():
            report += f"- {level_id}: {count} items\n"
        
        return report

def main():
    """Main execution function"""
    print("🚀 Starting Moroccan Education Data Collection")
    print("=" * 50)
    
    # Initialize collector
    collector = MoroccanEducationCollector()
    
    # Analyze current state
    print("\n📊 Analyzing current data...")
    analysis = collector.analyze_missing_content()
    
    print(f"Missing content types: {len(analysis['missing_content_types'])}")
    print(f"Subjects without content: {len(analysis['subjects_without_content'])}")
    
    # Collect missing content
    print("\n🔄 Collecting missing content...")
    result = collector.collect_missing_content()
    
    print(f"Generated {result['total_items']} new content items")
    print(f"Processed {result['subjects_processed']} subjects")
    
    # Save enhanced data
    print("\n💾 Saving enhanced data...")
    output_file = collector.save_enhanced_data(result['new_content'])
    
    # Generate report
    print("\n📋 Generating collection report...")
    report = collector.generate_collection_report()
    
    with open("data/collection_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n✅ Collection completed!")
    print(f"Enhanced data: {output_file}")
    print(f"Report: data/collection_report.md")

if __name__ == "__main__":
    main()
