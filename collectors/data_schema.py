"""
Data Schema and Validation for Moroccan Education Data
Ensures data quality and consistency
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum
import re


class LevelCategory(str, Enum):
    """Level categories"""
    PRIMAIRE = "primaire"
    COLLEGE = "college"
    LYCEE = "lycee"
    BAC = "bac"
    SUPERIEUR = "superieur"


class ContentType(str, Enum):
    """Content types"""
    COURS = "cours"
    EXERCICE = "exercice"
    CONTROLE = "controle"
    EXAMEN = "examen"
    CORRECTION = "correction"
    VIDEO = "video"
    RESUME = "resume"


class Difficulty(str, Enum):
    """Difficulty levels"""
    FACILE = "facile"
    MOYEN = "moyen"
    DIFFICILE = "difficile"


@dataclass
class ValidationResult:
    """Validation result"""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    score: float = 1.0


class DataValidator:
    """Validates collected data"""
    
    @staticmethod
    def validate_level(level: dict) -> ValidationResult:
        """Validate level data"""
        result = ValidationResult(is_valid=True)
        
        # Required fields
        required_fields = ['id', 'name', 'name_ar', 'order', 'category']
        for field in required_fields:
            if not level.get(field):
                result.errors.append(f"Missing required field: {field}")
                result.is_valid = False
        
        # Validate order
        if level.get('order'):
            if not isinstance(level['order'], int) or level['order'] < 1:
                result.errors.append(f"Invalid order: {level.get('order')}")
                result.is_valid = False
        
        # Validate category
        if level.get('category'):
            try:
                LevelCategory(level['category'])
            except ValueError:
                result.errors.append(f"Invalid category: {level.get('category')}")
                result.is_valid = False
        
        # Check Arabic name
        if level.get('name_ar'):
            if not re.search(r'[\u0600-\u06FF]', level['name_ar']):
                result.warnings.append("Arabic name doesn't contain Arabic characters")
                result.score -= 0.1
        else:
            result.warnings.append("Missing Arabic name")
            result.score -= 0.2
        
        return result
    
    @staticmethod
    def validate_subject(subject: dict) -> ValidationResult:
        """Validate subject data"""
        result = ValidationResult(is_valid=True)
        
        # Required fields
        required_fields = ['id', 'name', 'level_id']
        for field in required_fields:
            if not subject.get(field):
                result.errors.append(f"Missing required field: {field}")
                result.is_valid = False
        
        # Check Arabic name
        if not subject.get('name_ar'):
            result.warnings.append("Missing Arabic name")
            result.score -= 0.2
        
        # Check level linkage
        if not subject.get('level_id'):
            result.errors.append("Subject not linked to any level")
            result.is_valid = False
        
        return result
    
    @staticmethod
    def validate_content(content: dict) -> ValidationResult:
        """Validate content data"""
        result = ValidationResult(is_valid=True)
        
        # Required fields
        required_fields = ['id', 'title', 'level_id', 'content_type']
        for field in required_fields:
            if not content.get(field):
                result.errors.append(f"Missing required field: {field}")
                result.is_valid = False
        
        # Validate content type
        if content.get('content_type'):
            try:
                ContentType(content['content_type'])
            except ValueError:
                result.errors.append(f"Invalid content type: {content.get('content_type')}")
                result.is_valid = False
        
        # Check Arabic title
        if not content.get('title_ar'):
            result.warnings.append("Missing Arabic title")
            result.score -= 0.2
        
        # Check linkage
        if not content.get('subject_id'):
            result.warnings.append("Content not linked to subject")
            result.score -= 0.1
        
        return result
    
    @staticmethod
    def validate_dataset(data: dict) -> Dict[str, any]:
        """Validate entire dataset"""
        results = {
            'levels': {'valid': 0, 'invalid': 0, 'warnings': 0, 'avg_score': 0},
            'subjects': {'valid': 0, 'invalid': 0, 'warnings': 0, 'avg_score': 0},
            'content': {'valid': 0, 'invalid': 0, 'warnings': 0, 'avg_score': 0},
            'overall_score': 0,
            'errors': [],
            'warnings': []
        }
        
        # Validate levels
        level_scores = []
        for level in data.get('levels', []):
            validation = DataValidator.validate_level(level)
            if validation.is_valid:
                results['levels']['valid'] += 1
            else:
                results['levels']['invalid'] += 1
                results['errors'].extend(validation.errors)
            
            results['levels']['warnings'] += len(validation.warnings)
            results['warnings'].extend(validation.warnings)
            level_scores.append(validation.score)
        
        if level_scores:
            results['levels']['avg_score'] = sum(level_scores) / len(level_scores)
        
        # Validate subjects
        subject_scores = []
        for subject in data.get('subjects', []):
            validation = DataValidator.validate_subject(subject)
            if validation.is_valid:
                results['subjects']['valid'] += 1
            else:
                results['subjects']['invalid'] += 1
                results['errors'].extend(validation.errors)
            
            results['subjects']['warnings'] += len(validation.warnings)
            results['warnings'].extend(validation.warnings)
            subject_scores.append(validation.score)
        
        if subject_scores:
            results['subjects']['avg_score'] = sum(subject_scores) / len(subject_scores)
        
        # Validate content
        content_scores = []
        for content in data.get('content', []):
            validation = DataValidator.validate_content(content)
            if validation.is_valid:
                results['content']['valid'] += 1
            else:
                results['content']['invalid'] += 1
                results['errors'].extend(validation.errors)
            
            results['content']['warnings'] += len(validation.warnings)
            results['warnings'].extend(validation.warnings)
            content_scores.append(validation.score)
        
        if content_scores:
            results['content']['avg_score'] = sum(content_scores) / len(content_scores)
        
        # Calculate overall score
        all_scores = level_scores + subject_scores + content_scores
        if all_scores:
            results['overall_score'] = sum(all_scores) / len(all_scores)
        
        return results


class DataCleaner:
    """Cleans and organizes data"""
    
    @staticmethod
    def remove_duplicates(items: List[dict], key_fields: List[str]) -> List[dict]:
        """Remove duplicates based on key fields"""
        seen = set()
        unique_items = []
        
        for item in items:
            key = tuple(item.get(field, '') for field in key_fields)
            if key not in seen:
                seen.add(key)
                unique_items.append(item)
        
        return unique_items
    
    @staticmethod
    def sort_levels(levels: List[dict]) -> List[dict]:
        """Sort levels by order"""
        return sorted(levels, key=lambda x: x.get('order', 999))
    
    @staticmethod
    def sort_subjects(subjects: List[dict]) -> List[dict]:
        """Sort subjects by name"""
        return sorted(subjects, key=lambda x: x.get('name', ''))
    
    @staticmethod
    def sort_content(content: List[dict]) -> List[dict]:
        """Sort content by type and title"""
        type_order = {
            'cours': 1,
            'exercice': 2,
            'controle': 3,
            'examen': 4,
            'correction': 5,
            'video': 6,
            'resume': 7
        }
        return sorted(content, key=lambda x: (
            type_order.get(x.get('content_type', ''), 99),
            x.get('title', '')
        ))
    
    @staticmethod
    def clean_dataset(data: dict) -> dict:
        """Clean entire dataset"""
        cleaned = data.copy()
        
        # Remove duplicates
        cleaned['levels'] = DataCleaner.remove_duplicates(
            data.get('levels', []),
            ['id', 'name']
        )
        
        cleaned['subjects'] = DataCleaner.remove_duplicates(
            data.get('subjects', []),
            ['id', 'name', 'level_id']
        )
        
        cleaned['content'] = DataCleaner.remove_duplicates(
            data.get('content', []),
            ['id', 'title', 'level_id']
        )
        
        # Sort
        cleaned['levels'] = DataCleaner.sort_levels(cleaned['levels'])
        cleaned['subjects'] = DataCleaner.sort_subjects(cleaned['subjects'])
        cleaned['content'] = DataCleaner.sort_content(cleaned['content'])
        
        return cleaned


class DataOrganizer:
    """Organizes data into hierarchical structure"""
    
    @staticmethod
    def organize_by_level(data: dict) -> dict:
        """Organize data by level"""
        organized = {}
        
        for level in data.get('levels', []):
            level_id = level['id']
            organized[level_id] = {
                'level': level,
                'subjects': [],
                'content': []
            }
        
        # Add subjects to levels
        for subject in data.get('subjects', []):
            level_id = subject.get('level_id')
            if level_id in organized:
                organized[level_id]['subjects'].append(subject)
        
        # Add content to levels
        for content in data.get('content', []):
            level_id = content.get('level_id')
            if level_id in organized:
                organized[level_id]['content'].append(content)
        
        return organized
    
    @staticmethod
    def generate_statistics(data: dict) -> dict:
        """Generate statistics"""
        stats = {
            'total_levels': len(data.get('levels', [])),
            'total_subjects': len(data.get('subjects', [])),
            'total_content': len(data.get('content', [])),
            'by_category': {},
            'by_content_type': {},
            'by_level': {}
        }
        
        # Count by category
        for level in data.get('levels', []):
            category = level.get('category', 'unknown')
            stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
        
        # Count by content type
        for content in data.get('content', []):
            content_type = content.get('content_type', 'unknown')
            stats['by_content_type'][content_type] = stats['by_content_type'].get(content_type, 0) + 1
        
        # Count by level
        for level in data.get('levels', []):
            level_id = level['id']
            stats['by_level'][level_id] = {
                'subjects': 0,
                'content': 0
            }
        
        for subject in data.get('subjects', []):
            level_id = subject.get('level_id')
            if level_id in stats['by_level']:
                stats['by_level'][level_id]['subjects'] += 1
        
        for content in data.get('content', []):
            level_id = content.get('level_id')
            if level_id in stats['by_level']:
                stats['by_level'][level_id]['content'] += 1
        
        return stats

